from tkinter import *
from src.GUI.ListDict import ListDict

class Tool:
    def homepage():
        root = Tk()
        listdict = ListDict(root,0,0)
        listdict.initialiseDeleteButton()
        listdict.initialiseLabel("listdict")
        listdict.initialiseButton("Button1","button",())
        listdict.initialiseButton("Button2","button",())
        listdict.initialiseButton("Button3","button",())

        root.mainloop()