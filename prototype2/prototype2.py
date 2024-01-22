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
        Dependency.dependencyPriorityDict[self.priority] = [self] + Dependency.dependencyPriorityDict[self.priority]

    def getPriorityDependencyTypes(priority):
        """
            Returns all types of dependencies that are of greater or equal priority
        """

        depTypeList : list[Dependency] = []

        # Looks through each priority level higher then the more imp
        for i in range(0, priority):
            depTypeList += Dependency.dependencyPriorityDict[i]

        return depTypeList












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
        """

        # Returns the dependency array after replacing every name with the materials associated object
        dirDeps = self.dependencies.map( lambda dep : [Material.getUsingMaterialName(dep[0]), dep[1]])

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

        return Material.getUsingMaterialNum[num]
    
    def getPriorityDependencies(self, dependencyType : Dependency):
        """
            Gets all dependencies for this object that are of the type provided or a higher priority
        """


    
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

for item in matList:
    print(item.name)