import unittest
from venv import create
from src.XmlHandler import *
from src.Utility import *
from src.Recommendations import *

class TestRecommendations(unittest.TestCase):

    def setUp(self):

        self.files = XmlHandler.parseXmlFiles(["./tests/testAssets/MathsAndPhys1.xml"])

        self.Quantum_Physics = selectMaterialWithName("Quantum_Physics",self.files)
        self.Computer_Science = selectMaterialWithName("Computer_Science",self.files)
        self.Coding_Workshop = selectMaterialWithName("Coding_Workshop",self.files)
        self.Engineering = selectMaterialWithName("Engineering",self.files)
        self.Physics_Workshop = selectMaterialWithName("Physics_Workshop",self.files)
        self.Mechanics = selectMaterialWithName("Mechanics",self.files)
        self.Physics = selectMaterialWithName("Physics",self.files)
        self.FurtherMaths = selectMaterialWithName("Further_Maths",self.files)
        self.Advanced_Maths = selectMaterialWithName("Advanced_Maths",self.files)
        self.Basic_Maths = selectMaterialWithName("Basic_Maths",self.files)
        self.Subtraction = selectMaterialWithName("Subtraction",self.files)
        self.Addition = selectMaterialWithName("Addition",self.files)

    def test_greaterOrEqualPriority(self):
        """
        Tests the function greaterOrEqualPriority.
        It takes 2 strings and a list of strings and if string 1 is closer or equal distance from the beginning of the list then
        the function returns true
        """

        self.assertTrue(greaterOrEqualPriority("A","B",["A","B","C"]))
        self.assertFalse(greaterOrEqualPriority("B","A",["A","B","C"]))
        self.assertFalse(greaterOrEqualPriority("A","D",["A","B","C"]))

    def findIndirectDependencyLevels(self):
        """
        Tests the function findIndirectDependencyLevels.
        This function takes a material and a list of dependency levels in order of most to least important and returns a list of lists of materials, with the index of the list corresponding with the dependency levels
        """

        test1Set = findIndirectDependencyLevels(self.QuantumPhysics,["requires","recommends","enhancedBy"])
        self.assertTrue(Utility.isAEquivalentB([self.Physics_Workshop,self.Physics,self.Mechanics,self.FurtherMaths,self.Advanced_Maths,self.Basic_Maths],test1Set[0]))
        self.assertTrue(Utility.isAEquivalentB([self.Coding_Workshop,self.Addition,self.Subtraction],test1Set[1]))
        self.assertTrue(Utility.isAEquivalentB([self.Engineering,self.Computer_Science],test1Set[2]))

    def test_findDepPriority(self):
        """
        Tests the function findDepPriority
        This function takes the result of findIndirectDependecyLevels, a set of dep priorities and the name of a material and finds if the material is in the result and if it is what dep level it is
        """

        depPriorities = ["requires","recommends","enhancedBy"]
        levels = [[self.Quantum_Physics,self.Physics],[self.Basic_Maths],[self.Mechanics,self.Coding_Workshop,self.Computer_Science]]

        test1Set = findDepPriority(self.Quantum_Physics.name,levels,depPriorities)
        self.assertEqual("requires",test1Set)
        test2Set = findDepPriority(self.Basic_Maths.name,levels,depPriorities)
        self.assertEqual("recommends",test2Set)
        test3Set = findDepPriority(self.Computer_Science.name,levels,depPriorities)
        self.assertEqual("enhancedBy",test3Set)
        test4Set = findDepPriority(self.FurtherMaths,levels,depPriorities) # Testing with a mat not in material set
        self.assertEqual(test4Set,None)

    def test_createDependencyWeb(self):
        """
        Tests the function createDependencyWeb.
        """

        test1Set = createDependencyWeb([self.Quantum_Physics,self.Basic_Maths],["requires","recommends","enhancedBy"])
        self.assertEqual(test1Set, [[None,"requires"],["enhancedBy",None]])

        test2Set = createDependencyWeb([self.Quantum_Physics,self.Basic_Maths,self.Coding_Workshop,self.Addition],["requires","recommends","enhancedBy"])
        self.assertEqual(test2Set, [[None,"requires","recommends","recommends"],["enhancedBy",None,"enhancedBy","recommends"],[None,None,None,None],["enhancedBy","enhancedBy","enhancedBy",None]])
  
        

