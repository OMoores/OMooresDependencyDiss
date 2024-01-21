from pysat.formula import CNF
from pysat.solvers import Glucose3
import xml.etree.ElementTree as etree

class Material(): 
    materialNum = 0

    def __init__(self,xmlMaterial):
        self.xmlTree = xmlMaterial

        self.materialNum = Material.materialNum
        Material.materialNum += 1

        self.name = xmlMaterial[0].text

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
            Takes the dependencies section of an XML file and turns it into a list of dependencies
        """

        dependencyList = []

        for child in xmlDependencies:
            dependencyList.append(child.text)

        return dependencyList

    def getDependencyClause(self):
        """
            Looks at the dependencies for the object and returns a dependency clause that can be used with pysat
        """
        
        clause = []

        for dependency in self.dependencies:
            clause.append(materialDict[dependency])

        return clause
    
    def getDependencies(self, previousClauses = []):
        """
            Gets all dependencies from this material, including dependencies of dependencies
        """

        clauses = self.getDependencyClause()

        # Add two clauses together
        clauses.append(previousClauses)

        # Remove any duplicate materials

    def removeDuplicates(list):
        """
            Removes duplicate items from a list
        """

        returnList = list
        for item in list:
            returnList = Material.removeDuplicate(list, item)

        return returnList

        

        return list

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

# Create a dictionary with the material and its number
materialDict = {}
for mat in materialArray:
    materialDict[mat.name] = mat.materialNum

clauses = []

for mat in materialArray:
    clauses.append(mat.getDependencyClause())

clauses = list(filter(lambda clause: (len(clause) > 0), clauses))
print(clauses)

g = Glucose3()

list = [1,2,2,2,1,1,4,5,6,3,4,5,4]
print(Material.removeDuplicates(list))



