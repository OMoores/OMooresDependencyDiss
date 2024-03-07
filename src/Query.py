from xmlrpc.client import Boolean
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

  



def queryDependencies(materials : [Material], query : Query, resolvers : [[str]] = []):
    """
    Takes a set of materials and examines their dependencies, finding a list of materials that all satisfy a query.
    All materials must be linked to the original materials by a set of materials that fulfil the query.

    The resolvers parameter contains a list that will be used to resolve OR statements.
    [[None,tag1,tag2],[None,tag3,tag4]] -> Will look at the tags of a material. A material with tag1 and tag2 will be chosen in the OR, if none have these then a material with tag3 and tag4 will be chosen
    [["name"],[None,...]] -> Will look if either of the materials have the name "name", if none do then looks at the next resolver

    If none have these tags then throws an error

    Params:
    - materials : A list of materials that will be queried, the materials returned will all be subdependencies of at least one of these materials
    - query : A query, only materials that satsify this query will be returned
    - resolvers : This will contain a 2d list of tags that will be used to resolve OR statements

    Returns a list of materials that fulfil the query
    """

    # These are faster to access then a list (Think they use hash tables) and are used to check if a material has been looked at before 
    searchedMaterials = {}  # Key is materialname+dependencylevel value is an empty string
    validMaterials = {} # Key is material name value is the material

    # These will hold all the materials that are going to be examined in the next itteration of the main loop
    searchingMaterials = materials

    # Adding materials to validMaterials
    for mat in searchingMaterials:
        validMaterials[mat.name] = mat

    # Will stop when there are no materials left to search
    while len(searchingMaterials) > 0:

        newMaterials = [] # Materials that have been found that will be searched in the next itteration of the loop

        for material in searchingMaterials:
            dependencies = material.getDependencies(resolvers)
            
            # Look through every new dependency
            for dependency in dependencies:

                # Check if dependency is new
                if validMaterials.get(dependency[0].name) is not None:
                    continue
                # If material is in searched material with the correct dependency level it has already been searched so do not search again
                if searchedMaterials.get(dependency[0].name+dependency[1]) is not None:
                    continue
                # Add material to searched materials
                searchedMaterials[dependency[0].name+dependency[1]] = ""
                # Check if material is valid with its dependency
                if isQueryValid(dependency[0],dependency[1],query):
                    validMaterials[dependency[0].name] = dependency[0]
                    # This material is valid so add it to newMaterials
                    newMaterials.append(dependency[0])
                 

                

        # The valid materials that have been found will be looked at in the next loop
        searchingMaterials = newMaterials

    return validMaterials.values()
                
                







def isQueryValid(material, dependencyLevel : str, query : Query) -> bool:
    """
    Takes a material and its dependency level and checks if it is valid for a query

    params:
    - material : The material being checked against the query
    - dependencyLevel : The dependency level of the material
    - query : The query the material is being checked against

    Returns:
    A boolean representing if the material is valid 
    """

    for clause in query.clauses:
        if isClauseValid(material,dependencyLevel, clause):
            return True
        
    return False
    

def isClauseValid(material, dependencyLevel : str, clause : Clause) -> bool:
    """
    Takes a material, a dependencyLevel and a clause and checks if the material is valid for the clause
    """
    
    if not isDependencyLevelValid(dependencyLevel,clause):
        return False

    for variable in clause.variables:
        if not isVariableValid(material,variable):
            return False
        
    return True

def isVariableValid(material, variables : []) -> bool:
    """
    Takes a variable (a set of tags) and returns true if the material has any of these tags
    """

    # Check for wildcard
    if Utility.isAinB("*",variables):
        return True
    # Check for negation
    for variable in variables:
        if variable[0] == "-":
            if not Utility.isAinB(variable[1:],material.tags):
                return True
        elif Utility.isAinB(variable,material.tags):
            return True 
    return False
    
    
    

def isDependencyLevelValid(dependencyLevel : str, clause : Clause) -> bool:
    """
    Takes a clause and a dependency level and returns if the dependency is valid for the clause
    """

    for depLvl in clause.dependencyLevels:
        if depLvl[0] == "-":
            if not dependencyLevel == depLvl[1:]:
                return True

    if Utility.isAinB("*",clause.dependencyLevels):
        return True

    if Utility.isAinB(dependencyLevel,clause.dependencyLevels):
        return True
    return False