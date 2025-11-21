#TODO: implement handshake and database requests from gui
import socket
import json
from diffieHellman import *

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
        #initiate DH key exchange
        client_dh = DiffieHellmanParty()
        #gen pub/priv key
        client_dh.gen_keys()
        #recieve server public key
        server_public_key =  self.socket.recv(1024) #public key
        server_public_key = int(server_public_key.split(b'\n')[0])
        print(server_public_key)
        #send client public key
        self.socket.send(str(client_dh.public_key).encode() + b'\n')
        #compute shared key
        client_dh.compute_shared_secret(server_public_key)
        #compute aes key
        client_dh.get_aes_key()
        #recieve test encryption
        cipher_txt = self.socket.recv(1024)
        print(cipher_txt.split(b'\n')[0])
        print(client_dh.decrypt(cipher_txt, client_dh.iv))

        #self.socket.send("client reply".encode() + b'\n')
        #data = self.socket.recv(1024)
        #print(data)

#temporary test function
    def send_hello(self, event, text):
        self.socket.send(text.get().encode() + b'\n')
        data = self.socket.recv(1024)
        print(data)
#submit all fields of data to server for sql storing
    def send_all(self, acc_name, username, password, url, notes):
        self.socket.send("send_all".encode() + b'\n')
        response = self.socket.recv(1024)
        print(response)
        data = {
            "acc_name" : acc_name.get(),
            "username" : username.get(),
            "password" : password.get(),
            "url"      : url.get(),
            "notes"    : notes.get()
        }
        print(f"data: {data}")
        self.socket.send(json.dumps(data).encode() + b'\n')
        response = self.socket.recv(1024)
        print(response)
    def exit(self):
        self.socket.close()