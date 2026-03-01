# This follows the GeeksForGeeks tutorial here: https://www.geeksforgeeks.org/python/create-first-gui-application-using-python-tkinter/
from tkinter import *
from tkinter import ttk
import time
import sqlite3

def NewContact():
    root.destroy()
    def saveExit():
        contactInfo = []
        for entry in dynamic_entry:
            contactInfo.append(str(entry.get()))
        cur.execute(f"INSERT INTO people (name, surname, phone, email) VALUES (?, ?, ?, ?)", (contactInfo))
        db.commit()
        global root
        root = main()
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
    global db
    db = sqlite3.connect('people.db')
    global cur
    cur = db.cursor()
    if cur.execute("SELECT name FROM sqlite_master").fetchone() == None:
        empty = True
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
    root = Tk()
    # root window title and dimension
    root.title("people.py")
    # Set geometry(widthxheight)
    root.geometry('375x200')
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
    else:
        rows = cur.execute("SELECT * FROM people")
        rows = rows.fetchall()
        rows.insert(0, ('ID', 'Name', 'Surname', 'Phone', 'Email'))
        i = 0
        for j in rows:
            h = 0
            for k in j:
                lbl = Label(root, text=k, font=("TkDefaultFont", 12), wraplength=0.25)
                lbl.grid(column=h, row=i)
                h += 1
            if i > 0:
                ttk.Separator(root, orient="horizontal").grid(row=i-1, sticky="ew", columnspan=10, padx=0, pady=0)
                ttk.Separator(root, orient="horizontal").grid(row=i+1, sticky="ew", columnspan=10, padx=0, pady=0)
            else:
                pass
            
            i += 2
    btn2 = Button(root, text="Exit", command=root.destroy)
    try:
        if i == 0:
            pass
    except UnboundLocalError:
        btn2.grid(column=0, row=1)
    else:
        btn2.grid(column=0, row=i)
    return root
# Execute Tkinter
root = main()
root.mainloop()