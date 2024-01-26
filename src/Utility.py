class Utility:

    def isAinB(A, B : []) -> bool:
        """
            Takes a var and a list then returns true if A is in B and false if it is not

            Params:
            - A : A variable 
            - B : A list of variables
            Returns:
            A boolean representing if A is in B
        """

        for item in B:
            if A == item:
                return True
            
        return False