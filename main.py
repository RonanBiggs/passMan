from tkinter import *
import sqlite3
import tkinter as tk
from PasswordManagerWindow import *
from server import *




class Client:
    def __init__(self, host='localhost', port=5432):
        self.host = host
        self.port = port
        self.socket = None
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        greeting = self.socket.recv(1024).decode().strip()
        print(f"Server greeting: {greeting}")
#with PasswordManagerDB() as db:
if __name__ == "__main__":
#    app = PasswordManagerWindow()
#    app.mainloop()
    client = Client('localhost', 5432)
    client.connect()
