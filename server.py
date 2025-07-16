import socket
import threading

import settings

'''things to add:
- Add a server log that prints when a client connects or disconnects
- Add verification for client nickname to ensure no duplicates
- Add password protection for server access
- Add a command to list all connected clients
- Expand to internet access with proper security measures'''

client_list = []
nicknames = {}

def start_server():
    ### Starts the TCP server and listens for new client connections.
    global client_list, nicknames
    print("Starting server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((settings.host, settings.port))
    host, port = server_socket.getsockname()
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    try:
        #### Main server loop to accept connections
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}") ## use this info for server log
            # Start a new thread to handle the client and add client to the list
            client_list.append(client_socket) 
            client_thread = threading.Thread(target= handle_client, args= (client_socket,)) 
            client_thread.start()
            print (f"Active connections: {len(client_list)}") ## print number of active connections

            # client_socket.close() ## close connection after handling it
            # Additional per-connection handling code can go here
            
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        print("Cleaning up resources...")
        # Additional cleanup code can go here


def handle_client(client_socket):
    ### Handle a single client connection and assign a nickname
    global client_list, nicknames
    address = client_socket.getpeername()
    print(f"Handling client at {address}")
    nickname = client_socket.recv(1024).decode('utf-8')
    nicknames[address]=nickname
    welcome_message = f"Welcome {nickname} to the chat!"
    client_socket.send(welcome_message.encode('utf-8'))

    while True:
        ### Receive messages from the client
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Client {nickname} disconnected.")
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                break
            print(f"Received from {nickname}: {message}")
            # Broadcast the message to all connected clients
            for client in client_list:
                if client != client_socket:
                    client.send(f"Message from {nickname}: {message}".encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break
        continue   
    # Remove the client from the list and clean up
    client_list.remove(client_socket)
    del nicknames[address]


if __name__ == "__main__":
    start_server()