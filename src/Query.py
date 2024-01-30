class Query:
    """
        This class will hold a query, when a query is given to the solver the solver returns a set of materials based on the query
    """

    def __init__(self):
        """
            Creates a query

            Attributes:
                - Material set
                - Dependency req
                - And or not 
        """

        self.dependencyLevels = [] 
        """ The levels of dependency this clause applies to"""
        

