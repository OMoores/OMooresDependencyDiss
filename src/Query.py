from re import T
from numpy import number
from src.Debug import Debug
from src.Material import Material
from src.Utility import Utility

class Clause:
    """
        This class will hold a clause which makes up part of a query. A clause is made of a set of variables and a set of dependency levels 
        A clause is true if all of the variables are true

        A clause selects any item with any of the tags AND any of the dependency levels
        
            Attributes:
                - variables : A list of variables this clause selects -> A variable has the form ["tag1","tag2"] and will result in materials with tag1 OR tag2 being selected (can have as many tags as you want per variable)
                - dependencyLevels: A list of dependency levels this clause selects
    """

    def __init__(self):
        """
            Creates a clause
        """
        
        self.variables = [] # Variables are a set of tags that are linked together by an AND
        self.dependencyLevels = []


    def addVariables(self, variables : [[str]]) -> number:
        """
        Adds a list of variables to the clause, making sure there are no duplicate variables added

        Params:
            - var : A list of variables that are to be added to this clause, a list of tags (str)

        Returns:
        The number of variables in this clause
        """
        Debug.printLowPriority("Variables ",variables," are being added to clause ",self)
        for var in variables:
            self.addVariable(var)


        

    def addVariable(self, var : [str]) -> number:
        """
            Adds a single tag to a clause, making sure it is not already in this clause
        
            Params:
                - var : A variable to be added to the clause, a list of tags (str)

            Returns:
            The number of variables in this clause
        """

        # Checks to see tag not already present
        if (len(list(filter(lambda x : var == str(x), self.variables))) > 0):
            Debug.printLowPriority("Tag ",var," already exists in clause ",self)
            
        else: 
            self.variables.append(var)
            Debug.printNoPriority("Tag ",var," has been added to clause ",self)

        return len(self.variables)
    
    def addDependencyLevels(self, dependencyLevels : [str]) -> number:
        """
        Adds a set of dependency levels to the clause, they are only added if they do not already exist in the clause

        Params:
            -dependencyLevels : A list of dependency levels to be added
        
            Returns:
            The number of dependency levels in the clause
        """
        Debug.printLowPriority("Dependency levels ",dependencyLevels," are being added to clause ",self)
        for dep in dependencyLevels:
            self.addDependencyLevel(dep)



    def addDependencyLevel(self, dependencyLevel :[str]) -> number:
        """
            Adds a dependency level to the clause if it is not already a part of the clause

            Params:
                - dependencyLevel : A dependency level to be added
            
            Returns:
            The number of dependency levels in this clause
        """

        # Checks to see dependency level not already present
        if (len(list(filter(lambda x : dependencyLevel == str(x), self.dependencyLevels))) > 0):
            Debug.printLowPriority("Dependency level ",dependencyLevel," already exists in clause ",self)
            
        else: 
            self.dependencyLevels.append(dependencyLevel)
            Debug.printNoPriority("Dependency level ",dependencyLevel," has been added to clause ",self)

        return len(self.dependencyLevels)



class Query:
    """
        This class will hold a query, when a query is given to the solver the solver returns a set of materials based on the query.
        A query is made up of a set of clauses linked together by 

        
        Attributes:
            - clauses: A list of clauses that are in the pysat format
        
    """

    def __init__(self):
        """
            Creates a query 
        """

        self.clauses = []

    def addClauses(self, clauses : []) -> number:
        """
            Adds a list of clauses to the query

            Params:
                - clauses : A clause object
            
            Returns:
            The number of clauses in this query 
        """

        for clause in clauses:
            self.addClause(clause)

        return len(self.clauses)

    def addClause(self, clause : Clause) -> number:
        """
            Adds a clause to the query
        """

        Debug.printNoPriority("Adding clause ",clause," to Query ", self)

        self.clauses.append(clause)

    def solveQuery(self, material : Material) -> [Material]:
        """
            Returns a list of materials that are valid for this query
            
            Params:
            - material : The material the query is being applied to

            Returns:
            A list of materials that the query selects
        """
    
        solvedMaterials = []
        currentMaterials = [material] 
        """
            This will hold the materials that are being examined in the main loop, 
            at the end of the main loop materials that fullfil the clauses of the query will replace the materials in this list and then be examined in the next itteration of the loop
        """

        # While all possible new dependencies are already in the solved list
        while Utility.isASubsetB(currentMaterials, solvedMaterials):
            """
                This is the main loop of the functions 
            """

            subMaterials = [] # A list of the sub materials of the current list of materials

            # Look through current materials and check dependencies against clauses to find valid dependencies, then add to subMaterials
            validMaterials = Query.findValidMaterials(currentMaterials, self)
            
            # Create a list of the materials in validMaterials that are not in solvedMaterials -> uniqueMaterials
            uniqueMaterials = Utility.findAnotinB(validMaterials, solvedMaterials)

            # Add uniqueMaterials to solvedMaterials
            solvedMaterials += uniqueMaterials

            # Set current materials to the uniqueMaterials
            currentMaterials = uniqueMaterials  # At the end of the loop set the sub materials to be looked at in the next loop to the applicable materials from this loop

        return solvedMaterials

    def findValidMaterials(materials : [Material], query) -> [Material]:
        """
            Checks a set of materials against a query and returns materials that fulfil the query, does not return any materials in the materials parameter
            e.g. materials = [A,B], valid materials are [B,C,D] returns [C,D]

            Params:
            - materials : A set of materials
            - query : A query
            Returns:
            A set of materials that fulfil the query
        """
        validMaterialList = []

        # Look through every material
        for mat in materials:
                        
            # Look through each dependency
            for dep in mat.dependencies:

                # If material is valid and not already in return list add to return list
                if Query.isMaterialValid(dep, query) & Utility.isAinB(dep[0], validMaterialList):
                    validMaterialList.append(dep[0])


        return validMaterialList

    
    def isMaterialValid(dependency : [Material, str], query) -> bool:
        """
            Checks to see if a material is valid acording to a query
            
            If the dependency levels are not valid returns false, then checks to see if any variables are false if none are returns true 

            Params:
            - dependency : A dependency from a material [Material, dependencyLevel]
            - query : A query
            Returns:
            A boolean representing if the material fulfils the query
        """

        # Query -> Clause -> Variable -> Tag

        # For each clause in query
        for clause in query.clauses:
            # Check to see if valid dependency level
            if not Query.isDependencyValid(dependency[1], clause):
                return False

            # Check to see status of each variable
            for variable in clause.variables:
                if not Query.isVariableTrue(variable, dependency[0]): # If variable is not valid then the material is not valid
                    return False
                
        return True               

        
    
    def isVariableTrue(variable : [str], material : Material) -> bool:
        """
        Checks to see if a variable is true for a specific material, the variable is true if the material has any of the tags in the variable
        Handles wildcard and negation (*,-)

        Params:
        - variable : A list of tags
        - material : A material

        Returns:
        If a variable is fulfilled by the material
        """


        for tag in variable:
            if tag == "*": # Check for wildcard
                return True
            if tag[0] == "-": # Check for negation
                if not material.doesHaveTag(tag[1:]):
                    return True
            if material.doesHaveTag(tag): # If material has any of the tags the variable is true
                return True
            
        return False


    def isDependencyValid(dependenyLevel : str, clause : Clause) -> bool:
        """
        Checks to see if a dependency level fulfils the dependency levels of a clause
        Handles wildcard and negation (*,-)

        Params:
        - dependencyLevel : A dependency level
        - clause : A clause

        Returns:
        A boolean representing if the dependency level fulfils the dependency levels of the query
        """

        # Look in each clause and get the dependency levels
        for dep in clause.dependencyLevels:
    
            if dep[0] == "*":
                return True
            if dep[0] == "-":
                if str(dep[1:]) != str(dependenyLevel):
                    return True
            else:
                if dep == dependenyLevel:
                    return True

        return False



    







            
