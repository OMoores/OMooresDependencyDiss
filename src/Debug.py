class Debug:
    """
        Used for debugging, behaviour depends on debug level
    """

    debugLevel = 0
    """
        Levels:
            - 0 : Prints out nothing
            - 1 : Prints out high priority messages, something has gone wrong
            - 2 : Prints out medium priority messages, something has gone wrong but will not cause problems
            - 3 : Prints out low priority messages, something has been added that already exists
            - 4 : Prints out everything 
    """

    def printHighPriority(*argv):
        if (Debug.debugLevel >= 1):
            Debug.__print(argv)
    def printMediumPriority(*argv):
        if (Debug.debugLevel >= 2):
            Debug.__print(argv)
    def printLowPriority(*argv):
        if (Debug.debugLevel >= 3):
            Debug.__print(argv)
    def printNoPriority(*argv):
        if (Debug.debugLevel >= 4):
            Debug.__print(argv)
    def __print(*argv):
        print(''.join(map(str, argv[0])))