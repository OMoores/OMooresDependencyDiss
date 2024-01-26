# Importing Index
from src.Debug import *
from src.Utility import *

class Material:
    """
        A class that holds information about a piece material and its dependencies

        Attributes:
        - id
        - name
        - tags
        - dependencies
    """
    id = 0

    def __init__(self, name : str, tags : [str] = []):
        """
        Params:
            - name : The name of the material
            - tags (optional) : A list of strings that contain the tags for this material
        """

        self.name = self.setName(name)
        self.id = Material.id
        Material.id += 1
        self.tags = []
        self.addTags(tags)
        self.dependencies = [] 


        

    def setName(self, name : str) -> str:
        """
            Sets the name of a material and then returns the name of the material
            
            Params:
                - name : The name the material is to be given

            Returns:
            The name of the material 

        """
        Debug.printNoPriority("Material name being set: ", name)

        self.name = name

        return self.name

    def addTags(self, tags : [str]) -> int:
        """
            Adds a list of strings to the tags of a material and returns the number of tags a material has

            Params:
                - tags : A list of tags that are to be added to the materials tags

            Returns:
            The number of tags the material has
        """
        Debug.printNoPriority("Material tags being added: ", tags)

        # Check if tag is already in self.tags
        for tag in tags:
            if (Utility.isAinB(tag, self.tags)):
                self.tags.append(tag)

        return len(self.tags)


    

    def addDependencies(self, dependencies) -> int:
        """
            DECIDE HOW THESE ARE TO BE ADDED

            Params:
                - dependencies : 

            Returns:
            The number of dependencies the material has
        """
        ...

print(Material("AEIOU",["d"]))