import ast
import string
import secrets
import socket
import json
import os
from diffieHellman import *

class Client:
    def __init__(self, host='localhost', port=5432):
        self.host = host
        self.port = port
        self.socket = None
        self.client_dh = DiffieHellmanParty()

        # --- Search Result Vars ---
        self.search_result = "[]"

        #get or create password key
        filename = "secret_key.txt"
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                secret = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(256))
                self.encryption_key = secret
                f.write(secret)
        else:
            with open(filename, 'r') as f:
                self.encryption_key = f.read()



    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        greeting = self.socket.recv(1024).decode().strip()
        print(f"Server greeting: {greeting}")
        #initiate DH key exchange
#        self.client_dh = DiffieHellmanParty()
        #gen pub/priv key
        self.client_dh.gen_keys()
        #recieve server public key
        server_public_key =  self.socket.recv(1024) #public key
        server_public_key = int(server_public_key.split(b'\n')[0])
        print(server_public_key)
        #send client public key
        self.socket.send(str(self.client_dh.public_key).encode() + b'\n')
        #compute shared key
        self.client_dh.compute_shared_secret(server_public_key)
        #compute aes key
        self.client_dh.get_aes_key()
        #recieve test encryption
        cipher_txt = self.socket.recv(1024)
        print(cipher_txt.split(b'\n')[0])
        print(self.client_dh.decrypt(cipher_txt, self.client_dh.iv))

        #self.socket.send("client reply".encode() + b'\n')
        #data = self.socket.recv(1024)
        #print(data)



#send an encrypted message to the server
    def send(self, data):
       self.socket.send(self.client_dh.encrypt(data, self.client_dh.iv))
    def recv(self):
        return self.client_dh.decrypt(self.socket.recv(1024), self.client_dh.iv)

#temporary test function
    def send_hello(self, event, text):
        self.socket.send(text.get().encode() + b'\n')
        data = self.socket.recv(1024)
        print(data)
#submit all fields of data to server for sql storing
    def add_password(self, acc_name, username, password, url, notes):
#        self.socket.send("add_password".encode() + b'\n')
        self.send("add_password")
        response = self.recv()
        print(response)
        plaintext_pass = password.get()
        encrypted_pass = ""
        for i, char in enumerate(plaintext_pass):
            encrypted_char = chr(ord(char) ^ ord(self.encryption_key[i]))
            encrypted_pass = encrypted_pass + encrypted_char
        data = {
            "acc_name" : acc_name.get(),
            "username" : username.get(),
            "password" : encrypted_pass,
            "url"      : url.get(),
            "notes"    : notes.get()
        }
        print(f"data: {data}")
#        self.socket.send(json.dumps(data).encode() + b'\n')
        self.send(json.dumps(data))
        response = self.socket.recv(1024)
        print(response)
#send account name, expect all data back.
    def search_password(self, acc_name):
        self.send("search_password")
        response = self.recv()
        print(response)
        self.send(acc_name)
        response = self.recv()
        #TODO: Serverside message for no account found instead of empty list maybe?
        if response == "[]":
            print("No Account Found")
            return
        parsed_data = list(ast.literal_eval(response)[0]) #parses the sql row into a python list. i.e. parsed_data[1] = username
        #decrypt password
        decrypted_pass = ""
        for i, char in enumerate(parsed_data[3]):
            decrypted_char = chr(ord(char) ^ ord(self.encryption_key[i]))
            decrypted_pass = decrypted_pass + decrypted_char

        parsed_data[3] = decrypted_pass
        self.search_result = parsed_data
        print(parsed_data)

    def exit(self):
        self.socket.close()