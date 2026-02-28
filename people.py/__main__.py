# This follows the GeeksForGeeks tutorial here: https://www.geeksforgeeks.org/python/create-first-gui-application-using-python-tkinter/
from tkinter import *


root = Tk()
def NewContact():
    newContactWindow = Tk()
    newContactWindow.title("Create new Contact")
    # Set geometry(widthxheight)
    newContactWindow.geometry('350x200')

    lbl2 = Label(newContactWindow, text = "Placeholder text broo")
    lbl2.grid()
    
    btn = Button(newContactWindow, text = "Exit" ,
             fg = "red", command=newContactWindow.destroy)
    btn.grid(column=2, row=0)
    newContactWindow.mainloop()

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

# Execute Tkinter
root.mainloop()