from django.urls import Resolver404
from src.XmlHandler import XmlHandler
from tkinter import *
from src.GUI.ListDict import ListDict
from src.Query import *
from src.Recommendations import *


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

class Homepage:
    def __init__(self):
        self.root = Tk()

        # Hold dep priority and resolvers of current program
        self.depPriorityDict = {}
        self.resolversDict ={}

        def importMaterials():
            """
            This function will import materials to materialList
            """

            path = self.materialList.widgetDict["pathEntry"].get()

            materials = XmlHandler.parseXmlFiles([path])

            for material in materials:
                if self.materialList.dict.get(material.name) is None:
                    self.materialList.dict[material.name] = material
            
            self.materialList.refreshListbox()

        def selectItemFromMatList():
            """
            Takes selected item from materialList and adds it to selectedMaterials
            """

            for itemIndex in self.materialList.listbox.curselection():
                itemName = self.materialList.listbox.get(itemIndex)
                itemValue = self.materialList.dict[itemName]
                self.selectedMaterials.addItem(itemName,itemValue)

        def openQueryPage():

            queryPage = QueryPage(self)

        def openSettings():
            settingsPage = SettingsPage(self)

        def getRecommendOrder():
            
            recommendedOrder = recommendOrder(list(self.selectedMaterials.dict.values()),list(self.depPriorityDict.values()),list(self.resolversDict.values()))

            self.selectedMaterials.dict = {}

            for material in recommendedOrder:
                self.selectedMaterials.addItem(material.name,material)
            self.selectedMaterials.refreshListbox()

        def getMaterialsWithTags():

            tags = self.materialList.widgetDict["selectTagsEntry"].get().split(",")
            materials = returnMaterialWithTags(self.materialList.dict.values(),tags)
            
            for material in materials:
                self.selectedMaterials.addItem(material.name,material)
            


        self.materialList = ListDict(self.root,0,1)
        self.materialList.initialiseTitle("Material List")
        self.materialList.initialiseLabel("pathWidget","Material file path:")
        self.materialList.initialiseEntry("pathEntry")
        self.materialList.initialiseButton("importMaterials","Import materials",importMaterials)
        self.materialList.initialiseButton("selectMaterials","Select material",selectItemFromMatList)
        self.materialList.initialiseLabel("selectTagsLabel","Select materials with tags:")
        self.materialList.initialiseEntry("selectTagsEntry")
        self.materialList.initialiseButton("selectTagsButton","Select materials with tags",getMaterialsWithTags)
        self.materialList.initialiseDeleteButton()


        self.selectedMaterials = ListDict(self.root,1,1)
        self.selectedMaterials.initialiseTitle("Selected Materials")
        self.selectedMaterials.initialiseButton("queryButton","Query materials",openQueryPage)
        self.selectedMaterials.initialiseButton("recommendOrderButton","Recommend order",getRecommendOrder)
        self.selectedMaterials.initialiseDeleteButton()

        settingsButton = Button(self.root, text = "Settings",command=lambda:openSettings())
        settingsButton.grid(column=0,row=0)

        

        self.root.mainloop()


class QueryPage:
    def __init__(self, homepage : Homepage):
        """
        Opens a window that allows the construction and execution of a query
        """

        root = homepage.root
        masterMaterialList = homepage.materialList
        masterDepLevelList = homepage.depPriorityDict
        masterSelectedMaterials = homepage.selectedMaterials

        def selectItemFromMatList():
            """
            Takes selected item from materialList and adds it to toQueryList
            """

            for itemIndex in materialList.listbox.curselection():
                itemName = materialList.listbox.get(itemIndex)
                itemValue = materialList.dict[itemName]
                toQueryList.addItem(itemName,itemValue)

        

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

            queryResultList.clear()
            
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

        def addDepLevelToClause():
            depLevel = depLevelList.widgetDict["depLevelEntry"].get()
            depLevelList.addItem(depLevel,depLevel)
            depLevelList.refreshListbox()


        queryWindow = Toplevel(root)
        queryWindow.title("Query Material")


        # Creating a list of materials and copying materials from main window
        materialList = ListDict(queryWindow,0,0)
        materialList.initialiseTitle("Material List")
        materialList.initialiseButton("selectButton","Select material",selectItemFromMatList)
        materialList.dict = homepage.materialList.dict
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


        resolversList = ListDict(queryWindow,2,0)
        resolversList.initialiseTitle("Resolvers")
        resolversList.initialiseEntry("resolver")
        resolversList.initialiseButton("addName","Add name",addResolverName)
        resolversList.initialiseButton("addTags","Add tags",addResolverTags)
        resolversList.initialiseDeleteButton()

        def returnQueriedMaterials(returnMaterials):

            if returnMaterials[0] == 0:
                # Adding new materials
                for mat in returnMaterials[1:]:
                    masterSelectedMaterials.addItem(mat.name,mat)
            elif returnMaterials[0] == 1:
                
                # Deleting materials
                for mat in returnMaterials[1:]:
                    del masterSelectedMaterials.dict[mat.name]

            masterSelectedMaterials.refreshListbox()

        def selectNewMaterials():
            """
            Returns all materials in the queryResultList to be selected
            """

            returnQueriedMaterials([0] + list(queryResultList.dict.values())) # item 0 being 0 means the materials will be added
        
        def deleteNewMaterials():
            """
            Returns all materials in the queryResultList to be deleted
            """

            returnQueriedMaterials([1] + list(queryResultList.dict.values())) # item 0 being 1 means the materials will be deleted

        def selectToQuery():
            """
            Takes the query result and adds them to the items to be queried
            """

            matList = list(queryResultList.dict.values())
            
            for mat in matList:
                toQueryList.addItem(mat.name,mat)



        queryResultList = ListDict(queryWindow,3,0)
        queryResultList.initialiseTitle("Result of Query")
        queryResultList.initialiseButton("moveMatsButton","Select new items",selectNewMaterials)
        queryResultList.initialiseButton("deleteMatsButton","Delete new materials",deleteNewMaterials)
        queryResultList.initialiseButton("querySelectMatsButton","Add to query materials", selectToQuery)
        queryResultList.initialiseDeleteButton()

        def copyDepLevelsFromMaster():
            depLevelList.dict = masterDepLevelList.dict.copy()
            depLevelList.refreshListbox()

        depLevelList = ListDict(queryWindow,2,2)
        copyDepLevelsFromMaster() # Making sure it starts with all the dep levels from the master class
        depLevelList.initialiseTitle("Dependency Levels of Query")
        depLevelList.initialiseLabel("entryLabel","Enter dependency level:")
        depLevelList.initialiseEntry("depLevelEntry")
        depLevelList.initialiseButton("addDepLevel","Add dependency level",addDepLevelToClause)
        depLevelList.initialiseDeleteButton()

        # Query constructor Label
        queryConstructorLabel = Label(queryWindow,text="Query Constructor:")
        queryConstructorLabel.grid(column=1,row=1)
        

class SettingsPage():

    def __init__(self,homepage : Homepage):
        root = homepage.root

        recommendWindow = Toplevel(root)
        recommendWindow.title("Settings")

        def addDependencyLevel():
            depList.addItem(depList.widgetDict["depEntry"].get(),depList.widgetDict["depEntry"].get())
            homepage.depPriorityDict = depList.dict.copy()

        def removeDependencyLevel():
            for itemIndex in reversed(depList.listbox.curselection()):
                itemName = depList.listbox.get(itemIndex)
                del depList.dict[itemName]
                depList.listbox.delete(END,itemIndex)
                depList.refreshListbox()
            homepage.depPriorityDict = depList.dict.copy()
            

        def addResolverName():

            resolverEntry = resolversList.widgetDict["resolver"].get()
            resolversList.addItem("Name: "+resolverEntry,resolverEntry)
            resolversList.refreshListbox()
            homepage.resolversDict = resolversList.dict.copy()
        
        def addResolverTags():
            
            resolverEntry = resolversList.widgetDict["resolver"].get()
            resolvers = resolverEntry.split(",")
            resolvers = [None]+resolvers
            resolversList.addItem("Tags: "+resolverEntry,resolvers)
            resolversList.refreshListbox()
            homepage.resolversDict = resolversList.dict.copy()

        def removeResolver():
            for itemIndex in reversed(resolversList.listbox.curselection()):
                itemName = resolversList.listbox.get(itemIndex)
                del resolversList.dict[itemName]
                resolversList.listbox.delete(END,itemIndex)
                resolversList.refreshListbox()
            homepage.resolversDict = depList.dict.copy() 
         

        # Creating a list for dependency priority
        depList = ListDict(recommendWindow,0,1)
        depList.dict = homepage.depPriorityDict.copy() # Copying dependency priority from homepage 
        depList.refreshListbox()
        depList.initialiseTitle("Dependency Priority:")
        depList.initialiseEntry("depEntry")
        depList.initialiseButton("depEntryButton","Add dependency",addDependencyLevel)
        depList.initialiseButton("depDeleteButton","Delete dependency",removeDependencyLevel)

        # Creating a list for resolvers
        resolversList = ListDict(recommendWindow,1,1)
        resolversList.dict = homepage.resolversDict.copy()
        resolversList.refreshListbox()
        resolversList.initialiseTitle("Resolvers")
        resolversList.initialiseEntry("resolver")
        resolversList.initialiseButton("addName","Add name",addResolverName)
        resolversList.initialiseButton("addTags","Add tags",addResolverTags)
        resolversList.initialiseButton("deleteButton","Delete resolver",removeResolver)

