# This follows the GeeksForGeeks tutorial here: https://www.geeksforgeeks.org/python/create-first-gui-application-using-python-tkinter/
from tkinter import *
from tkinter import ttk
import sqlite3
from functools import partial
import os
import pyperclip
import sys

def GetColumns():
    data = cur.execute('SELECT * FROM people')
    columns = []
    for i in list(data.description):
        columns += i
    while True:
        try:
            columns.remove(None)
        except:
            return columns

def NewContact(index: int = -1):
    def saveExit():
        global root
        if index == -1:
            contactInfo = []
            for entry in dynamic_entry:
                contactInfo.append(str(entry.get()))
            cur.execute(f"INSERT INTO people {tuple(items)} VALUES {tuple(contactInfo)}")
            db.commit()
            newContactWindow.destroy()
            root.destroy()
            root = main()
        else:
            global rows
            contactInfo = []
            for entry in dynamic_entry:
                contactInfo.append(str(entry.get()))
            update = ""
            for item, info in zip(items, contactInfo):
                update += f'{item}="{info}", '
            update = update[:-2]
            cur.execute(f"UPDATE people SET {update} WHERE id={index}")
            db.commit()
            newContactWindow.destroy()
            root.destroy()
            root = main()
            rows = cur.execute("SELECT * FROM people")
            rows = rows.fetchall()
            rows.insert(0, columns)
    id = cur.execute('select * from people')
    id = id.fetchall()
    try:
        id = id[-1][0]+1
    except IndexError:
        id = 1
    newContactWindow = Toplevel(root)
    if index == -1:
        newContactWindow.title("Create new Contact")
    else:
        newContactWindow.title(f"Editing Contact #{index}")
    # Set geometry(widthxheight)
    newContactWindow.configure(padx=5, pady=5)

    items = columns[1:]
    dynamic_label = []
    dynamic_entry = []
    i = 1

    idLabel = Label(newContactWindow, text="ID")
    idLabel.grid(row=0)
    if index == -1:
        idLabel2 = Label(newContactWindow, text=id)
        idLabel2.grid(row=0, column=1, sticky="w")
        for item in items:
            label = Label(newContactWindow, text = item)
            dynamic_label.append(label)
            label.grid(row=i)

            entry = Entry(newContactWindow, width=25)
            dynamic_entry.append(entry)
            entry.grid(row=i, column=1)
            i += 1
    else:
        idLabel2 = Label(newContactWindow, text=index)
        idLabel2.grid(row=0, column=1, sticky="w")
        contactInfo = cur.execute("SELECT * FROM people WHERE id = ?", (index,))
        contactInfo = list(contactInfo.fetchone())
        contactInfo.pop(0)
        for info, item in zip(contactInfo, items):
            if type(item) == int:
                continue
            label = Label(newContactWindow, text = item)
            dynamic_label.append(label)
            label.grid(row=i)

            entry = Entry(newContactWindow, width=25)
            if info is not None:
                entry.insert(0, info)
            dynamic_entry.append(entry)
            entry.grid(row=i, column=1)
            i += 1

    exitbtn = Button(newContactWindow, text = "Save and Exit", command=saveExit)
    exitbtn.grid()
    newContactWindow.mainloop()

def newFields() -> Tk:
    FieldsWindow = Toplevel(root)
    FieldsWindow.configure(padx=5, pady=5)
    FieldsWindow.title("Managing fields")
    fields = cur.execute("PRAGMA table_info(people)")
    fields = fields.fetchall()
    fieldsTemp = []
    elements = []
    def editField(index: int, save: bool = False):
        canChange = True
        if save == False:
            for trio in elements:
                if canChange == False:
                    break
                if trio[0]["text"] == '     ✔️':
                    canChange = False
                else:
                    canChange = True
            if canChange == True:
                elements[index][0].configure(text='     ✔️', command=partial(editField, index, True))
                elements[index][2].configure(state="normal")
                exit.configure(state="disabled")
                global oldName
                oldName = elements[index][2].get()
        else:
            elements[index][0].configure(text='     ✏️', command=partial(editField, index))
            cur.execute(f"ALTER TABLE people RENAME COLUMN '{oldName}' to '{elements[index][2].get()}'")
            elements[index][2].configure(state="disabled")
            exit.configure(state="normal")
            db.commit()

    def deleteField(index: int, columnName: str):
        for element in elements[index]:
            element.destroy()
        cur.execute(f"ALTER TABLE people DROP COLUMN '{columnName}'")
        db.commit()
    global i
    for t, i in zip(fields, range(len(fields))):
        fieldsTemp.append(t[1])
        if t[1] != "id":
            edit = Button(FieldsWindow, text='     ✏️', width=2, command=partial(editField, i))
            edit.grid(row=i, column=0)
            delete = Button(FieldsWindow, text='     🗑️', width=2, command=partial(deleteField, i, t[1]))
            delete.grid(row=i, column=1)
        else:
            edit = Button(FieldsWindow, text='     ✏️', width=2, state="disabled")
            edit.grid(row=i, column=0)
            delete = Button(FieldsWindow, text='     🗑️', width=2, state="disabled")
            delete.grid(row=i, column=1)
        lbl = Entry(FieldsWindow, font=("TkDefaultFont", 12))
        lbl.insert(0, t[1])
        lbl.configure(state="disabled")
        lbl.grid(row=i, column=2)
        elements.append((edit, delete, lbl))
    def CreateField():
        global i
        def SaveNewField():
            global i
            elements[-1][0].configure(text='     ✏️', command=partial(editField, i+1))
            cur.execute(f"ALTER TABLE people ADD '{elements[-1][2].get()}' text")
            elements[-1][2].configure(state="disabled")
            exit.configure(state="normal")
            db.commit()
            i += 1
            
        def CancelNewField():
            edit.destroy()
            delete.destroy()
            lbl.destroy()
            exit.configure(state="active")
            elements.pop()
        edit = Button(FieldsWindow, text='     ✔️', width=2, state="active", command=SaveNewField)
        edit.grid(row=i+1, column=0)
        delete = Button(FieldsWindow, text='     🗑️', width=2, state="active", command=CancelNewField)
        delete.grid(row=i+1, column=1)
        lbl = Entry(FieldsWindow, font=("TkDefaultFont", 12))
        lbl.grid(row=i+1, column=2)
        elements.append((edit, delete, lbl))
        exit.configure(state="disabled")
        exit.grid(row=i+2)
        new.grid(row=i+2)
    new = Button(FieldsWindow, text='+', width=4, command=CreateField, font=("TkDefaultFont", 12, "bold"))
    new.grid(column=0, row=i+2, columnspan=2, sticky="we")
    def saveExit():
        global columns
        global root
        columns = GetColumns()
        FieldsWindow.destroy()
        root.destroy()
        root = main()
        root.mainloop()
    exit = Button(FieldsWindow, text='Done', width=4, command=saveExit, font=("TkDefaultFont", 12, "bold"))
    exit.grid(column=2, row=i+2, columnspan=2, sticky="we")
    fieldsTemp = fields
    del fieldsTemp
    FieldsWindow.mainloop()

def main() -> Tk:
    global db
    global cur
    global columns
    global dbFile
    global empty
    global logo
    files = os.listdir()
    for i in range(3):
        for file in files:
            if ".db" not in file:
                files.pop(files.index(file))
    if len(files) == 1 and files[0] == 'people.db': # AKA the only DB is people.db
        empty = False
        db = sqlite3.connect('people.db')
        cur = db.cursor()
        try:
            id = cur.execute('select * from people')
        except sqlite3.OperationalError:
            empty = True
            cur.execute("""CREATE TABLE people(
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          text,
            surname       text,
            phone         text,
            email         text);""")
            columns = ["id", "name", "surname", "phone", "email"]
        if empty == False:
            try:
                id = id.fetchall()[-1]
            except IndexError:
                empty = True
            else:
                empty = False
            columns = GetColumns()
    elif len(files) == 0: # AKA there is no DB
        empty = True
        db = sqlite3.connect('people.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE people(
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        name          text,
        surname       text,
        phone         text,
        email         text);""")
        columns = ["id", "name", "surname", "phone", "email"]
    else:
        global dbFile
        if "dbFile" not in globals(): # AKA hasn't selected yet
            conflictWindow = Tk()
            if getattr(sys, 'frozen', False):
                logo = PhotoImage(file=os.path.join(sys._MEIPASS, "files/logo.png"))
            else:
                logo = PhotoImage(file="logo.png")
            conflictWindow.iconphoto(True, logo)
            conflictWindow.title("Multiple databases detected")
            conflictLBL = Label(conflictWindow, text=("""Looks like multiple databases have been detected! 
Please choose the one you'd like to open:"""))
            conflictLBL.grid(row=0, column=0)
            def SetDB(dbFileI: str):
                global empty
                global dbFile
                global cur
                global db
                global columns
                dbFile = dbFileI
                empty = False
                db = sqlite3.connect(dbFile)
                cur = db.cursor()
                try:
                    id = cur.execute('select * from people')
                except sqlite3.OperationalError:
                    empty = True
                    cur.execute("""CREATE TABLE people(
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    name          text,
                    surname       text,
                    phone         text,
                    email         text);""")
                    columns = ["id", "name", "surname", "phone", "email"]
                if empty == False:
                    try:
                        id = id.fetchall()[-1]
                    except IndexError:
                        empty = True
                    else:
                        empty = False
                    columns = GetColumns()
                conflictWindow.destroy()
            for dbs, i in zip(files, range(len(files)+1)):
                btn = Button(conflictWindow, text=dbs, command=partial(SetDB, dbs))
                btn.grid(row=i+1, column=0)
            conflictWindow.mainloop()



    root = Tk()
    # root window title and dimension
    root.title("people.py")
    # Set geometry(widthxheight)
    root.configure(padx=5, pady=5)
    if getattr(sys, 'frozen', False):
        logo = PhotoImage(file=os.path.join(sys._MEIPASS, "files/logo.png"))
    else:
        logo = PhotoImage(file="logo.png")
    root.iconphoto(True, logo)
    # adding menu bar in root window
    # new item in menu bar labelled as 'New'
    # adding more items in the menu bar 
    menu = Menu(root)
    item = Menu(menu, tearoff=False)
    item.add_command(label='New Contact', command=NewContact)
    item.add_command(label='Manage Fields', command=newFields)
    item.add_separator()
    item.add_command(label='Exit', command=root.destroy)
    menu.add_cascade(label='File', menu=item)
    root.config(menu=menu)
    def copyText(text: str, dummy):
        pyperclip.copy(text)
    def deleteContact(contactIndex: int):
        global root
        cur.execute("DELETE FROM people WHERE id=?", (contactIndex,))
        db.commit()
        root.destroy()
        root = main()
        root.mainloop()
    def editContact(contactIndex: int):
        NewContact(contactIndex)
    if empty == True:
        # adding a label to the root window
        lbl = Label(root, text = "Create some contacts to get started!", font=("TkDefaultFont", 12))
        lbl.grid()
    else:
        rows = cur.execute("SELECT * FROM people")
        rows = rows.fetchall()
        rows.insert(0, columns)
        i = 0
        labels = []
        for j in rows:
            h = 2
            if j != columns:
                edit = Button(root, text='     ✏️', width=2, command=partial(editContact, j[0]))
                edit.grid(row=i, column=0)

                edit = Button(root, text='     🗑️', width=2, command=partial(deleteContact, j[0]))
                edit.grid(row=i, column=1)
            thislbl = []
            for k in j:
                lbl = Label(root, text=k, font=("TkDefaultFont", 12), wraplength=0.25)
                lbl.grid(column=h, row=i)
                if j != columns:
                    thislbl.append(lbl)
                    lbl.bind("<Button-1>", partial(copyText, k))
                h += 1
            if j != columns:
                labels.append(thislbl)
            if i > 0:
                ttk.Separator(root, orient="horizontal").grid(row=i-1, sticky="ew", columnspan=10, padx=0, pady=0)
                ttk.Separator(root, orient="horizontal").grid(row=i+1, sticky="ew", columnspan=10, padx=0, pady=0)
            else:
                pass
            
            i += 2
    return root
# Execute Tkinter

root = main()
root.mainloop()