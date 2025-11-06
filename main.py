from tkinter import *
import sqlite3
import tkinter as tk
from PasswordManagerWindow import *


def test(event, text):
    print(text.get())

'''
def window_init():
    # ====== draw window ======
    root=Tk()
    root.title('Tkinter Window - Center')
    window_width = 300
    window_height = 200
    root.geometry(f'{window_width}x{window_height}')

   # ====== buttons ======
    button = Button(root, text="Add Account", command=lambda : print("cool"))
    button.pack(ipadx=5, ipady=5, expand=True)
    #text entry box
    #box_label = Label(root, text='tmp: ')
    #box_label.pack(pady=2)
    #hide pass
    #entry = Entry(root, show='*')
    #text_var = StringVar()
    #entry = Entry(root, textvariable=text_var)
    #entry.pack(pady=20)
    #entry.focus()
    #output text
    #output_label = Label(root)
    #output_label.pack()
    #text_var.trace_add(
    #    "write",
    #    lambda *args: output_label.config(text=text_var.get().upper())
    #)
    #keyboard
    #root.bind('<Return>', lambda event: test(event, text_var))

    root.mainloop()
'''


class PasswordManagerDB:
    con = sqlite3.connect('passwords.db')
    cur = con.cursor()
    def __init__(self):
        pass
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

with PasswordManagerDB() as db:
    app = PasswordManagerWindow()
    app.mainloop()
