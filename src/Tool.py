from src.XmlHandler import XmlHandler
from tkinter import *
from src.GUI.ListDict import ListDict

class Tool:
    def homepage():
        root = Tk()

        def importMaterials():
            """
            This function will import materials to materialList
            """

            path = materialList.widgetDict["pathEntry"].get()

            materials = XmlHandler.parseXmlFiles([path])

            for material in materials:
                if materialList.dict.get(material.name) is None:
                    materialList.dict[material.name] = material
            
            materialList.refreshListbox()

        def selectItemFromMatList():
            """
            Takes selected item from materialList and adds it to selectedMaterials
            """

            for itemIndex in materialList.listbox.curselection():
                itemName = materialList.listbox.get(itemIndex)
                itemValue = materialList.dict[itemName]
                selectedMaterials.addItem(itemName,itemValue)

        def openQueryPage():

            Tool.queryPage(root,materialList.dict)

            


        materialList = ListDict(root,0,0)
        materialList.initialiseTitle("Material List")
        materialList.initialiseLabel("pathWidget","Material file path:")
        materialList.initialiseEntry("pathEntry")
        materialList.initialiseButton("importMaterials","Import materials",importMaterials)
        materialList.initialiseButton("selectMaterials","Select material",selectItemFromMatList)
        materialList.initialiseDeleteButton()


        selectedMaterials = ListDict(root,1,0)
        selectedMaterials.initialiseTitle("Selected Materials")
        selectedMaterials.initialiseButton("queryButton","Query materials",openQueryPage)
        selectedMaterials.initialiseButton("recommendOrderButton","Recommend order",())
        selectedMaterials.initialiseDeleteButton()
        

        root.mainloop()


    def queryPage(root, materialDict):
        """
        Opens a window that allows the construction and execution of a query
        """

        def selectItemFromMatList():
            """
            Takes selected item from materialList and adds it to toQueryList
            """

            for itemIndex in materialList.listbox.curselection():
                itemName = materialList.listbox.get(itemIndex)
                itemValue = materialList.dict[itemName]
                toQueryList.addItem(itemName,itemValue)


        queryWindow = Toplevel(root)
        queryWindow.title("Query Material")


        # Creating a list of materials and copying materials from main window
        materialList = ListDict(queryWindow,0,0)
        materialList.initialiseTitle("Material List")
        materialList.initialiseButton("selectButton","Select material",selectItemFromMatList)
        materialList.dict = materialDict
        materialList.refreshListbox()


        toQueryList = ListDict(queryWindow,1,0)
        toQueryList.initialiseTitle("Materials Being Queried")
        toQueryList.initialiseDeleteButton()






    
