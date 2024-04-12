from src.XmlHandler import XmlHandler
from tkinter import *
from src.GUI.ListDict import ListDict
from src.GUI.Operation import Operation
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


        def getRecommendOrder():

            def recommendOrderFunc():
                recommendedOrder = recommendOrder(list(self.selectedMaterials.dict.values()),list(self.depPriorityDict.values()),list(self.resolversDict.values()))

                self.selectedMaterials.dict = {}

                for material in recommendedOrder:
                    self.selectedMaterials.addItem(material.name,material)
                self.selectedMaterials.refreshListbox()

            settingsPage = SettingsPage(self, recommendOrderFunc)
            
            

        def getMaterialsWithTags():

            tags = self.materialList.widgetDict["selectTagsEntry"].get().split(",")
            materials = returnMaterialWithTags(self.materialList.dict.values(),tags)
            
            for material in materials:
                self.selectedMaterials.addItem(material.name,material)

        def clearQueriedMaterials():

            self.selectedMaterials.clear()

            


        self.materialList = ListDict(self.root,0,1)
        self.materialList.initialiseTitle("Material List")
        self.materialList.initialiseLabel("pathWidget","Material file path:")
        self.materialList.initialiseEntry("pathEntry")
        self.materialList.initialiseButton("importMaterials","Import materials",self.importMaterials)
        self.materialList.initialiseButton("selectMaterials","Select material",selectItemFromMatList)
        self.materialList.initialiseLabel("selectTagsLabel","Select materials with tags:")
        self.materialList.initialiseEntry("selectTagsEntry")
        self.materialList.initialiseButton("selectTagsButton","Select materials with tags",getMaterialsWithTags)
        self.materialList.initialiseDeleteButton()


        self.selectedMaterials = ListDict(self.root,1,1)
        self.selectedMaterials.initialiseTitle("Selected Materials")
        self.selectedMaterials.initialiseButton("queryButton","Query materials",openQueryPage)
        self.selectedMaterials.initialiseButton("recommendOrderButton","Recommend order",getRecommendOrder)
        self.selectedMaterials.initialiseButton("clear","Clear selected materials",clearQueriedMaterials)
        self.selectedMaterials.initialiseDeleteButton()

        def selectedMaterialDependencies():
            """
            Takes the currently selected material in the selectedMaterials listDict and makes depListDict show the materials dependencies
            """
            
            # Clear previous content of listdict
            depListDict.clear()

            # Find selected material
            selectedMaterialIndex = self.selectedMaterials.listbox.curselection()[0]
            selectedMaterialName = self.selectedMaterials.listbox.get(selectedMaterialIndex)
            selectedMaterial = self.selectedMaterials.dict[selectedMaterialName]

            # Display dependencies
            dependencies = selectedMaterial.dependencies

            for dependency in dependencies:
                # Display each dependency
                depListDict.dict[Utility.turnMatDepIntoText(dependency)] = dependency

            # Setting title
            title = selectedMaterial.name + " dependencies"

            depListDict.widgetDict["topLabel"].config(text=title)


            depListDict.refreshListbox()

        def showOrDependencies():
            """
            Displays the OR dependencies of all selected mateirals in depListDict
            """
            
            depListDict.clear()

            # Gets all selected materials
            selectedMaterials = list(self.selectedMaterials.dict.values())

            # Getting each materials dependencies that have ORs in them
            for orMaterial in selectedMaterials:
                orDependencies = findOrDependencies(orMaterial)


                # Writing each dependency to depListDict
                for orStr in orDependencies:

                    orStr = orMaterial.name + " " + orStr
                    depListDict.addItem(orStr, orMaterial)
        
            # Setting title
            depListDict.widgetDict["topLabel"].config(text="All OR dependencies")
                    
        
        # A list that displays a materials dependencies
        depListDict = ListDict(self.root,3,1)
        depListDict.initialiseTitle("Material dependencies")
        depListDict.initialiseButton("showDepSelectedMat","Selected material",selectedMaterialDependencies)
        depListDict.initialiseButton("showOrDeps","OR dependencies",showOrDependencies)

        def selectedMaterialTags():
            """
            Displays the tags of the selected material in tagsListDict
            """

            tagsListDict.clear()

            # Find selected material
            selectedMaterialIndex = self.selectedMaterials.listbox.curselection()[0]
            selectedMaterialName = self.selectedMaterials.listbox.get(selectedMaterialIndex)
            selectedMaterial = self.selectedMaterials.dict[selectedMaterialName]

            for tag in selectedMaterial.tags:
                tagsListDict.addItem(tag,tag)

            # Setting title of tagsListDict to show what material is being looked at
            title = selectedMaterial.name + " tags"
            tagsListDict.widgetDict["topLabel"].config(text=title)

            tagsListDict.refreshListbox()


        tagsListDict = ListDict(self.root,4,1)
        tagsListDict.initialiseTitle("Material tags")
        tagsListDict.initialiseButton("showTagsSelectedMat","Selected material",selectedMaterialTags)

        def openMaterialConstructor(homepage):

            constructor = MaterialConstructor(homepage)

        optionsFrame = Frame(self.root)
        constructorButton = Button(optionsFrame, text = "Material constructor",command=lambda:openMaterialConstructor(self))
        optionsFrame.grid(column=0,row=0)
        constructorButton.grid(column=1,row=0)

        

        self.root.mainloop()

    def importMaterials(self):
            """
            This function will import materials to materialList
            """

            paths = self.materialList.widgetDict["pathEntry"].get()
            paths = paths.split(",")

            materials = XmlHandler.parseXmlFiles(paths)

            for material in materials:
                if self.materialList.dict.get(material.name) is None:
                    self.materialList.dict[material.name] = material
            
            self.materialList.refreshListbox()

    def importTemp(self):

        path = "temp.xml"

        materials = XmlHandler.parseXmlFiles([path])

        for material in materials:
            if self.materialList.dict.get(material.name) is None:
                self.materialList.dict[material.name] = material
        
        self.materialList.refreshListbox()



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
            resolvers = getResolvers()

            # Create query
            query = Query()
            for clause in list(clauseList.dict.values()):
                query.addClause(clause)

            queryResult = queryDependencies(materials,query,resolvers)

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
            resolversList.addItem("Tags: "+resolverEntry,resolvers)
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

        def getResolvers():

            return list(resolversList.dict.values())



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
            depLevelList.dict = masterDepLevelList.copy()
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
    """
    A settings page opened before materials are queried, recommendOrderFunc is the function that recommendsOrder and sets materials in homepage
    """

    def __init__(self,homepage : Homepage, recommendOrderFunc):
        root = homepage.root

        self.recommendWindow = Toplevel(root)
        self.recommendWindow.title("Settings")

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
        depList = ListDict(self.recommendWindow,0,1)
        depList.dict = homepage.depPriorityDict.copy() # Copying dependency priority from homepage 
        depList.refreshListbox()
        depList.initialiseTitle("Dependency Priority:")
        depList.initialiseEntry("depEntry")
        depList.initialiseButton("depEntryButton","Add dependency",addDependencyLevel)
        depList.initialiseButton("depDeleteButton","Delete dependency",removeDependencyLevel)

        # Creating a list for resolvers
        resolversList = ListDict(self.recommendWindow,1,1)
        resolversList.dict = homepage.resolversDict.copy()
        resolversList.refreshListbox()
        resolversList.initialiseTitle("Resolvers")
        resolversList.initialiseEntry("resolver")
        resolversList.initialiseButton("addName","Add name",addResolverName)
        resolversList.initialiseButton("addTags","Add tags",addResolverTags)
        resolversList.initialiseButton("deleteButton","Delete resolver",removeResolver)

        def recOrderButtonFunc():
            try:
                recommendOrderFunc()
            except:
                ...
            self.recommendWindow.destroy()


        # Creating button to query materials
        queryButton = Button(self.recommendWindow,text="Recommend order", command=recOrderButtonFunc)
        queryButton.grid(row=0,column=2)

class MaterialConstructor:
    
    def __init__(self, homepage : Homepage): 
        """
        A window for creating materials. Materials in this window do not have proper dependencies until they are created and set to a file or sent to the main window. They have tempDeps filled in with strings representing material name
        """
    

        self.selectedMaterial : Material = None

        def createMaterial():
            """
            Creates an empty material and selects it
            """

            materialName = self.newMaterialList.widgetDict["materialNameEntry"].get()

            self.newMaterialList.addItem(materialName,Material(materialName))

            self.selectedMaterial = self.newMaterialList.dict[materialName]
            
            self.refreshWindow()

        def selectMaterial():
            """
            Gets the current material selected and puts its dependencies and tags in the dep and tag list,
            Whenever tags and deps are added they are added to the most recently selected material
            """
            # If cannot select a material selectedMaterial is set to None
            try:
                # Selecting the material
                selectedMaterialIndex = self.newMaterialList.listbox.curselection()[0]
                selectedMaterialName = self.newMaterialList.listbox.get(selectedMaterialIndex)
                self.selectedMaterial = self.newMaterialList.dict[selectedMaterialName]

                displayMaterial(self.selectedMaterial)
                
            except:
                self.selectedMaterial = None

        def displayMaterial(selectedMaterial : Material):
            """
            Takes a material and displays the materials deps and tags
            """

            self.selectedMaterial = selectedMaterial
            self.refreshWindow()

            

        def deleteMaterial():

            for itemIndex in reversed(self.newMaterialList.listbox.curselection()):
                itemName = self.newMaterialList.listbox.get(itemIndex)
                del self.newMaterialList.dict[itemName]
                self.newMaterialList.listbox.delete(END,itemIndex)
                self.newMaterialList.refreshListbox()

            self.materialDepsList.clear()
            self.materialTagsList.clear()

            
        self.root = Toplevel(homepage.root)        
        self.root.title("Material constructor")

        topFrame = Frame(self.root)
        addMaterialButton = Button(topFrame,text="Add materials",command=lambda:self.addMaterialsToHomepage(homepage)) 
        self.filenameEntry = Entry(topFrame)
        fileCreateButton = Button(topFrame,text="Create file:",command=lambda:self.createFile())   
        addMaterialButton.grid(column=0,row=0)
        fileCreateButton.grid(column=1,row=0)
        self.filenameEntry.grid(column=2,row=0)
        topFrame.grid(column=0,row=0)

        self.newMaterialList = ListDict(self.root,0,1)
        self.newMaterialList.initialiseTitle("Materials")
        self.newMaterialList.initialiseLabel("materialNameLabel","Material name")
        self.newMaterialList.initialiseEntry("materialNameEntry")
        self.newMaterialList.initialiseButton("createMaterialButton","Create material",createMaterial)
        self.newMaterialList.initialiseButton("selectMaterialButton","Select material",selectMaterial)
        self.newMaterialList.initialiseButton("deleteMaterialButton","Delete material",deleteMaterial)

        def openDependencyConstructor():
            constructor = DependencyConstructor(self)

        self.materialDepsList = ListDict(self.root,1,1)
        self.materialDepsList.initialiseTitle("Dependencies of selected material")
        self.materialDepsList.initialiseButton("depCreatorButton","Create dependency",openDependencyConstructor)
        self.materialDepsList.initialiseDeleteButton()

        def addTag():
            """
            Adds tag to currently selected material
            """
            self.selectedMaterial.addTags([self.materialTagsList.widgetDict["tagEntry"].get()]) 
            self.refreshWindow()

        def deleteTags():
            selectedTag = self.materialTagsList.listbox.curselection()
            tagName = self.materialTagsList.listbox.get(selectedTag)    
            tag = self.materialTagsList.dict[tagName]                      
            self.selectedMaterial.deleteTags([tag])
            self.refreshWindow()
        self.materialTagsList = ListDict(self.root,2,1)
        self.materialTagsList.initialiseTitle("Tags of selected material")
        self.materialTagsList.initialiseLabel("tagEntryLabel","Tag")
        self.materialTagsList.initialiseEntry("tagEntry")
        self.materialTagsList.initialiseButton("addTagButton","Add tag",addTag)
        self.materialTagsList.initialiseButton("deleteTagButton","Delete tag",deleteTags)

    def refreshWindow(self):
        """
        Refreshes all listboxes and displays deps and tags of selected material
        """

        # Making tags and deps the tags and deps of this material
        dependencies = self.selectedMaterial.dependencies
        tags = self.selectedMaterial.tags

        # Clear dep and tags list
        self.materialDepsList.dict = {}
        self.materialTagsList.dict = {}

        # Setting dependency list
        for dependency in dependencies:
            # Getting key that will represent dependency -> What the user will see
            depStr = str(dependency[0])
            depLvlStr = str(dependency[1])
            key = depLvlStr + ": " + depStr
            self.materialDepsList.addItem(key,dependency)

        for tag in tags:
            self.materialTagsList.addItem(tag,tag)
        
        self.materialDepsList.refreshListbox()
        self.materialTagsList.refreshListbox()

        depString = str("Dependencies of " + self.selectedMaterial.name)
        self.materialDepsList.widgetDict["topLabel"].config(text=depString)

        tagString = str("Tags of " + self.selectedMaterial.name)
        self.materialTagsList.widgetDict["topLabel"].config(text=tagString)

    def createFile(self):
        """
        Creates an XML file using the materials and filename provided in the constructor
        """

        XmlHandler.createXmlFile(self.filenameEntry.get(),list(self.newMaterialList.dict.values()))
        
    def addMaterialsToHomepage(self, homepage : Homepage):
        """
        Adds materials to the homepage by exporting materials to a temp file then importing them to the homepage
        """

        XmlHandler.createXmlFile("temp",list(self.newMaterialList.dict.values()))
        homepage.importTemp()



class DependencyConstructor:
    """
    Opens a window for creating dependencies
    """

    def __init__(self, materialConstructor : MaterialConstructor):
        self.root = Toplevel(materialConstructor.root)
        self.root.title("Dependency Constructor")
        
        addDep = Button(self.root, text="Create dependency",command=lambda:self.addDependency(materialConstructor))
        addDep.pack()
        depLevelLabel = Label(self.root,text="Dependency level")
        depLevelLabel.pack()
        self.depLevelEntry = Entry(self.root)
        self.depLevelEntry.pack()

        self.operation = Operation(self.root)

    def addDependency(self,materialConstructor : MaterialConstructor):
        """
        Adds the dependency currently in the constructor to the materialConstructors current material
        """
        tempDep = [self.operation.getTempDep(),self.depLevelEntry.get()]

        materialConstructor.selectedMaterial.addDependency(tempDep)

        materialConstructor.refreshWindow()

        self.root.destroy()
        self = None

        



def turnMatDepIntoText(dependency  : []) -> str:
    """
    Takes a dependency from a material in the form [[opcode, operation, operation],level] and returns the dependency in text form

    Params:
    - dependency : A list representing a dependency

    Returns:
    A string representing the dependency in a human readable form
    """

    returnString = dependency[1] + ": " + turnOperationIntoText(dependency[0])

    return returnString

def turnOperationIntoText(operation : []) -> str:
    """
    Takes an operation from a dependency in the form [opcode, operation, operation] and returns the operation in text form

    Params:
    - operation : A list representing an operation

    Returns:
    A string representing the operation in a human readable form
    """
    
    if operation[0] == None:
        return operation[1].name
    elif operation[0] == "AND":
        return turnOperationIntoText(operation[1]) + " AND " + turnOperationIntoText(operation[2])
    elif operation[0] == "OR":
        return turnOperationIntoText(operation[1]) + " OR " + turnOperationIntoText(operation[2])

def findOrDependencies(material : Material) -> [str]:
    """
    Takes a material and returns a list of its dependencies that have OR in them
    
    Params:
    - material : A material

    Returns:
    A list of strings representing dependencies with ORs in in human readable form 
    """
    
    returnList = []

    for dependency in material.dependencies:
        if doesHaveOrDependency(dependency):
            returnList.append(turnMatDepIntoText(dependency))

    return returnList


def doesHaveOrDependency(dependency) -> bool:
    """
    Takes a dependency and returns if the dependency contains an OR
    """

    operation = dependency[0]
    while operation[0] != None:
        if operation[0] == "OR":
            return True
        if operation[0] == "AND":
            if doesHaveOrDependency([operation[1]]) or doesHaveOrDependency([operation[2]]):
                return True
            return False

        operation = operation[0]
    
    return False
        
        
