from msilib.schema import ListBox
from tkinter import *
from src.XmlHandler import *
from src.Material import Material

class Tool:
    """
    This class will contain methods and attributes for using the other functions in this project
    """

    materials = {}

    
        

    def homepage():
        """
        This function is called to start the window that opens when the program is run
        """


        def getMatImportPath():
            """
            Gets the value currently entered into the entry widget matImportPathButton
            """

            return matImportPathButton.get()
        
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

        


        

        root = Tk()

        # Creating an entry form to take filepath 
        matImportPathButton = Entry(root)
        matImportPathButton.grid(row=0,column=0)

        # Creating button to import materials from filepath
        matImportButton = Button(root, text="Import materials from files", command = lambda : importMaterials(getMatImportPath())).grid(row=1,column=0)

        # Creating list of material -> Frame and scrollbar
        matListFrame = Frame(root)
        matListScrollbar = Scrollbar(matListFrame, orient=VERTICAL)
        matListbox = Listbox(matListFrame, yscrollcommand=matListScrollbar.set)
        matListScrollbar.config(command=matListbox.yview)
        matListScrollbar.pack(side=RIGHT, fill=Y)
        
        matListFrame.grid(row=2,column=0)
        matListbox.pack()






        root.mainloop()

        

        

    



Tool.homepage()