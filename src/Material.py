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
    nextId = 0

    def __init__(self, name : str, tags : [str] = []):
        """
        Params:
            - name : The name of the material
            - tags (optional) : A list of strings that contain the tags for this material
        """

        self.name = self.setName(name)
        self.id = Material.nextId
        self.tags = [] # Initialise tags variable
        self.addTags(tags)
        self.dependencies = [] 
        self.tempDep : [[str,str]] = []  
        """
            A variable used to hold the dependency information from the xml file
            [dependency name, dependency level]
        """

        Debug.printLowPriority("Material being initialised, name: ",self.name,", id: ",self.id,", tags: ",self.tags,", dependencies: ",self.dependencies)


        Material.nextId += 1

 


        

    def setName(self, name : str) -> str:
        """
            Sets the name of a material and then returns the name of the material
            
            Params:
                - name : The name the material is to be given

            Returns:
            The name of the material 

        """
        Debug.printNoPriority("Material name being set to: ", name)
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
        Debug.printNoPriority("Material tags being added: ", tags, " for Material ", self.name)

        # Check if tag is already in self.tags
        for tag in tags:
            if (not Utility.isAinB(tag, self.tags)):
                self.tags.append(tag)

        return len(self.tags)


    

    def addDependency(self, dependency, dependencyLevel) -> int:
        """
            Adds a material to the dependency list of this material if a dependency of the same name does not exist

            Params:
                - dependency : A material object
                - dependencyLevel : The level of dependency on a material

            Returns:
            The number of dependencies the material has
        """

        if not Utility.isAinB(dependency, self.dependencies):
            Debug.printNoPriority("Adding dependency '", dependency.name,"' to Material '",self.name,"'")
            self.dependencies.append([dependency,dependencyLevel])
        else:
            Debug.printLowPriority("Dependency '", dependency.name,"' already exists in material '",self.name,"'")

        
        
