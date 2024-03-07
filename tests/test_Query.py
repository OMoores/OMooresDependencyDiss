import unittest
from src.Query import *
from src.XmlHandler import *
from src.Utility import *
from src.Recommendations import selectMaterialWithName


class TestQuery(unittest.TestCase):


    def setUp(self):
        self.files = XmlHandler.parseXmlFiles(["./tests/testAssets/MathsAndPhys2.xml"])
        
        self.Quantum_Physics = selectMaterialWithName("Quantum_Physics",self.files)
        self.Engineering = selectMaterialWithName("Engineering",self.files)
        self.Mechanics = selectMaterialWithName("Mechanics",self.files)
        self.Physics = selectMaterialWithName("Physics",self.files)
        self.Further_Maths = selectMaterialWithName("Further_Maths",self.files)
        self.Basic_Maths = selectMaterialWithName("Basic_Maths",self.files)
        self.Subtraction = selectMaterialWithName("Subtraction",self.files)
        self.Addition = selectMaterialWithName("Addition",self.files)

        self.requiredLectureQuery = Query()
        allLectureClause = Clause()
        allLectureClause.addDependencyLevel("requires")
        allLectureClause.addVariable(["Lecture"])
        self.requiredLectureQuery.addClause(allLectureClause)

        self.requiredMathsAndLectureQuery = Query()
        allMathsAndLectureClause = Clause()
        allMathsAndLectureClause.addDependencyLevel("requires")
        allMathsAndLectureClause.addVariables([["Maths"],["Lecture"]])
        self.requiredMathsAndLectureQuery.addClause(allMathsAndLectureClause)

        self.allMatQuery = Query()
        allMatClause = Clause()
        allMatClause.addDependencyLevel("*")
        allMatClause.addVariable(["*"])
        self.allMatQuery.addClause(allMatClause)

        self.requiredNotMechanicsORLectureQuery = Query()
        mathsClause = Clause()
        mathsClause.addDependencyLevel("requires")
        mathsClause.addVariable(["-Mechanics"])
        self.requiredNotMechanicsORLectureQuery.addClauses([mathsClause,allLectureClause])



    def isDependencyLevelValid(self):
        requiredClause = Clause()
        requiredClause.addDependencyLevel("requires")
        
        recReqClause = Clause()
        recReqClause.addDependencyLevels(["requires","recommends"])

        allClause = Clause()
        allClause.addDependencyLevel("*")

        notRequiredClause = Clause()
        notRequiredClause.addDependencyLevel("-requires")
        
        self.assertTrue(isDependencyLevelValid("requires",requiredClause)) # Testing can recognise a single dep level correctly
        self.assertFalse(isDependencyLevelValid("recommends",requiredClause)) # Testing can reject invalid dependency levels
        self.assertTrue(isDependencyLevelValid("recommends",recReqClause)) # Testing can recognise a dependency level from a clause with multiple dependency levels
        self.assertTrue(isDependencyLevelValid("requires",allClause))
        self.assertFalse(isDependencyLevelValid("requires",notRequiredClause))
        self.assertTrue(isDependencyLevelValid("recommends",notRequiredClause))

    def test_queryDependency(self):
        
        self.assertTrue(Utility.isAEquivalentB(queryDependencies([self.Further_Maths],self.allMatQuery),[self.Further_Maths,self.Basic_Maths,self.Addition,self.Subtraction])) # Checking wildcard works
        self.assertTrue(Utility.isAEquivalentB(queryDependencies([self.Mechanics],self.allMatQuery,[[None,"Maths"]]),[self.Mechanics,self.Further_Maths,self.Basic_Maths,self.Addition,self.Subtraction])) # Test works with OR
        self.assertTrue(Utility.isAEquivalentB(queryDependencies([self.Mechanics],self.allMatQuery,[[None,"Physics"]]),[self.Mechanics,self.Further_Maths,self.Basic_Maths,self.Addition,self.Subtraction,self.Physics])) 
        self.assertTrue(Utility.isAEquivalentB(queryDependencies([self.Engineering],self.requiredNotMechanicsORLectureQuery,[[None,"Physics"]]),[self.Engineering,self.Physics,self.Mechanics,self.Basic_Maths,self.Addition,self.Subtraction]))


    def test_isQueryValid(self):

        self.assertTrue(isQueryValid(self.Basic_Maths,"requires",self.allMatQuery)) 
        self.assertTrue(isQueryValid(self.Addition,"requires",self.requiredNotMechanicsORLectureQuery)) 
        self.assertTrue(isQueryValid(self.Physics,"requires",self.requiredNotMechanicsORLectureQuery))
        self.assertFalse(isQueryValid(self.Addition,"requires",self.requiredMathsAndLectureQuery))
        

    def test_isClauseValid(self):

        allMatClause = Clause()
        allMatClause.addDependencyLevel("*")
        allMatClause.addVariable(["*"])

        notMathsOrLectureClause = Clause()
        notMathsOrLectureClause.addDependencyLevel("requires")
        notMathsOrLectureClause.addVariable(["Workshop,-Maths"])

        mathsAndLectureClause = Clause()
        mathsAndLectureClause.addVariables([["Maths"],["Lecture"]])
        mathsAndLectureClause.addDependencyLevel("requires")

        self.assertTrue(isClauseValid(self.Basic_Maths,"requires",allMatClause))
        self.assertTrue(isClauseValid(self.Basic_Maths,"recommends",allMatClause)) # Checking dep levels work
        self.assertFalse(isClauseValid(self.Addition,"requires",notMathsOrLectureClause)) 
        self.assertFalse(isClauseValid(self.Mechanics,"requires",notMathsOrLectureClause)) # Checking negation works

        # Checking works with multiple Variables
        self.assertTrue(isClauseValid(self.Basic_Maths,"requires",mathsAndLectureClause))
        self.assertFalse(isClauseValid(self.Mechanics,"requires",mathsAndLectureClause))

    def test_isVariableValid(self):

        self.assertTrue(isVariableValid(self.Basic_Maths,["Maths","Lecture"]))
        self.assertFalse(isVariableValid(self.Basic_Maths,["English","Science"])) 
        self.assertTrue(isVariableValid(self.Basic_Maths,["*"])) # Checking works with wildcard
        self.assertTrue(isVariableValid(self.Basic_Maths,["-English"])) # Checking works with negation
        

