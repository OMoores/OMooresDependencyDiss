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


g = Glucose3()

