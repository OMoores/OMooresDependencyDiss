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
            for i in range(0,len(child)):
                if child[i].tag == "fileName":
                    mat.setName(child[i].text)
                    break
        except:
            Debug.printHighPriority("Material has failed to created, could not read name: ", mat.name)


        # Setting tags
        try:
            tagList = []

            for i in range(0,len(child)):
                if child[i].tag == "tags":
                    
                    for tag in child[i]:
                        tagList.append(tag.text)
                    break
            mat.addTags(tagList)
        except:
            Debug.printMediumPriority("Material has failed to add tags: ", mat.name)

        # Adding dependencies in string form
        try:
            # Looking through every tag in dependency tag and adding their text -> Will be used later to find actual dependencies
            for i in range(0,len(child)):
                if child[i].tag == "dependencies":
                    for dep in child[i]:
                        mat.tempDep.append([dep.text, dep.tag])
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
            for strDep in mat.tempDep:
                Debug.printNoPriority("Setting dependency for ",mat.name," adding dependency '",strDep[0],"' at level ", strDep[1])
                # Checking to see if dependency exists
                if returnDict.get(strDep[0]) is not None:
                    mat.addDependency(returnDict[strDep[0]],strDep[1]) # Getting the material object and parsing the dependency level
                else:
                    Debug.printLowPriority("Could not find material '",strDep,"' for dependency, creating placeholder material")
                    # If material does not exist create it with placeholder tag
                    returnDict[strDep[0]] = Material(strDep[0])
                    returnDict[strDep[0]].addTags(["placeholder"])

        Debug.printNoPriority("Setting dependencies. Current materialDict: ", materialDict.values())

        return returnDict


