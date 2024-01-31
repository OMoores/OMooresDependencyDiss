from numpy import number

from src.Material import Material


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

    def addDependencyLevels(self, dependencyLevels : [str]) -> number:
        """
        Adds a dependency level to the clause
        """
