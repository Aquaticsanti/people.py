# This follows the GeeksForGeeks tutorial here: https://www.geeksforgeeks.org/python/create-first-gui-application-using-python-tkinter/
from tkinter import *
import sqlite3

db = sqlite3.connect('people.db')
cur = db.cursor()
if cur.execute("SELECT name FROM sqlite_master").fetchone() == None:
    empty = True
    id = 0
    cur.execute("""CREATE TABLE people(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          text,
    surname       text,
    phone         text,
    email         text);""")
else:
    empty = False
    id = cur.execute("select id from people order by rowid desc LIMIT 1")
    if id.fetchone() == None:
        empty = True
        id = 0
    else:
        print(id.fetchone())
        id = id.fetchone()

def NewContact():
    def saveExit():
        contactInfo = []
        for entry in dynamic_entry:
            contactInfo.append(str(entry.get()))
        cur.execute(f"INSERT INTO people (name, surname, phone, email) VALUES (?, ?, ?, ?)", (contactInfo))
        db.commit()
        newContactWindow.destroy()
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

    exitbtn = Button(newContactWindow, text = "Save and Exit", command=saveExit)
    exitbtn.grid()
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
    if empty == True:
        # adding a label to the root window
        lbl = Label(root, text = "Create some contacts to get started!")
        lbl.grid()
    # adding Entry Field
    #  txt = Entry(root, width=10)
    #  txt.grid(column =1, row =0)
    # function to display user text when
    # button is clicked
    #  def clicked():
    #      res = "You wrote" + txt.get()
    #      lbl.configure(text = res)
    # button widget with red color text inside
    #  btn = Button(root, text = "Click me" ,
    #              fg = "red", command=clicked)
    # Set Button Grid
    #  btn.grid(column=2, row=0)
    btn2 = Button(root, text="Exit", command=root.destroy)
    btn2.grid(column=3, row=0)
    return root
# Execute Tkinter
root = main()
root.mainloop()