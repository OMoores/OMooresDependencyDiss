from cProfile import label
from tkinter import *

from numpy import var
from src.Recommendations import recommendOrder
from src.GUI.EntryButton import *
from src.GUI.ListDict import *
from src.XmlHandler import *
from src.Query import *
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
        haveTags = True
        for tag in tags:
            if not material.doesHaveTag(tag):
                haveTags = False
        if haveTags:
            returnMaterials.append(material)

    return returnMaterials


class Tool:
    """
    This class will contain methods and attributes for using the other functions in this project
    """

    dependencyPriority = []
    

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

        # Creating listbox to store recommended order in
        def recOrder():
            """
            Finds the recommended order to learn the set of selected material and puts it in the  resultListbox
            """

            # Clear resultListbox
            resultListbox.delete(0,END)

            # Get all selected materials
            selectedMaterials = []

            for item in selectedListDict.listbox.get(0, END):
                selectedMaterials.append(selectedListDict.dict[item])

            # Find recommended order
            recommendedOrder = recommendOrder(selectedMaterials,depOrderEntry.get().split(","),list(resolversListDict.dict.values()))

            for item in reversed(recommendedOrder): # First item in recommend order is last to be learnt
                resultListbox.insert(END,item.name)


        resultFrame = Frame(root)
        resultScrollbar = Scrollbar(resultFrame, orient=VERTICAL)
        resultListbox = Listbox(resultFrame,yscrollcommand=resultScrollbar.set) 
        resultScrollbar.config(command=resultListbox.yview)
        resultScrollbar.pack(side=RIGHT, fill=Y)
        resultListbox.pack()
        resultFrame.grid(row=3,column=2)
        recommendOrderButton = Button(root, text="Recommend order to learn selected material", command=lambda:recOrder())
        recommendOrderButton.grid(row=2,column=2)

        def queryMats():
            """
            Querys currently selected materials and puts them in the output box
            """

            resultListbox.delete(0,END)

            selectedMaterials = []

            for item in selectedListDict.listbox.get(0, END):
                selectedMaterials.append(selectedListDict.dict[item])

            # for queryIndex in reversed(queryListDict.listbox.curselection()):
            #     print(queryIndex)

            queryIndex = queryListDict.listbox.curselection()[0]
            getName = queryListDict.listbox.get(queryIndex)
            
            query = queryListDict.dict[getName]

            queriedMaterials = queryDependencies(selectedMaterials,query,list(resolversListDict.dict.values()))

            for item in queriedMaterials:
                resultListbox.insert(END,item.name)

        queryMaterialsButton = Button(root,text="Query selected materials",command=lambda:queryMats())
        queryMaterialsButton.grid(row=4,column=2)

        # Entry field for dep order
        depOrderEntry = Entry(root)
        depOrderLabel = Label(root, text="Priority of dependencies:")
        depOrderLabel.grid(row=0,column=3) 
        depOrderEntry.grid(row=1,column=3) 

        def addResolverName():
            """
            Adds the name of a material to the resolver and refreshes listbox
            """

            unformattedName = resolversListDict.entry.get()

            if resolversListDict.dict.get(unformattedName) is None:
                resolversListDict.dict[unformattedName] = [unformattedName]

            resolversListDict.refreshListbox()

        def addResolverTags():
            """
            Adds tags to the resolver and refreshes listbox 
            """

            unformattedTags = resolversListDict.entry.get()
            
            if resolversListDict.dict.get(unformattedTags) is None:
                resolversListDict.dict[unformattedTags] = [None] + [tag for tag in unformattedTags.split(",")]

            resolversListDict.refreshListbox()



        # listDict to hold resolvers
        resolversListDict = listDict(root,deleteText="Delete selected resolver", labelText = "Resolvers:")
        resolversListDict.listboxFrame.grid(row=3,column=3)
        resolversListDict.label.grid(row=2,column=3)
        resolversListDict.entry = Entry(root)
        resolversListDict.entryLabel = Label(root, text="Enter name or tags for resolver:")
        resolversListDict.addMaterialNameButton = Button(root,text="Add material name", command=lambda:addResolverName())
        resolversListDict.addMaterialTagsButton = Button(root,text="Add material tags", command=lambda:addResolverTags())
        resolversListDict.deleteButton.grid(row=4,column=3)
        resolversListDict.entryLabel.grid(row=5,column=3)
        resolversListDict.entry.grid(row=6,column=3)
        resolversListDict.addMaterialNameButton.grid(row=7, column=3)
        resolversListDict.addMaterialTagsButton.grid(row=8,column=3)

        # ----- QUERY CONSTRUCTOR ----- #
        def openQueryConstructor():
            """
            Opens the query constructor window
            """

            # Creating a new window
            queryConstructorWindow = Toplevel(root)
            queryConstructorWindow.title("Query Constructor")

            def addQuery():
                """
                Adds the query constructed to the current list of queries in the main window and shuts this window
                """
                query = Query()
                query.addClauses(list(clauseListDict.dict.values()))
                queryName = clauseListDict.queryNameEntry.get()

                queryListDict.addItem(queryName,query)
                queryListDict.refreshListbox()

                queryConstructorWindow.destroy() # Shuts the window

            # Creating a listbox to hold each clause created
            clauseListDict = listDict(queryConstructorWindow,deleteText="Delete clause",labelText="Clauses in current query:")
            clauseListDict.label.grid(row=0,column=0)
            clauseListDict.listboxFrame.grid(row=1,column=0)
            clauseListDict.deleteButton.grid(row=2,column=0)
            clauseListDict.useQuery = Button(queryConstructorWindow, text="Create query", command=lambda:addQuery())
            clauseListDict.queryLabel = Label(queryConstructorWindow,text="Name of query:")
            clauseListDict.queryNameEntry = Entry(queryConstructorWindow)
            clauseListDict.queryLabel.grid(row=3,column=0)
            clauseListDict.queryNameEntry.grid(row=4,column=0)
            clauseListDict.useQuery.grid(row=5,column=0)
            

            def addVar():
                """
                Adds a variable to the lists of variables to be added to the current clause
                """

                varName = varListDict.varNameEntry.get()
                var = varListDict.varEntry.get().split(",")

                varListDict.addItem(varName,var)
                varListDict.refreshListbox()


            def addClause():
                """
                Adds a clause to the list of clauses to be added to the current query
                """ 
                clause = Clause()
                # Creating the new clause
                clause.addVariables(list(varListDict.dict.values()))
                depLevels = varListDict.depLevelEntry.get().split(",")
                clause.addDependencyLevels(depLevels)

                clauseName = nameClauseEntry.get()

                clauseListDict.addItem(clauseName,clause)
                clauseListDict.refreshListbox()

    

            # Creating a listbox to hold each var created for a clause
            varListDict = listDict(queryConstructorWindow, deleteText="Delete variable",labelText="Variables in new clause")
            varListDict.varEntry = Entry(queryConstructorWindow)
            varListDict.depLevelEntry = Entry(queryConstructorWindow)
            varListDict.depLevelLabel = Label(queryConstructorWindow,text="Dependency levels for variable")
            varListDict.addVarButton = Button(queryConstructorWindow, text="Add variable to clause",command=lambda:addVar())
            varListDict.varNameLabel = Label(queryConstructorWindow,text="Name of variable:")
            varListDict.varNameEntry = Entry(queryConstructorWindow)
            varListDict.listboxFrame.grid(row=1,column=1)
            varListDict.label.grid(row=0,column=1)
            varListDict.deleteButton.grid(row=2,column=1)
            varListDict.varEntry.grid(row=4,column=1)
            varListDict.addVarButton.grid(row=3,column=1)
            varListDict.depLevelLabel.grid(row=5,column=1)
            varListDict.depLevelEntry.grid(row=6,column=1)
            varListDict.varNameLabel.grid(row=7,column=1)
            varListDict.varNameEntry.grid(row=8,column=1)


            # Creating widgets to save clause and name it
            addClauseButton = Button(queryConstructorWindow, text="Create new clause", command=lambda:addClause())       
            addClauseButton.grid(row=2,column=2) 
            nameClauseLabel = Label(queryConstructorWindow,text="Name of clause:")
            nameClauseLabel.grid(row=3,column=2)
            nameClauseEntry = Entry(queryConstructorWindow)
            nameClauseEntry.grid(row=4,column=2)


        queryListDict = listDict(root,"Delete selected query","Queries:")
        queryListDict.listboxFrame.grid(row=3,column=4)
        queryListDict.label.grid(row=2,column=4)
        queryListDict.deleteButton.grid(row=4,column=4)
        queryListDict.createQueryButton = Button(root,text="Open query constructor",command=lambda:openQueryConstructor())
        queryListDict.createQueryButton.grid(row=0,column=4)




        root.mainloop()

        

        

    



Tool.homepage()