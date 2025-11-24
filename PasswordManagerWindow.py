import tkinter as tk
from client import *



LARGE_FONT= ("Verdana", 12)
class PasswordManagerWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.client = Client('localhost', 5432)
        self.client.connect()
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Add Account",
                           command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Lookup",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

def test(event, text):
    print(text.get())
class PageOne(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure((0, 1), weight=1)



        #TEXT INPUT VARIABLES
        acc_name_txt = tk.StringVar()
        username_txt = tk.StringVar()
        password_txt = tk.StringVar()
        url_txt = tk.StringVar()
        notes_txt = tk.StringVar()
        #LABELS
        win_label = tk.Label(self, text="Add Account Page", font=LARGE_FONT)
        acc_label = tk.Label(self, text="Account Name: ", font=LARGE_FONT)
        user_label = tk.Label(self, text="Username: ", font=LARGE_FONT)
        pass_label = tk.Label(self, text="Password: ", font=LARGE_FONT)
        url_label = tk.Label(self, text="URL: ", font=LARGE_FONT)
        notes_label = tk.Label(self, text="Notes: ", font=LARGE_FONT)
        #BUTTON
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        #button2 = tk.Button(self, text="Page Two",
        #                    command=lambda: controller.show_frame(PageTwo))
        submit_button = tk.Button(self, text="Submit Entry",
                            command=lambda: controller.client.add_password(acc_name_txt, username_txt, password_txt, url_txt, notes_txt))
        #TEXT ENTRIES
        acc_entry = tk.Entry(self, textvariable=acc_name_txt)
        user_entry = tk.Entry(self, textvariable=username_txt)
        pass_entry = tk.Entry(self, textvariable=password_txt)
        url_entry = tk.Entry(self, textvariable=url_txt)
        notes_entry = tk.Entry(self, textvariable=notes_txt)
        #FOCUS ON ACC NAME
        acc_entry.focus()

        #KEYBOARD BINDS
#        acc_entry.bind('<Return>', lambda event: controller.client.send_hello(event, acc_name_txt))
#        user_entry.bind('<Return>', lambda event: test(event, username_txt))
#        pass_entry.bind('<Return>', lambda event: test(event, password_txt))
#        url_entry.bind('<Return>', lambda event: test(event, url_txt))
#        notes_entry.bind('<Return>', lambda event: test(event, notes_txt))

        #ARRANGE ON SCREEN
        win_label.grid(row = 0, column = 1)
        acc_label.grid(row = 3, column = 0)
        user_label.grid(row = 4, column = 0)
        pass_label.grid(row = 5, column = 0)
        url_label.grid(row = 6, column = 0)
        notes_label.grid(row = 7, column = 0)
        button1.grid(row = 0, column = 0)
        #button2.grid(row=2, column=1)
        submit_button.grid(row=1, column=2)
        acc_entry.grid(row = 3, column = 1)
        user_entry.grid(row = 4, column = 1)
        pass_entry.grid(row = 5, column = 1)
        url_entry.grid(row = 6, column = 1)
        notes_entry.grid(row = 7, column = 1)



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        acc_name_txt = tk.StringVar()
        win_label = tk.Label(self, text="Search", font=LARGE_FONT)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))

        acc_entry = tk.Entry(self, textvariable=acc_name_txt)


        win_label.grid(row = 0, column = 2)
        button1.grid(row=0, column=0)
        acc_entry.grid(row=1,column=2)
