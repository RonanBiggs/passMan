import tkinter as tk
from client import *



LARGE_FONT= ("Verdana", 12)
class PasswordManagerWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.client = Client('localhost', 5432)
        self.client.connect()
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, SearchResults, DeletePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_close(self):
        try:
            self.client.exit()
        except:
            pass
        self.destroy()

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

        delete_button = tk.Button(self, text="Delete Account",
                            command=lambda: controller.show_frame(DeletePage))
        delete_button.pack()


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
        submit_button = tk.Button(self, text="Submit Entry",
                                  command=lambda: (controller.client.search_password(acc_name_txt.get()) or controller.show_frame(SearchResults)))

        acc_entry = tk.Entry(self, textvariable=acc_name_txt)


        win_label.grid(row = 0, column = 2)
        button1.grid(row=0, column=0)
        submit_button.grid(row=1,column=1)
        acc_entry.grid(row=1,column=2)


class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        win_label = tk.Label(self, text="Search Results", font=LARGE_FONT)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        win_label.grid(row=0, column=2)
        button1.grid(row=0, column=0)

        self.results_label = tk.Label(self, text="", font=LARGE_FONT)
        self.username_label = tk.Label(self, text="", font=LARGE_FONT)
        self.password_label = tk.Label(self, text="", font=LARGE_FONT)
        self.notes_label = tk.Label(self, text="", font=LARGE_FONT)
        self.url_label = tk.Label(self, text="", font=LARGE_FONT)

        
    def tkraise(self, aboveThis=None):
        tk.Frame.tkraise(self, aboveThis)
        self.update_page()
    def update_page(self):
        self.results_label.grid_forget()
        self.username_label.grid_forget()
        self.password_label.grid_forget()
        self.notes_label.grid_forget()
        self.url_label.grid_forget()
        if self.controller.client.search_result == "[]" or "":
            self.results_label.config(text="No Account Found")
            self.results_label.grid(row=1, column=2)
        else:
            result = self.controller.client.search_result
            self.username_label.config(text=f"Username: {result[2]}")
            self.password_label.config(text=f"Password: {result[3]}")
            self.notes_label.config(text=f"Notes: {result[4]}")
            self.url_label.config(text=f"URL: {result[5]}")
            self.username_label.grid(row=1, column=1)
            self.password_label.grid(row=2, column=1)
            self.notes_label.grid(row=3, column=1)
            self.url_label.grid(row=4, column=1)
            self.controller.client.search_result = "[]"



class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        acc_name_txt = tk.StringVar()
        win_label = tk.Label(self, text="Delete an Account", font=LARGE_FONT)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        submit_button = tk.Button(self, text="Submit",
                                  command=lambda: (controller.client.delete_account(acc_name_txt.get())))

        acc_entry = tk.Entry(self, textvariable=acc_name_txt)


        win_label.grid(row = 0, column = 2)
        button1.grid(row=0, column=0)
        submit_button.grid(row=1,column=1)
        acc_entry.grid(row=1,column=2)
