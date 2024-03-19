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
        self.frame.grid(column=column,row=row)

    def initialiseLabel(self,text : str):
        """
        Creates a label at the top of the listbox
        """
        self.widgetDict["topLabel"] = Label(self.frame, text = text)
        self.widgetDict["topLabel"].grid(column=0,row=0)

        

    def initialiseDeleteButton(self):
        """
        Creates a button that deletes the currently selected item in the listbox
        """

        def deleteSelectedItem(self):
            try:
                for itemIndex in reversed(self.listbox.curselection()):
                    itemName = self.listbox.get(itemIndex)
                    del self.dict[itemName]
                    self.listbox.delete(itemIndex)
            except:
                ...

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



        

    