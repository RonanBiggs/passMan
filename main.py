from tkinter import *
import sqlite3

def test(event, text):
    print(text.get())

def window_init():
    #draw window
    root=Tk()
    root.title('Tkinter Window - Center')
    window_width = 300
    window_height = 200
    root.geometry(f'{window_width}x{window_height}')
    #text entry box
    box_label = Label(root, text='tmp: ')
    box_label.pack(pady=2)

    #hide pass
    #entry = Entry(root, show='*')
    text_var = StringVar()
    entry = Entry(root, textvariable=text_var)
    entry.pack(pady=20)
    entry.focus()

    #output text
    #output_label = Label(root)
    #output_label.pack()
    #text_var.trace_add(
    #    "write",
    #    lambda *args: output_label.config(text=text_var.get().upper())
    #)


    #keyboard
    root.bind('<Return>', lambda event: test(event, text_var))

    root.mainloop()

class PasswordManagerDB:
    def __init__(self):
        self.init_db()
    def init_db(self):
        con = sqlite3.connect('passwords.db')
        cur = con.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            username TEXT,
            password TEXT NOT NULL,
            url TEXT,
            notes TEXT,
            created_at, DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at, DATETIME DEFAULT CURRENT_TIMESTAMP
        ''')
        con.commit()
        con.close()
    def add_password(self):
        pass
    def search_password(self):
        pass
    def del_password(self):
        pass
window_init()
db = PasswordManagerDB()