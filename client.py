import socket
import threading

import settings

''' things to add:
- Begin building a GUI for the client'''

def start_client():
    print("Connecting to server...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((settings.host, settings.port))
    print("Connected to server.")
    nickname = input("Enter your nickname: ")
    client_socket.send(nickname.encode('utf-8'))

    # Start a thread to handle incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    run_client(client_socket)

    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    print("Disconnected from server.")


def run_client(client_socket):
    # Main loop to send messages
    print("Type your message (or /quit to exit):")
    while True:
        # Read user input
        message = input("")
        if message.strip().lower() == "/quit":
            break
        client_socket.send(message.encode('utf-8'))

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                continue
            # Print the received message
            print(f"Received: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    
    
    client_socket.close()
    print("Connection closed.")



if __name__ == "__main__":
    start_client()