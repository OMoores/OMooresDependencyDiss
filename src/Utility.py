
class Utility:

    def isAinB(A, B : []) -> bool:
        """
            Takes a var and a list then returns true if A is in B and false if it is not, converts all values to str before checking them

            Params:
            - A : A variable 
            - B : A list of variables

            Returns:
            A boolean representing if A is in B
        """

        for item in B:
            if str(A) == str(item):
                return True
            
        return False
    
    def isAEquivalentB(A : [], B : []) -> bool:
        """
        Takes 2 lists A and B and returns true if all A is in B and all B is in A

        Params:
        - A : A list of variables
        - B : A list of variables

        Returns:
        A boolean representing if A is equivalent to B
        """

        for item in A:
            if not Utility.isAinB(item, B):
                return False
        
        for item in B:
            if not Utility.isAinB(item, A):
                return False
        
        return True
    
    def isASubsetB(A : [], B : []) -> bool:
        """
            Takes 2 lists A and B and returns true if A is a subset of B and false if it isn't
        
            Params:
            - A : A list of variables
            - B : A list of variables

            Returns:
            A boolean representing if A is a subset of B
        """

        if len(A) < 1: 
            return True

        subset = True # Assume A is a subset and look for variables in A that aren't in B

        for item in A:
            if not Utility.isAinB(str(item),B):
                return False
            
        return True
    
    def findAnotinB(A : [], B : []) -> []:
        """
            Returns items in A that are not in B
            
            Params:
            - A : A list of variables
            - B : A list of variables

            Returns:
            A list of materials in A that arent in B
        """
        
        unique = []

        for item in A:
            if not Utility.isAinB(str(item), B):
                unique.append(item)
        
        return unique
    
    def turnMatDepIntoText(dependency  : []) -> str:
        """
        Takes a dependency from a material in the form [[opcode, operation, operation],level] and returns the dependency in text form

        Params:
        - dependency : A list representing a dependency

        Returns:
        A string representing the dependency in a human readable form
        """

        returnString = dependency[1] + ": " + Utility.turnOperationIntoText(dependency[0])

        return returnString
    
    def turnOperationIntoText(operation : []) -> str:
        """
        Takes an operation from a dependency in the form [opcode, operation, operation] and returns the operation in text form

        Params:
        - operation : A list representing an operation

        Returns:
        A string representing the operation in a human readable form
        """
        
        if operation[0] == None:
            return operation[1].name
        elif operation[0] == "AND":
            return Utility.turnOperationIntoText(operation[1]) + " AND " + Utility.turnOperationIntoText(operation[2])
        elif operation[0] == "OR":
            return Utility.turnOperationIntoText(operation[1]) + " OR " + Utility.turnOperationIntoText(operation[2])

    def findOrDependencies():
        """
        Takes a list of materials and returns a list of all dependencies that have an OR in them
        """

    
    def findOrDependency():
        ...


