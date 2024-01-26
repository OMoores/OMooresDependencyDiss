from Material import Material
from Debug import Debug
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

            tree = etree.parse(path)

            root = tree.getroot() # The Materials section of the xml file

            for child in root: # Each child is a material
                material = XmlHandler.initMaterial(child)

                # Checking to see if a material with the same name exists in materialNameDict
                if material.name in materialNameDict: 
                    Debug.printLowPriority(str("Material ",material.name," already exists"))
                else:
                    # If a material with this name does not exist then adds material to dictionary with no issues
                    materialNameDict[material.name] = material


        # Return list of materials -> Only the values of the materialNameDict
        return materialNameDict.values()        

    def initMaterial(child) -> Material:
        """
        Takes the child of the root of a correctly formatted xml file (the material tag) and returns a Material object created from the name and tag found in the child

        Params:
            - child : Contains the information about a material from an xml file -> etree.parse(path).getroot()[index] will return a child from an appropriate xml file path

        Returns:
        A material with the name and tags from the child input
        """

        # Setting name
        try:
            mat = Material(child[0])
        except:
            Debug.printMediumPriority("Material has failed to created, could not read name: ", child)

        # Setting tags
        try:
            tagList = []

            for tag in child[1]:
                tagList.append(tag.text)

            mat.addTags(child[1])
        except:
            Debug.printMediumPriority("Material has failed to add tags: ", mat.name)
        
        


