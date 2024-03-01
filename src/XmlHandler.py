from os import error
from uu import Error
from src.Material import *
from src.Debug import *
import xml.etree.ElementTree as etree


class XmlHandler:

    def parseXmlFiles(xmlPathList : [str]) -> [Material]:
        """
        Takes a list of filepaths of xml files and returns a set of materials with their names, tags and dependencies set to the correct values 

        Params:
        - xmlPathList : A list of filepaths

        Returns:
        A list of Materials
        """

        # A dictionary of material names and its Material object
        materialNameDict = {}
        """material name : Material object"""

        # Look at every xml file and create a lists of every material
        for path in xmlPathList:

            Debug.printNoPriority("Reading file: ", path)

            try:
                tree = etree.parse(path)
                root = tree.getroot() # The Materials section of the xml file
            except:
                Debug.printHighPriority("File ",path," is not a valid xml files")
                raise(Error)

            # Check file is formatted properly
            if root.tag != "materials":
                raise Error("File is not formatted properly")


            for child in root: # Each child is a material

                if child.tag != "material":
                    raise Error("File is not formatted properly")

                material = XmlHandler.initMaterial(child)

                # Checking to see if a material with the same name exists in materialNameDict
                if material.name in materialNameDict: 
                    Debug.printLowPriority("Material ",material.name," already exists")
                    raise(Error)
                else:
                    # If a material with this name does not exist then adds material to dictionary with no issues
                    materialNameDict[material.name] = material

        materialNameDict = XmlHandler.setDependencies(materialNameDict)


        # Return list of materials -> Only the values of the materialNameDict
        return list(materialNameDict.values())        

    def initMaterial(child) -> Material:
        """
        Takes the child of the root of a correctly formatted xml file (the material tag) and returns a Material object created from the name and tag found in the child
Exception
        Params:
            - child : Contains the information about a material from an xml file -> etree.parse(path).getroot()[index] will return a child from an appropriate xml file path

        Returns:
        A material with the name and tags from the child input
        """
        # Name defaults to id
        mat = Material(Material.nextId)

        # Setting name
        try:
            # Looking for fileName tag
            fileNameTag = XmlHandler.getTag(child,"fileName")
            mat.setName(fileNameTag[0].text)
    
        except:
            Debug.printHighPriority("Material has failed to created, could not read name: ", mat.name)


        # Setting tags
        try:

            tagList = []
            tagsTag = XmlHandler.getTag(child,"tags")[0]
                    
            for tag in tagsTag:
                tagList.append(tag.text)
            mat.addTags(tagList)

        except:
            Debug.printMediumPriority("Material has failed to add tags: ", mat.name)

        # Adding dependencies in string form
        try:
            tempDep = XmlHandler.getTempDep(child)
            mat.tempDep = tempDep
        except:
            Debug.printMediumPriority("Material has failed to add dependencies: ",mat.name)
        

        return mat

    def setDependencies(materialDict : {str : Material}) -> {str : Material}:
        """
        Params:
            - materialDict : A dictionary name : Material

        Return:
        A dictionary containing materials with all their dependencies set
        """ 

        # A clone of the dictionary, this will be returned
        returnDict = materialDict.copy()

        # Look through every item
        for mat in materialDict.values():
            for dependency in mat.tempDep:
                funcReturn = XmlHandler.formatDependency(dependency, returnDict)
                # Unpacking the return of the function
                formattedDep = funcReturn[0]
                returnDict = funcReturn[1]

                mat.addDependency(formattedDep)

        return returnDict

    
    def formatDependency(unformattedDep, materialDict):
        """
        Takes a dependency as it is in tempDep and returns it with the name of the material replaced with a reference to the material,
        if the material does not exist creates an empty material and adds it to the materialDict

        Returns a list in the format [formattedDep, materialDict]
        """
        formattedDep = []

        funcReturn = XmlHandler.formatOperation(unformattedDep[0],materialDict) # Getting the operation of the dependency formatted and the updated dict, then unpacks
        formattedOp = funcReturn[0]
        updatedDict = funcReturn[1]

        formattedDep.append(formattedOp)
        formattedDep.append(unformattedDep[1])

        return [formattedDep,updatedDict]

    def formatOperation(unformattedOperation, materialDict):
        """
        Takes an unformatted operation and formats it, updating the material dict if a material that is not in the dict is found

        Returns [formattedOperation, materialDict]
        """

        dictClone = materialDict.copy()

        formattedOperation = []
        # This means operation is just a normal dependency, just replace the name of the mateiral with the mateiral
        if unformattedOperation[0] == None:

            # Creating a new operation in the same format but with the material object instead of the name
            formattedOperation.append(None)
            matName = unformattedOperation[1]
            if dictClone.get(matName) is not None:
                formattedOperation.append(dictClone[matName])
            else:
                dictClone[matName] = Material(matName) # Creating a placeholder material if a material with the name in the dependency does not exist
                formattedOperation.append(dictClone[matName])
            return [formattedOperation, dictClone]
        else:
            # Creating new AND or OR operation 
            formattedOperation.append(unformattedOperation[0])
            funcReturn = XmlHandler.formatOperation(unformattedOperation[1], dictClone) # Getting the new formatted op and the updated dict
            newOperation = funcReturn[0]
            dictClone = funcReturn[1]
            formattedOperation.append(newOperation)
            funcReturn = XmlHandler.formatOperation(unformattedOperation[2], dictClone)
            newOperation = funcReturn[0]
            dictClone = funcReturn[1]
            formattedOperation.append(newOperation)

            return [formattedOperation, dictClone]

    def getTag(element, tagName : str):
        """
        Takes a etree element from an XML file and a tagName and returns any tags that have the name tagName

        Params:
        - element : An etree element that represents a tag e.g. dependencies
        - tagName : The name of a tag

        Returns:
        Returns a list of all of the tags in element that have the name tagName
        """

        tags = []

        for i in range(len(element)):
            if element[i].tag == tagName:
                tags.append(element[i])

        return tags
    
    def getTempDep(element):
        """
        Takes the dependencies element from an XML file and returns a list of temp deps, dependencies before they have been formatted and added to a material

        Params:
        - element : An etree element (should be the material element) 

        Returns:
        A list of dependencies in the format [[operation,"dependency level"],...]
        
        An operation is either a material or an OR, AND or NOT operation

        material -> [None,"material name"] --- None means this list only contains a material name
        OR -> ["OR", operation, operation]
        AND -> ["AND", operation, operation]
        """

        # Looking through every tag in dependency tag and adding their text -> Will be used later to find actual dependencies
        dependenciesTag = XmlHandler.getTag(element,"dependencies")[0]

        dependencies = [] 

        for dependencyTag in dependenciesTag:
            dependency = XmlHandler.createDependency(dependencyTag) # Creates an empty dependency -> No operator, no material, dependency level
            dependencies.append(dependency)

        return dependencies


    def createDependency(element):
        """
        Takes a dependency level element and turns it into a list that represents a dependency

        Param:
        - element : An etree element, should be a dependencyTag e.g. requires

        Returns:
        A list representing a dependency [operation, dependency level] (List of operations can be found in the description of the function getTempDep)
        """

        return [XmlHandler.createOperation(element),element.tag]
        
        

    def createOperation(element):
        """
        Takes an element inside a dependency level element and turns it into an operation  

        Param:
        - element : An etree element, should be an AND, OR or material element

        Returns:
        A list representing an operation (List of operations can be found in the description of the function getTempDep)
        """

        # If dependency is just a material it will have a length of 0 and the text will be the material
        if len(element) == 0:
            return [None, element.text]
        elif element.tag == "OR": # An OR dependency
            # Make sure there are only 2 materials
            if len(element) == 2:
                return ["OR",XmlHandler.createOperation(element[0]),XmlHandler.createOperation(element[1])]
            else:
                Debug.printHighPriority("When reading XML file found OR statement with more then 2 materials")
        elif element.tag == "AND": # An AND dependency
            # Make sure there are only 2 materials
            if len(element) == 2:
                return ["AND",XmlHandler.createOperation(element[0]),XmlHandler.createOperation(element[1])]
            else:
                Debug.printHighPriority("When reading XML file found OR statement with more then 2 materials")
        else:
            return XmlHandler.createOperation(element[0])