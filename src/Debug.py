class Debug:
    """
        Used for debugging, behaviour depends on debug level
    """

    debugLevel = 4
    """
        Levels:
            - 0 : Prints out nothing
            - 1 : Prints out high priority messages
            - 2 : Prints out medium priority messages
            - 3 : Prints out low priority messages
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