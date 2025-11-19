from tkinter import *
import sqlite3
import tkinter as tk
from PasswordManagerWindow import *
from server import *
from client import *


#with PasswordManagerDB() as db:
if __name__ == "__main__":
    app = PasswordManagerWindow()
    app.mainloop()