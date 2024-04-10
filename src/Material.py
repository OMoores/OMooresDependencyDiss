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

    def deleteTags(self, tags : [str]):
        for tag in tags:
            self.tags.remove(tag)

    

    def addDependency(self, dependency) -> int:
        """
            Adds a material to the dependency list of this material if a dependency of the same name does not exist

            Params:
                - dependency : A formatted dependency clause e.g. [[None,material],"requires"]

            Returns:
            The number of dependencies the material has
        """

        if not Utility.isAinB(dependency, self.dependencies):
            Debug.printLowPriority("Adding dependency: '", dependency,"' to material'",self.name,"'")
            self.dependencies.append(dependency)
        else:
            Debug.printLowPriority("Dependency '", dependency,"' already exists in material '",self.name,"'")

    def doesHaveTag(self, checkTag : str) -> bool:
        """
            Checks to see if a material has a tag. Works with - and *

            Params:
            - tag : A tag
            Returns:
            A boolean representing if material has the tag in
        """

        if checkTag == "*":
            return True
        if checkTag[0] == "-":
            if self.doesHaveTag(checkTag[1:]):
                return False
            return True

        for tag in self.tags:
            if str(tag) == str(checkTag):
                return True
            
        return False

        
        
    def printMaterialList(materials : []):
        """
        Prints a list of materials names
        """

        list = []
        for mat in materials:
            list.append(mat.name)

        print(list)


    def getDependencies(self, resolvers : [[str]] = []) -> [[]]:
        """
        Looks at this material and finds all of its dependencies and their dependency levels. Uses the resolvers to resolve any OR 

        Params:
        - material : The material whos dependencies will be extracted
        - resolvers : A 2d list of names/tags that will be used to resolve any OR dependencies (defaults to [])

        Returns:
        A list of materials and their dependency levels in the format [[Material, str]]
        """

        dependencies = {} # A dict with [material, dependency level] and value an empty string, get they keys to 

        for dependency in self.dependencies:

            

            # Find all of the materials and their dependency levels in each dependency
            newDependencies = extractDependency(dependency, resolvers) # Dependencies from this itteration of the loop
            # Adds dependencies if they arent already in the dependencies dict
            for newDep in newDependencies:

                # An items id in the dict is their name + their dep level
                id = newDep[0].name + newDep[1]
                
                # If a dependency has not been added to the dependencies dict add it
                if dependencies.get(id) is None:
                    dependencies[id] = newDep

        return list(dependencies.values())
    
    def resolutionLevel(self, resolver : [[str]]) -> int:
        """
        Takes a 2d list of strings (a resolver) and checks the properties of the material against these. If a list starts with [None,...] it means the tags are being checked 
        and if it starts with ["string"] It means the name is being checked. Returns the index furthest down the list where the materials name matches or all the tags are present in this material

        Params:
        - resolvers : A 2d list of names/tags that will be used to resolve any OR dependencies

        Returns:
        An int, the index of the resolver where this material is resolved
        """
        # Looks at every index in resolver
        for i in range(len(resolver)):
            if resolver[i][0] is None: # This index of resolver is a tag list

                # Checks if negation occurs in any of the resolvers
                for tag in resolver[i][1:]:
                    if tag[0] == "-":
                        print(tag[1:])
                        if not Utility.isAinB(tag[1:],self.tags): # The negated tag is not present so this is valid

                            if len(resolver[i][1:]) == 1: # If the negated tag is the only resolver then this resolution level is true => resolver would be [[None,-tag],...]
                                return i
                            else:
                                resolver[i].remove(tag)
                                
                                       

                # If the tags (the first item in a list of tags in the resolver is none to flag that the list is tags not a name
                if Utility.isASubsetB(resolver[i][1:],self.tags):
                    return i
            else:
                if self.name == resolver[i][0]:
                    return i

        return None # If material does not resolve returns None
            
            



def extractDependency(dependency : [], resolvers : [[str]] = []) -> [[Material,str]]:
    """
    Takes a dependency and extracts all of the materials in that dependency and returns each material with the dependency level in a list

    Params:
    - dependency : A list representing a dependency in the form [operation, dependency level]
    - resolvers : A 2d list of names/tags that will be used to resolve any OR dependencies, defaults to an empty list

    Returns:
    A list of materials and their dependencies in the format [[Material, str]]
    """

    dependencyLevel = dependency[1]
    operation = dependency[0]

    
    return extractOperation(operation, dependencyLevel, resolvers)

    

def extractOperation(operation, dependencyLevel, resolvers : [[str]] = []) -> [[Material,str]]:
    """
    Takes an operation and extracts all of the materials in that operation and returns each material with the dependency level in a list.
    If a decision cannot be made returns an error

    Params:
    - operation : A list representing an operation in the form [None, material] or [AND/OR, operation, operation]
    - dependencyLevel : The dependency level of this operation
    - resolvers : A 2d list of names/tags that will be used to resolve any OR dependencies

    Returns:
    A list of materials and their dependencies in the format [[Material, str]]
    """

    if operation[0] == None:
        return [[operation[1], dependencyLevel]]
    if operation[0] == "AND":
        return extractOperation(operation[1],dependencyLevel, resolvers) + extractOperation(operation[2],dependencyLevel,resolvers)
    if operation[0] == "OR": # Try to resolve OR, if cannot errors
        
        # If cannot find material in operation due to insufficient resolver information then picks the other set of material (assuming this set can be resolved) else errors
        try:
            operation1Materials = resolveOperation(operation[1], dependencyLevel, resolvers)
        except:
            operation1Materials = None

        try:
            operation2Materials = resolveOperation(operation[2], dependencyLevel, resolvers)
        except:
            operation2Materials = None


        if operation1Materials == None and operation2Materials == None:
            # Returning both materials as if the OR was an AND
            print("Could not resolver operation: ", operation, " with resolvers: ", resolvers)
            return extractOperation(operation[1],dependencyLevel, resolvers) + extractOperation(operation[2],dependencyLevel,resolvers) # If cannot resolve then returns both materials
        elif operation1Materials == None:
            return operation2Materials[1] # Item 0 return from resolve operations is the resolution level
        elif operation2Materials == None:
            return operation1Materials[1]
        
        if operation1Materials[0] > operation2Materials[0]: # Higher resolution level means lower priority
            return operation2Materials[1]
        elif operation2Materials[0] > operation1Materials[0]:
            return operation1Materials[1]
        else:
            #Tries to resolve without the resolution level they were both succesful with, sees if there is another that one has priority with
            resolvers.pop(operation1Materials[0])
            return extractOperation(operation,dependencyLevel,resolvers)
            #raise Exception("Could not resolve an OR with operations:\n",operation[1], "\n",operation[2],"\nWith resolvers: ",resolvers, "\nBoth had same resolution level so no decision could be made")
        

def resolveOperation(operation, dependencyLevel, resolvers) -> [int,[[Material,str],...]]:
    """
    Takes an operation and create extracts all the materials from it using extractOperation, then checks that all the materials that are found are resolvable acording to the resolvers.
    If they are not resolvable errors
    

    Params:
    - operation : The operation being resolved for
    - dependencyLevel : The dependency level of this operation
    - resolvers : A 2d list of names/tags that will be used to resolve any OR dependencies

    Returns:
    A list of materials and their dependencies in the format [int,[[Material, str]]]. The int represents the resolution level of this operation
    """

    # Finding the resolution level of AND -> The lowerst common resolution level of both operations in the AND
    if operation[0] == "AND":

        # Finding the lowest resolution level of each operation
        try:
            operation1Resolution = resolveOperation(operation[1],dependencyLevel,resolvers)
            operation2Resolution = resolveOperation(operation[2],dependencyLevel,resolvers)
        except:
            raise Exception("Resolution failed")

        # Returns the lowest common resolution level
        if operation1Resolution[0] == operation2Resolution[0]:
            returnVal = [operation1Resolution[0]] + [extractOperation(operation[1], dependencyLevel, resolvers) + extractOperation(operation[2], dependencyLevel, resolvers)]
            return returnVal
        # If resolution level is not same removes lowest resolution level of the 2 and tries again
        elif operation1Resolution[0] < operation2Resolution[0]:
            resolvers.pop(operation1Resolution[0])
            return resolveOperation(operation,dependencyLevel,resolvers)
        else:
            resolvers.pop(operation2Resolution[0])
            return resolveOperation(operation,dependencyLevel,resolvers)        
    # Finding the resolution level of OR -> The resolution level of operation in the operation selected by the resolvers

    # Finding the resolution level of Material 

    # This gets a list of materials then need to find the resolutionLevel of each material, if a material does not have a resolution level then error
    extractedMaterials : [] = extractOperation(operation, dependencyLevel, resolvers) # Materials extracted from the operation in the format [material, dependency level]

    # Finds the lowest common resolution level of all materials#
    for resolutionLevel in range(0,len(resolvers)):
        skipLoop = False
        for pair in extractedMaterials:
            material : Material = pair[0]
            if not material.resolutionLevel([resolvers[resolutionLevel]]) != None:
                skipLoop = True
                break
        if skipLoop == False:
            return [resolutionLevel,extractedMaterials]

            

    raise Exception("Could not resolve")

        






    

