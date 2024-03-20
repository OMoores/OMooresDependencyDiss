from tkinter import *

class ListDict:
    """
    This class is to be used when there is a listbox and a dict that should contain the same items
    
    The class contains method for managing the contents of the listbox and the dict as well as an inbuilt scrollbar
    """

    def __init__(self, root, column : int, row : int):

        # This dict will hold items to be displayed in the listbox
        self.dict = {}
        # This dict will hold any widgets added to this ListDict
        self.widgetDict = {}
        # This frame will hold all widgets relating to this listdict
        # The listbox is at 0,1 in the grid of this frame
        self.frame = Frame(root) 

        # Creating the listbox with a scrollbar
        listboxFrame = Frame(self.frame)
        listboxScrollbar = Scrollbar(listboxFrame, orient=VERTICAL)
        self.listbox = Listbox(listboxFrame, yscrollcommand=listboxScrollbar.set)
        listboxScrollbar.config(command=self.listbox.yview)
        listboxScrollbar.pack(side=RIGHT,fill=Y)
        self.listbox.pack()
        listboxFrame.grid(column=0,row=1)

        # Creating a frame to hold buttons labels and other widgets (operation frame -> For holding things to perform operations)
        self.opFrame = Frame(self.frame)
        self.opFrame.grid(column=1,row=1)

        # Placing the frame in root at the row and column coords provided
        self.frame.grid(column=column,row=row,sticky="W")

    def addItem(self, key : str, value):
        """
        Adds an item to the dict and listbox, if item is already in dict then does not do anything
        """

        if self.dict.get(key) is None:
            self.dict[key] = value

        self.refreshListbox()

    def clear(self):
        self.dict = {}
        self.refreshListbox()



    def refreshListbox(self):
        """
        Refreshes the listbox, deletes all material and readds them
        """
        
        self.listbox.delete(0,END)

        for key in self.dict.keys():
            self.listbox.insert(END,key)

    def initialiseTitle(self,text : str):
        """
        Creates a label at the top of the listbox
        """
        self.widgetDict["topLabel"] = Label(self.frame, text = text)
        self.widgetDict["topLabel"].grid(column=0,row=0)

        

    def initialiseDeleteButton(self):
        """
        Creates a button that deletes the currently selected item in the listbox
        """

        def deleteSelectedItem():

        
            for itemIndex in reversed(self.listbox.curselection()):
                itemName = self.listbox.get(itemIndex)
                del self.dict[itemName]
                self.listbox.delete(END,itemIndex)
                self.refreshListbox()
            

        # If the delete button exists then delete it and create a new one
        self.initialiseButton("deleteButton","Delete item",deleteSelectedItem)

    def initialiseButton(self, name : str, text : str, function):
        """
        Creates a button using the inputted function and name
        If a button with this name already exists deletes it and creates this new button
        """

        if self.widgetDict.get(name) is not None:
            del self.dict[name]
        self.widgetDict[name] = Button(self.opFrame,text=text, command=lambda:function())
        self.widgetDict[name].pack()

    def initialiseEntry(self, name : str):
        """
        Create an entry using the inputed name
        """

        if self.widgetDict.get(name) is not None:
            del self.dict[name]
        self.widgetDict[name] = Entry(self.opFrame)
        self.widgetDict[name].pack()

    def initialiseLabel(self, name : str, text : str):
        """
        Creates a label using the inputed name and text
        """

        if self.widgetDict.get(name) is not None:
            del self.dict[name]
        self.widgetDict[name] = Label(self.opFrame, text=text)
        self.widgetDict[name].pack()

        

    