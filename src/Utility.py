
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

