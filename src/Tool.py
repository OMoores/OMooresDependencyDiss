from msilib.schema import ListBox
from tkinter import *
from src.GUI.EntryButton import *
from src.GUI.ListDict import *
from src.XmlHandler import *
from src.Material import *
from src.Utility import *


def returnMaterialWithTags(materials : [Material], tags : [str]):
    """
    Returns any material provided that has all of the tags given

    Params:
    - materials : A list of materials
    - tags : A list of strings 

    Returns:
    A list of materials with all of the tags provided
    """

    returnMaterials = []

    for material in materials:
        if Utility.isASubsetB(tags,material.tags):
            returnMaterials.append(material)

    return returnMaterials


class Tool:
    """
    This class will contain methods and attributes for using the other functions in this project
    """

    

    def homepage():
        """
        This functions creates a page where you can import materials and select groups of material
        """
        

        root = Tk()

        # Creating a listDict to hold all materials that have been imported
        importedListDict = materialListDict(root, "Delete selected item", "List of imported materials:")
        importedListDict.label.grid(row=2,column=0)
        importedListDict.listboxFrame.grid(row=3,column=0)
        importedListDict.deleteButton.grid(row=4,column=0)

        # Creating an entry form and button to take filepath 
        matImport = MaterialImportEntryButton(Entry(root), Button(root, text = "Import materials from filepath:"))
        matImport.button.config(command=lambda:matImport.importMaterials(importedListDict.dict,importedListDict.refreshListbox)) # When matImports button is clicked then will set matImports input to the value of matImports entry
        matImport.button.grid(row=0,column=0)
        matImport.entry.grid(row=1,column=0)

        # Creating a listDict to hold selected materials from imported materials
        selectedListDict = materialListDict(root,"Delete selected item","List of selected materials:")
        selectedListDict.deleteButton.config(command=lambda:selectedListDict.deleteSelectedItem())
        selectedListDict.label.grid(row=2,column=1)
        selectedListDict.listboxFrame.grid(row=3,column=1)
        selectedListDict.deleteButton.grid(row=4,column=1)
        # Creating a button to select items from importedListDict
        selectedListDict.selectButton = Button(root, text="Select item from imported material", command=lambda:selectedListDict.addItems(importedListDict.getSelectedItems()))
        selectedListDict.selectButton.grid(row=0,column=1)

        # Creating an input and a button that selects materials from imported material list based on their tags
        selectMatsWithTags = EntryButton(Entry(root), Button(root,text="Select materials with tags:"))
        # When the button is clicked adds all imported materials that have the correct tags (from the entry widget)
        selectMatsWithTags.button.config(command=lambda:selectedListDict.addItems(returnMaterialWithTags(importedListDict.dict.values(),selectMatsWithTags.entry.get().split(","))))
        selectMatsWithTags.button.grid(row=0,column=2)
        selectMatsWithTags.entry.grid(row=1,column=2)



        root.mainloop()

        

        

    



Tool.homepage()