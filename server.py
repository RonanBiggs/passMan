import sqlite3
import json
import socket
from diffieHellman import *
import secrets
import string

#TODO: Extending passwordManagerDB to also be the server
#TODO: handle handshake and database requests
class PasswordManagerDB:
    #init server
    greeting = {
        "version": "1.0",
        "server": "passmanServer/1.0",
        "status": "ready"
    }
    def __init__(self, db='passwords.db', host='localhost', port=5432):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.host = host
        self.port = port
        self.running = False
        self.server_dh = None
    def __enter__(self): #Runs as start of with
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            username TEXT,
            salt CHAR(16),
            password TEXT NOT NULL,
            url TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);
        ''')
        self.con.commit()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb): #Runs at end of with
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()
    def send(self, client_socket, data):
        client_socket.send(self.server_dh.encrypt(data, self.server_dh.iv))
    def recv(self, client_socket):
        return self.server_dh.decrypt(client_socket.recv(1024), self.server_dh.iv)
    #SERVER FUNCTIONS
    def start(self):
        self.running = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)  # Allow up to 5 pending connection
        print(f"Server listening on port {self.port}")

        while self.running:
            client_socket, addr = s.accept()
            #TODO: multithreading
            with client_socket:
                print(f"connection from {addr}")
                client_socket.send(json.dumps(self.greeting).encode() + b'\n')
                #Incoming Connection: initiate DH
                self.server_dh = DiffieHellmanParty()
                #gen public/private key
                self.server_dh.gen_keys()
                #send server public key
                client_socket.send(str(self.server_dh.public_key).encode() + b'\n')
                #recieve client public key
                client_public_key = client_socket.recv(1024)
                client_public_key = int(client_public_key.split(b'\n')[0])
                #gen shared key
                shared_key = self.server_dh.compute_shared_secret(client_public_key)
                #gen aes key
                self.server_dh.get_aes_key()
                client_socket.send(self.server_dh.encrypt("cipher text from server", self.server_dh.iv))
                while True:
                    response = self.server_dh.decrypt(client_socket.recv(1024), self.server_dh.iv)
                    if not response:
                        print(f"client {addr} disconnected")
                        break
                    switch = {
                        'add_password' : lambda : self.add_password_response(client_socket),
                        'search_password' : lambda : self.search_password_response(client_socket),
                        'other' : lambda : client_socket.sendall(response)
                    }
                    print(f"response: {response}")#.decode().strip()
                    function_result = switch.get(response, lambda: "unknown")()
                    self.send(client_socket, function_result)
                    #client_socket.sendall(self.server_dh.encrypt(response, self.server_dh.iv))


    #RESPONSE FUNCTIONS

    #sendall response - servers action taken when sendall command is received (submitting all fields)
    def add_password_response(self, client_socket):
        client_socket.sendall(self.server_dh.encrypt("add_password: OKAY", self.server_dh.iv))
        #self.add_password(self, an, u, p, url, notes)
        response = self.server_dh.decrypt(client_socket.recv(1024), self.server_dh.iv)
        parsed_data = json.loads(response)#.decode('utf-8'))
        acc_name = parsed_data['acc_name']
        username = parsed_data['username']
        #idk why i thought i could hash the passwords. doesn't really work.
        #salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        #password = SHA256.new(data=(parsed_data['password'] + salt).encode('utf-8')).hexdigest()
        password = parsed_data['password']
        url = parsed_data['url']
        notes = parsed_data['notes']
        self.add_password(acc_name, username, password, url, notes)
        return f"added: {response}"
        
    def search_password_response(self, client_socket):
        client_socket.sendall(self.server_dh.encrypt("search_password: OKAY", self.server_dh.iv))
        response = self.recv(client_socket)
        data = str(self.search_password(response))
        return data
        #self.send(client_socket, data)

    #DATABASE FUNCTIONS
    def add_password(self, account_name=None, username=None, password=None, url=None, notes=None):
        self.cur.execute("INSERT INTO passwords (account_name, username, password, url, notes) VALUES ('%s', '%s', '%s', '%s', '%s')"%(account_name, username, password, url, notes))
        self.con.commit()

    def update_password(self, account_name=None, username=None, password=None, url=None, notes=None):
        if account_name is None:
            raise ValueError("No Such Account")

        updates = []
        params = []
        fields = [
            ('username', username),
            ('password', password),
            ('url', url),
            ('notes', notes)
        ]

        for column, value in fields:
            if value is not None:
                updates.append(f"{column} = ?")
                params.append(value)

        if updates is None:
            raise ValueError("No New Changes")

        params.append(account_name)
        sql = f"UPDATE passwords SET {', '.join(updates)} WHERE account_name = ?"
        self.cur.execute(sql, params)
        self.con.commit()


    def search_password(self, acc_name):
        self.cur.execute(f"SELECT * FROM passwords WHERE account_name = '{acc_name}'")
        output = self.cur.fetchall()
        return output

    def del_password(self, account_name):
        sql = 'DELETE FROM passwords WHERE account_name = ?'
        self.cur.execute(sql, (account_name,))
        self.con.commit()

if __name__ == "__main__":
    with PasswordManagerDB() as db:
        db.start()