from tkinter import *
from src.Material import Material

class listDict:
    """
    This class is to be used when there is a listbox and a dict that should contain the same items
    
    Can have a button to delete materials
    """

    def __init__(self, root, deleteText : str = None, labelText = None):
        self.dict = {}
        
        self.label = Label(root, text = labelText)
        self.deleteButton = Button(text=deleteText)

        # Setting up the frame and scrollbar for listbox
        self.listboxFrame = Frame(root) # Holds the listbox and the scrollbar
        scrollbar = Scrollbar(self.listboxFrame, orient=VERTICAL)
        self.listbox = Listbox(self.listboxFrame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.listbox.pack()


        

      


    def refreshListbox(self):
        """
        Refreshes the listbox, deletes all material and readds them
        """
        
        self.listbox.delete(0,END)

        for key in self.dict.keys():
            self.listbox.insert(END,key)

    def deleteSelectedItem(self):
        """
        Deletes an item from the dict and listbox
        """
        ...

    def getSelectedItems(self):
        """
        Returns the item the user is currently selecting
        """

        selected = self.listbox.curselection()
        items = []

        for index in selected:
            items.append(self.dict[self.listbox.get(index)])



        return items
    
    


        

    
        
class materialListDict(listDict):
    """
    A listDict specifically made to hold materials.
    After items are added refreshes the listbox so items will be displayed
    """

    def addItems(self,materials : [Material]):

        for material in materials:
            if not self.addItem(material):
                Exception()

        self.refreshListbox()


    def addItem(self,material : Material) -> bool:
        """
        Adds a material, the name is added to the end of the listbox and the name is used as a key for the dict where the material is the value
        If the item is already present in the dict nothing happens

        Param:
        - material : The material to be added

        Returns:
        A bool signifying if the item was sucessfully added, returns false if it wasnt or if it was already present
        """

        try:
            if self.dict.get(material.name) is None:
                self.dict[material.name] = material

            return True
        except:
            return False
        
    def deleteSelectedItem(self) -> bool:
        """
        Deletes the material currently selected by the user

        Returns:
        A bool signifying if the item was sucessfully deleted
        """

        try:
            # Looks through all selected items backwards and removes them from dict and listbox
            # Has to be backward or will mess up for loop
            for itemIndex in reversed(self.listbox.curselection()):
                itemName = self.listbox.get(itemIndex)
                del self.dict[itemName]
                self.listbox.delete(itemIndex)
            
            return True

        except:
            return False
