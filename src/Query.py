from numpy import number
from src.Debug import Debug
from src.Material import Material
from src.Utility import Utility


class Query:
    """
        This class will hold a query, when a query is given to the solver the solver returns a set of materials based on the query.
        A query is made up of a set of clauses linked together by 
    """

    def __init__(self):
        """
            Creates a query

            Attributes:
                - clauses: A list of clauses that are in the pysat format
                
        """

        self.dependencyLevels = [] 
        """ The levels of dependency this clause applies to """

    def addClauses(clauses : []) -> number:
        """
            Adds a clause to the query

            Params:
                - clause : A clause object
            
            Returns:
            The number of clauses in this query 
        """

    def solveQuery() -> [Material]:
        """
            Returns:
            A list of materials that the query selects
        """

        

class Clause:
    """
        This class will hold a clause which makes up part of a query. A clause is made of a set of tags, a set of dependency levels 

        A clause selects any item with any of the tags AND any of the dependency levels
    """

    def __init__(self):
        """
            Creates a clause

            Attributes:
                - tags: A list of tags this clause selects
                - dependencyLevels: A list of dependency levels this clause selects
        """
        
        self.tags = []
        self.dependencyLevels = []


    def addTags(self, tags : [str]) -> number:
        """
        Adds a list of tags to the clause, making sure there are no duplicate tags added

        Params:
            - tags : A list of tags that are to be added to this clause

        Returns:
        The number of tags in this clause
        """
        Debug.printLowPriority("Tags ",tags," are being added to clause ",self)
        for tag in tags:
            self.addTag(tag)


        

    def addTag(self, tag : str) -> number:
        """
            Adds a single tag to a clause, making sure it is not already in this clause
        
            Params:
                - tag : A tag to be added to the clause

            Returns:
            The number of tags in this clause
        """

        # Checks to see tag not already present
        if (len(list(filter(lambda x : tag == str(x), self.tags))) > 0):
            Debug.printLowPriority("Tag ",tag," already exists in clause ",self)
            
        else: 
            self.tags.append(tag)
            Debug.printNoPriority("Tag ",tag," has been added to clause ",self)

        return len(self.tags)
    
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

        # Checks to see tag not already present
        if (len(list(filter(lambda x : dependencyLevel == str(x), self.tags))) > 0):
            Debug.printLowPriority("Dependency level ",dependencyLevel," already exists in clause ",self)
            
        else: 
            self.dependencyLevels.append(dependencyLevel)
            Debug.printNoPriority("Dependency level ",dependencyLevel," has been added to clause ",self)

        return len(self.dependencyLevels)

