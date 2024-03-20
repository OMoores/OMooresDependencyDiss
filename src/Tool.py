from winreg import QueryReflectionKey
from src.XmlHandler import XmlHandler
from tkinter import *
from src.GUI.ListDict import ListDict
from src.Query import *

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

        def addDepLevelToClause():
            depLevel = depLevelList.widgetDict["depLevelEntry"].get()
            depLevelList.addItem(depLevel,depLevel)
            depLevelList.refreshListbox()

        def addVarToClause():
            varName = varList.widgetDict["varName"].get()
            varValue = varList.widgetDict["varEntry"].get().split(",")

            varList.addItem(varName,varValue)
            varList.refreshListbox()

        def addClauseToQuery():
            clauseName = clauseList.widgetDict["clauseName"].get()
            varValues = list(varList.dict.values())
            clause = Clause()       

            clause.addDependencyLevels(list(depLevelList.dict.values()))

            for var in varValues:    
                clause.addVariable(var)
            
            clauseList.addItem(clauseName,clause)
            clauseList.refreshListbox()
            varList.clear()

        def queryMaterials():
            
            materials = list(toQueryList.dict.values())

            # Create query
            query = Query()
            for clause in list(clauseList.dict.values()):
                query.addClause(clause)

            queryResult = queryDependencies(materials,query)

            for material in queryResult:
                queryResultList.addItem(material.name,material)
            
            queryResultList.refreshListbox()

        def addResolverName():

            resolverEntry = resolversList.widgetDict["resolver"].get()
            resolversList.addItem("Name: "+resolverEntry,[resolverEntry])
            resolversList.refreshListbox()
        
        def addResolverTags():
            
            resolverEntry = resolversList.widgetDict["resolver"].get()
            resolvers = resolverEntry.split(",")
            resolvers = [None]+resolvers
            resolversList.addItem("Tags: "+resolverEntry,[resolvers])
            resolversList.refreshListbox()


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
        toQueryList.initialiseButton("queryButton","Query materials",queryMaterials)
        toQueryList.initialiseDeleteButton()

        clauseList = ListDict(queryWindow,0,2)
        clauseList.initialiseTitle("Clauses in Query")
        clauseList.initialiseLabel("nameLabel","Enter clause name:")
        clauseList.initialiseEntry("clauseName")
        clauseList.initialiseButton("addClauses","Add clause",addClauseToQuery)
        clauseList.initialiseDeleteButton()

        varList = ListDict(queryWindow,1,2)
        varList.initialiseTitle("Variables in Clause")
        varList.initialiseLabel("nameLabel","Enter variable name:")
        varList.initialiseEntry("varName")
        varList.initialiseLabel("entryLabel","Enter variable:")
        varList.initialiseEntry("varEntry")
        varList.initialiseButton("addVar","Add variable",addVarToClause)
        varList.initialiseDeleteButton()

        depLevelList = ListDict(queryWindow,2,2)
        depLevelList.initialiseTitle("Dependency Levels of Clause")
        depLevelList.initialiseLabel("entryLabel","Enter dependency level:")
        depLevelList.initialiseEntry("depLevelEntry")
        depLevelList.initialiseButton("addDepLevel","Add dependency level",addDepLevelToClause)
        depLevelList.initialiseDeleteButton()

        resolversList = ListDict(queryWindow,2,0)
        resolversList.initialiseTitle("Resolvers")
        resolversList.initialiseEntry("resolver")
        resolversList.initialiseButton("addName","Add name",addResolverName)
        resolversList.initialiseButton("addTags","Add tags",addResolverTags)
        resolversList.initialiseDeleteButton()

        def selectNewMaterials():
            """
            Returns all materials in the queryResultList to be selected
            """

            return [0] + list(queryResultList.dict.values()) # item 0 being 0 means the materials will be added
        
        def deleteNewMaterials():
            """
            Returns all materials in the queryResultList to be deleted
            """

            return [1] + list(queryResultList.dict.values()) # item 0 being 1 means the materials will be deleted

        def selectToQuery():
            """
            Takes the query result and adds them to the items to be queried
            """

            matList = list(queryResultList.dict.values())
            
            for mat in matList:
                toQueryList.addItem(mat.name,mat)

            matList.refreshListbox()


        queryResultList = ListDict(queryWindow,3,0)
        queryResultList.initialiseTitle("Result of Query")
        queryResultList.initialiseButton("moveMatsButton","Select new items",selectNewMaterials)
        queryResultList.initialiseButton("deleteMatsButton","Delete new materials",deleteNewMaterials)
        queryResultList.initialiseButton("querySelectMatsButton","Add to query materials", selectToQuery)
        queryResultList.initialiseDeleteButton()

        # Query constructor Label
        queryConstructorLabel = Label(queryWindow,text="Query Constructor:")
        queryConstructorLabel.grid(column=1,row=1)
        






    
