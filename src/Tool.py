from msilib.schema import ListBox
from tkinter import *
from src.XmlHandler import *
from src.Material import Material
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

    materials = {}
    selectedMaterials = {}

    
        

    def homepage():
        """
        This function is called to start the window that opens when the program is run
        """


        def getMatImportPath():
            """
            Gets the value currently entered into the entry widget matImportPathButton
            """

            return matImportPathEntry.get()
        
        def listMaterials():
            """
            Updates matListbox to contain all materials in Tool.materials
            """

            matListbox.delete(0,END)

            for mat in Tool.materials.keys():
                matListbox.insert(END,mat)
            
        def importMaterials(path : str):
            """
            Takes a path and imports materials from that path and updating the materials class variable with new imported materials. Does not overwrite any materials that have already been imported,
            if any materials with the same name are imported they will be disgarded
            """
            newMaterials = XmlHandler.parseXmlFiles([path])

            for mat in newMaterials:
                if Tool.materials.get(mat.name) is None:
                    Tool.materials[mat.name] = mat

            listMaterials()

        def deleteCurrentMaterial():
            """
            Deletes a seleceted item from matList and deletes the same item from the materials dict
            Also deletes it from selectedMatList
            """
            for item in reversed(matListbox.curselection()):
                itemName = matListbox.get(item)

                # Deleting from selectedMatListbox and selectedMaterials if present
                if Tool.selectedMaterials.get(itemName) is not None:
                    del Tool.selectedMaterials[itemName]
                    listSelectedMaterials()
                    
                # Deleting from matListBox and materials
                del Tool.materials[itemName]
                matListbox.delete(item)

            

        def selectCurrentMaterial():
            """
            Adds the currently selected material to the list and dict of selected materials.
            If the material has already been added then does nothing
            """

            selectedItemIndex = matListbox.curselection()
            selectedItemName = matListbox.get(selectedItemIndex)
            selectedItem = Tool.materials[selectedItemName]

            if Tool.selectedMaterials.get(selectedItemName) is None:
                Tool.selectedMaterials[selectedItemName] = selectedItem

            listSelectedMaterials()

        def listSelectedMaterials():
            """
            Updates selectedMatListBox to contain all materials in selectedMaterials dict
            """

            selectedMatListbox.delete(0,END)

            for mat in Tool.selectedMaterials.keys():
                selectedMatListbox.insert(END,mat)

        def selectMaterials(materials : [Material]):
            """
            Adds the given materials to the selectedMaterial dict and selectedMatListBox if they are not already present
            """

            for material in materials:
                if Tool.selectedMaterials.get(material.name) is None:
                    Tool.selectedMaterials[material.name] = material

            listSelectedMaterials()     

        def getTagList():
            """
            Gets the list of tags in selectTagsEntry and returns them in a list of strings
            """           

            return selectTagsEntry.get()

        def getTags():
            tagList = getTagList()

            returnTags = tagList.split(",")

            return returnTags

        


        

        root = Tk()

        # Creating an entry form to take filepath 
        matImportPathEntry = Entry(root)
        matImportPathEntry.grid(row=0,column=0)

        # Creating button to import materials from filepath
        matImportButton = Button(root, text="Import materials from files", command = lambda : importMaterials(getMatImportPath()))
        matImportButton.grid(row=1,column=0)

        # Creating list of material -> Frame, listbox and scrollbar
        matListFrame = Frame(root)
        matListScrollbar = Scrollbar(matListFrame, orient=VERTICAL)
        matListbox = Listbox(matListFrame, yscrollcommand=matListScrollbar.set)
        matListScrollbar.config(command=matListbox.yview)
        matListScrollbar.pack(side=RIGHT, fill=Y)
        matListFrame.grid(row=2,column=0)
        matListbox.pack()

        # Button to select currently selected materials
        selectMatButton = Button(root, text = "Select material",command = lambda: selectCurrentMaterial())
        selectMatButton.grid(row=3,column=0)

        # Button to delete currently selected material
        deleteMatButton = Button(root, text = "Delete material",command = lambda: deleteCurrentMaterial())
        deleteMatButton.grid(row=4,column=0)

        # Creating an entry form to take tags of materials to be selected
        selectTagsEntry = Entry(root)
        selectTagsEntry.grid(row=0,column=1)

        # Creating a button to select materials with the tags from selectTagsEntry
        selectTagsButton = Button(root, text="Select materials with tags")
        selectTagsButton.grid(row=1,column=1)

        # Creating list of materials that have been selected
        selectedMatListFrame = Frame(root)
        selectedMatListScrollbar = Scrollbar(selectedMatListFrame, orient=VERTICAL)
        selectedMatListbox = Listbox(selectedMatListFrame, yscrollcommand=selectedMatListScrollbar.set)
        selectedMatListScrollbar.config(command=selectedMatListbox.yview)
        selectedMatListScrollbar.pack(side=RIGHT, fill=Y)
        selectedMatListFrame.grid(row=2,column=1)
        selectedMatListbox.pack()


        root.mainloop()

        

        

    



Tool.homepage()