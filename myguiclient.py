import socket
import threading
import tkinter as tk

import settings  # your settings.py file should define host and port

class ChatClient:
    ''' A simple chat client with a GUI using Tkinter '''
    def __init__(self, screen):
        ''' Initialize the chat client GUI and socket connection '''
        self.screen = screen
        self.screen.title("LaChat")

        # Frame for display area and scrollbar
        display_frame = tk.Frame(self.screen)
        display_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Display area for messages
        self.display_area = tk.Text(display_frame, height=20, width=50, state='disabled', wrap='word')
        self.display_area.pack(side='left', fill='both', expand=True)

        # Scrollbar for the display area
        scrollbar = tk.Scrollbar(display_frame, command=self.display_area.yview)
        scrollbar.pack(side='right', fill='y')
        self.display_area.config(yscrollcommand=scrollbar.set)

        # Frame for entry and send button
        entry_frame = tk.Frame(self.screen)
        entry_frame.pack(padx=10, pady=(0, 10), fill='x')

        # Chat box for typing messages
        self.chat_entry = tk.Entry(entry_frame, width=40)
        self.chat_entry.pack(side='left', padx=(0, 5), expand=True, fill='x')
        self.chat_entry.bind('<Return>', lambda event: self.send_message())

        # Send button
        self.send_button = tk.Button(entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side='left')

        # connect to server and prompt for nickname
        self.connect()
        self.get_nickname()

    def get_nickname(self):
        # prompt window for nickname
        self.nickname_window = tk.Toplevel(self.screen)
        self.nickname_window.geometry("350x120")
        self.nickname_window.attributes("-topmost", True)
        self.nickname_window.title("Enter Nickname")
        self.nickname_window.grab_set()
        tk.Label(self.nickname_window, text="Please enter your nickname:").pack(padx=10, pady=10)
        self.nickname_entry = tk.Entry(self.nickname_window)
        self.nickname_entry.pack(padx=10, pady=(0, 10))
        self.nickname_entry.focus_set()
        self.nickname_entry.bind('<Return>', lambda event: self.set_nickname())
        submit_btn = tk.Button(self.nickname_window, text="Submit", command=self.set_nickname)
        submit_btn.pack(pady=(0, 10))

    def connect(self):
        '''Establish connection to the server using host and port from settings'''
        self.display_area.config(state='normal')
        self.display_area.insert(tk.END, "Connecting to server...\n")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((settings.host, settings.port))
            self.display_area.insert(tk.END, "Connection Established...\n")
            self.display_area.config(state='disabled')
        except Exception as e:
            self.display_area.config(state='normal')
            self.display_area.insert(tk.END, f"Connection error: {e}\n")
            self.display_area.config(state='disabled')
            self.disconnect()
            
    def set_nickname(self):
        # set nick name and send to server
        self.nickname = self.nickname_entry.get().strip()
        self.sock.send(self.nickname.encode('utf-8'))
        self.nickname_window.destroy()
        self.screen.attributes("-topmost", True)
        self.display_area.config(state='normal')
        self.display_area.insert(tk.END, f"Nickname set to: {self.nickname}\n")
        self.display_area.config(state='disabled')

    

    def disconnect(self):
        '''Disconnect from the server and close the socket'''
        sock = getattr(self, 'sock', None)
        if hasattr(self, 'sock'):
            try:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                self.display_area.config(state='normal')
                self.display_area.insert(tk.END, "Disconnected from server.\n")
                self.display_area.config(state='disabled')
            except Exception as e:
                self.display_area.config(state='normal')
                self.display_area.insert(tk.END, f"Disconnect error: {e}\n")
                self.display_area.config(state='disabled')
            finally:
                self.sock = None

    def send_message(self):
        message = self.chat_entry.get()
        if message and hasattr(self, 'sock'):
            try:
                self.sock.send(message.encode())
                self.display_area.config(state='normal')
                self.display_area.insert(tk.END, f"You: {message}\n")
                self.display_area.config(state='disabled')
                self.chat_entry.delete(0, tk.END)
            except Exception as e:
                self.display_area.config(state='normal')
                self.display_area.insert(tk.END, f"Send error: {e}\n")
                self.display_area.config(state='disabled')

        # Bind Enter key to send_message in __init__ after self.send_button creation:
        pass





if __name__ == "__main__":
    screen = tk.Tk()
    client = ChatClient(screen)
    screen.mainloop()
