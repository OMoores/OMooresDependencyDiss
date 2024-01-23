from pysat.formula import CNF
from pysat.solvers import Glucose3
import xml.etree.ElementTree as etree

class Dependency:
    """
        An object representing a dependency, the highest priority dependancy has a priority of 0
    """


    dependencyDict = {}
    """ A list holding the priorities of all dependencies """
    dependencyPriorityDict = {}
    """ A dictionary mapping priority level to dependency type, priority : [list of dep types] """

    def __init__(self, name : str, priority : int):
        self.name = name
        self.priority = priority


        Dependency.dependencyDict[self.name] = self.priority

        # If a dependency type of this priority already exists, adds this dependency type to a list with already existing ones, if not creates a list with only this type in
        try:
            Dependency.dependencyPriorityDict[self.priority] = Dependency.dependencyPriorityDict[self.priority].append(self)
        except:
            Dependency.dependencyPriorityDict[self.priority] = [self]

    def getPriorityDependencyTypes(priority):
        """
            Returns all types of dependencies that are of greater or equal priority
        """

        depTypeList : list[Dependency] = []

        # Looks through each priority level higher then the more imp
        for i in range(0, priority + 1):
            depTypeList += Dependency.dependencyPriorityDict[i]

        return depTypeList

    def setUpDependencies():
        """
            Creates some basic dependency types
        """

        Dependency("requires",0)
        Dependency("recommends",1)
        Dependency("optional",2)











class Material: 
    """
        An object representing a piece of learning material
    """


    materialNum = 0
    materialDict = {}
    """ A dictionary holding all materials created materialNum : Material """
    materialNameDict = {}
    """ A dictionary holding all the names of all materials created materialName : materialNum """
    

    def __init__(self,xmlMaterial):
        self.xmlTree = xmlMaterial
        """
            The xmlTree that represents this material
        """
        # -----
        self.materialNum = Material.materialNum
        """
            The number that will represent this material in pysat clauses
        """
        Material.materialNum += 1 # Incrimenting material so next material is given different number

        # -----
        self.name = str(self.materialNum) # Materials default name is its number
        """
            The name of a material, set to fileName if one is present
        """
        try:
            self.name = xmlMaterial[0].text
        except:
            print("Could not find material name, setting name to material number ",self.name)
        # -----
        self.tags = []
        """
            The tags of a material
        """
        try:
            self.tags = self.parseTags(xmlMaterial[1])
        except:
            print("No tags for material ",self.name)
        # -----
        self.dependencies = []
        """
            A list of materials this material is dependent on: [[dependencyName, dependency level],[],[]], access via get direct dependencies function which will return the materialObjects
        """
        try:
            self.dependencies = self.parseDependencies(xmlMaterial[2])
        except:
            print("No dependencies")
            self.dependencies = []

        # CHANGE IF NECESSARY
        Material.materialDict[self.materialNum] = self
        Material.materialNameDict[self.name] = self.materialNum



    def parseTags(self, xmlTags):
        """
            Takes the tags section of an XML file and turns it into a list of tags
        """

        tagList = []

        for child in xmlTags:
            tagList.append(child.text)

        return tagList

    def parseDependencies(self, xmlDependencies):
        """
            Takes the dependencies section of an XML file and turns it into a list of dependencies []
        """
        dependencyList = []

        for child in xmlDependencies:
 
            dependencyList.append([child.text,child.tag])

        

        return dependencyList
    
    def getDirectDependencies(self):
        """
            Returns the directDependencies of this object as a list of material objects
            In future versions will need to account for not being able to find a material
            [Material, priority]
        """

        dirDeps = []
        # Returns the dependency array after replacing every name with the materials associated object
        for dep in self.dependencies:
            dirDeps.append([Material.getUsingMaterialName(dep[0]), dep[1]])

        return dirDeps

    def getUsingMaterialNum(num):
        """
            Returns the material object of the material with the corresponding material number
        """

        return Material.materialDict[num]
    
    def getUsingMaterialName(name):
        """
            Returns the material object of the material with the corresponding material name
        """

        num = Material.materialNameDict[name]

        return Material.getUsingMaterialNum(num)



    def getDependencies(self, dependencyType, previousClauses = []):
        """
            Gets all dependencies from this material, including dependencies of dependencies
        """

        dirClause = self.getDirectDependencies() # A list of [Material, priority]

        clauses = []
        # Remove items of insufficient priority
        for dep in dirClause:
            
            depPriority = Dependency.dependencyDict[dep[1]]

            if depPriority <= dependencyType[0].priority:
                clauses.append(dep)

        if len(clauses) == 0:
            return clauses
        if len(previousClauses) == len(Material.removeDuplicates(clauses + previousClauses)):
            return Material.removeDuplicates(clauses + previousClauses)
        
        clauses = Material.removeDuplicates(clauses + previousClauses)
        
        # Find dependencies that are not in previous clauses 
        newDependencies = Material.findItemsNotInA(previousClauses,clauses)

        tempDep = []
        # For every new dependency find their dependencies
        for dep in newDependencies:
            tempDep += Material.getDependencies(Material.materialDict[dep[0].materialNum], dependencyType, clauses)

        newDependencies += Material.findItemsNotInA(newDependencies,tempDep)

        # Return new dependencies 
        return newDependencies
    
    
    def removeDuplicates(list):
        """
            Removes duplicate items from a list
        """

        returnList = list
        for item in list:
            returnList = Material.removeDuplicate(list, item)

        return returnList

        

        return list
    
    def findItemsNotInA(A,B): # TODO
        """
            Returns a list of items in B that are not in A
        """

        returnSet = []

        # Look through every item in B and see if it is in A
        for AItem in B:
            inA = False
            for BItem in A:
                if AItem == BItem:
                    inA = True
            
            if not inA:
                returnSet.append(AItem)
        
        return returnSet
                    


    def removeDuplicate(list, duplicate):
        """
            Checks list for item and removes all but the first instance of this item
        """

        # Has the first occurence of the item been found
        found = False

        # Looks through every item in list and checks if it is the same as the duplicate
        index = 0
        while index < len(list):
            if list[index] == duplicate:

                if found == True:
                    list.pop(index)
                    continue
                found = True
            index +=1

        return list


    
def parseXMLFiles(xmlList : list[str]) -> list[Material]:
    """
        Takes a list of XMLFiles and returns a list of material objects based on the materials contained in the XML files
    """

    materialList : list[Material] = []

    # Parse every file individually and add all materials to materialList
    for file in xmlList:
        tree = etree.parse(file)

        root = tree.getroot()

        for child in root:
            materialList.append(Material(child))




    return materialList


matList = parseXMLFiles(["./TestMaterial/NatInspired/GenProg.xml"])
Dependency.setUpDependencies()

list = matList[0].getDependencies(Dependency.getPriorityDependencyTypes(0))

for item in list:
    print(item[0].name, item[1])