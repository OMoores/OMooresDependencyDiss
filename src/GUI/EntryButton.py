from tkinter import *
from src.Material import Material
from src.XmlHandler import XmlHandler


class EntryButton():
    """
    This class is used when there is an entry widget. It holds the entry widget and a button
    """

    def __init__(self, entry : Entry, button : Button):
        self.entry = entry
        self.button = button

class MaterialImportEntryButton(EntryButton):
    """
    An extension of the EntryButton class that is used specifically to import materials using an entry that takes a filepath
    """
    def importMaterials(self, dict : {}, func):
        """
        Used when the button is clicked, sets the dictionary passed to the function to materials from imported 
        xml file. If a material with a name is already in the dict another with this name will not be added

        Then it runs a function that should update anything that needs the new materials

        Params:
        - dict : A dictionary
        - func : A function
        """

        path = self.entry.get()

        materials = XmlHandler.parseXmlFiles([path])

        # Look through material and add to dict if not already present
        for material in materials:
            if dict.get(material.name) is None:
                dict[material.name] = material

        func()
        
