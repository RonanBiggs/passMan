from tkinter import *

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


    root.mainloop()

window_init()