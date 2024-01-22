from pysat.formula import CNF
from pysat.solvers import Glucose3
import xml.etree.ElementTree as etree

class Material(): 
    materialNum = 0
    materialDict = {}
    """ A dictionary holding all materials created materialNum : Material"""
    materialNameDict = {}

    def __init__(self,xmlMaterial):
        self.xmlTree = xmlMaterial
        self.dependencies = []
        """
            A list of materials this material is dependent on
        """
        self.materialNum = Material.materialNum
        """
            The number that will represent this material in pysat clauses
        """
        Material.materialNum += 1

        try:
            self.name = xmlMaterial[0].text

        except:
            self.name = ""


        try:
            self.tags = self.parseTags(xmlMaterial[1])
        except:
            print("No tags")
            self.tags = []
        
        
        try:
            self.dependencies = self.parseDependencies(xmlMaterial[2])
        except:
            print("No dependencies")
            self.dependencies = []

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
            Takes the dependencies section of an XML file and turns it into a list of dependencies => Filenames
        """
        dependencyList = []

        for child in xmlDependencies:
 
            dependencyList.append(child.text)

        return dependencyList

    def getDependencyClause(self): # RETURNS NAMES NOT NUMBERS
        """
            Looks at the dependencies for the object and returns a dependency clause that can be used with pysat
        """
        
        clause = []

        for dependencyName in self.dependencies:
            clause.append(Material.materialNameDict[dependencyName])

        return clause
    
    def getDependencies(self, previousClauses = []):
        """
            Gets all dependencies from this material, including dependencies of dependencies
        """

        clauses = self.getDependencyClause()

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
            tempDep += Material.getDependencies(Material.materialDict[dep], clauses)

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
    

    




    

# Get XML file
tree = etree.parse("./TestMaterial/NatInspired/GenProg.xml")
root = tree.getroot() # Materials

#Array holding materials
materialArray = []

# Create every material
for child in root:
    materialArray.append(Material(child))




g = Glucose3()

print(materialArray[6].name)
for item in materialArray[6].getDependencies():
    print(Material.materialDict[item].name)



