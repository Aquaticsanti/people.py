# This follows the GeeksForGeeks tutorial here: https://www.geeksforgeeks.org/python/create-first-gui-application-using-python-tkinter/
from tkinter import *


def NewContact():
    newContactWindow = Tk()
    newContactWindow.title("Create new Contact")
    # Set geometry(widthxheight)
    newContactWindow.geometry('308x144')

    items = ["Name", "Surname", "Phone", "Email"]
    dynamic_label = []
    dynamic_entry = []
    i = 0
    for item in items:
        label = Label(newContactWindow, text = item)
        dynamic_label.append(label  )
        label.grid(row=i)

        entry = Entry(newContactWindow, width=25)
        dynamic_entry.append(entry)
        entry.grid(row=i, column=1)
        i += 1
    #nameLabel = Label(newContactWindow, text = "Name")
    #nameLabel.grid()

    #nameEntry = Entry(newContactWindow, width=25)
    #nameEntry.grid(column=1, row=0)

    #surnameLabel = Label(newContactWindow, text="Surname")
    #surnameLabel.grid(row=1)

    #surnameEntry = Entry(newContactWindow, width=25)
    #surnameEntry.grid(column=1, row=1)

    #emailLabel = Label(newContactWindow, text="Email")
    #emailLabel.grid(row=2)

    #emailEntry = Entry(newContactWindow, width=25)
    #emailEntry.grid(column=1, row=2)

    #phoneLabel = Label(newContactWindow, text="Phone")
    #phoneLabel.grid(row=3)

    #phoneEntry = Entry(newContactWindow, width=25)
    #phoneEntry.grid(column=1, row=3)

    btn = Button(newContactWindow, text = "Exit", command=newContactWindow.destroy)
    btn.grid()
    newContactWindow.mainloop()

def main() -> Tk:
    root = Tk()
    # root window title and dimension
    root.title("people.py")
    # Set geometry(widthxheight)
    root.geometry('350x200')
    # adding menu bar in root window
    # new item in menu bar labelled as 'New'
    # adding more items in the menu bar 
    menu = Menu(root)
    item = Menu(menu, tearoff=False)
    item.add_command(label='New Contact', command=NewContact)
    menu.add_cascade(label='New', menu=item)
    root.config(menu=menu)
    # adding a label to the root window
    lbl = Label(root, text = "Placeholder text broo")
    lbl.grid()
    # adding Entry Field
    txt = Entry(root, width=10)
    txt.grid(column =1, row =0)
    # function to display user text when
    # button is clicked
    def clicked():
        res = "You wrote" + txt.get()
        lbl.configure(text = res)
    # button widget with red color text inside
    btn = Button(root, text = "Click me" ,
                fg = "red", command=clicked)
    # Set Button Grid
    btn.grid(column=2, row=0)
    btn2 = Button(root, text="Exit", command=root.destroy)
    btn2.grid(column=3, row=0)
    return root
# Execute Tkinter
root = main()
root.mainloop()