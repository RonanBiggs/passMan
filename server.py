import sqlite3
import json
import socket
from diffieHellman import *

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
    def __enter__(self): #Runs as start of with
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            username TEXT,
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
                server_dh = DiffieHellmanParty()
                #gen public/private key
                server_dh.gen_keys()
                #send server public key
                client_socket.send(str(server_dh.public_key).encode() + b'\n')
                #recieve client public key
                client_public_key = client_socket.recv(1024)
                client_public_key = int(client_public_key.split(b'\n')[0])
                #gen shared key
                shared_key = server_dh.compute_shared_secret(client_public_key)
                #gen aes key
                server_dh.get_aes_key()
                client_socket.send(server_dh.encrypt("cipher text from server", server_dh.iv))
                while True:
                    response = client_socket.recv(1024)
                    switch = {
                        b'send_all\n' : lambda : self.send_all_response(client_socket),
                        b'other\n' : lambda : client_socket.sendall(response)
                    }
                    print(f"response: {response}")#.decode().strip()
                    switch.get(response, lambda: print("unknown"))()
                    client_socket.sendall(response)

    #RESPONSE FUNCTIONS

    #sendall response - servers action taken when sendall command is received (submitting all fields)
    def send_all_response(self, client_socket):
        client_socket.sendall("send_all: OKAY".encode())
        #self.add_password(self, an, u, p, url, notes)
        response = client_socket.recv(1024)
        parsed_data = json.loads(response.decode('utf-8'))
        acc_name = parsed_data['acc_name']
        username = parsed_data['username']
        password = parsed_data['password']
        url = parsed_data['url']
        notes = parsed_data['notes']
        self.add_password(acc_name, username, password, url, notes)
        print(f"sarr: {response}")

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


    def search_password(self):
        self.cur.execute("SELECT * FROM passwords WHERE account_name = 'google'")
        output = self.cur.fetchall()
        print(output)

    def del_password(self, account_name):
        sql = 'DELETE FROM passwords WHERE account_name = ?'
        self.cur.execute(sql, (account_name,))
        self.con.commit()

if __name__ == "__main__":
    with PasswordManagerDB() as db:
        db.start()