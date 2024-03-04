import unittest
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
        self.Further_Maths = selectMaterialWithName("Further_Maths",self.files)
        self.Advanced_Maths = selectMaterialWithName("Advanced_Maths",self.files)
        self.Basic_Maths = selectMaterialWithName("Basic_Maths",self.files)
        self.Subtraction = selectMaterialWithName("Subtraction",self.files)
        self.Addition = selectMaterialWithName("Addition",self.files)


    def test_findIndirectDependencyLevels(self):
        """
        Tests the function findIndirectDependencyLevels.
        This function takes a material and a list of dependency levels in order of most to least important and returns a list of lists of materials, with the index of the list corresponding with the dependency levels
        """

        test1Set = findIndirectDependencyLevels(self.Quantum_Physics,["requires","recommends","enhancedBy"])
        self.assertTrue(Utility.isAEquivalentB([self.Quantum_Physics,self.Physics_Workshop,self.Physics,self.Mechanics,self.Further_Maths,self.Advanced_Maths,self.Basic_Maths],test1Set[0]))
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
        self.assertEqual(0,test1Set)
        test2Set = findDepPriority(self.Basic_Maths.name,levels,depPriorities)
        self.assertEqual(1,test2Set)
        test3Set = findDepPriority(self.Computer_Science.name,levels,depPriorities)
        self.assertEqual(2,test3Set)
        test4Set = findDepPriority(self.Further_Maths,levels,depPriorities) # Testing with a mat not in material set
        self.assertEqual(3,test4Set)

    def test_createDependencyWeb(self):
        """
        Tests the function createDependencyWeb.
        """
        test1Set = createDependencyWeb([self.Quantum_Physics,self.Basic_Maths,self.Coding_Workshop,self.Addition],["requires","recommends","enhancedBy"])
        self.assertEqual(test1Set, [[3,0,1,1],[3, 3,2,1],[3,3,3,3],[3,2,2,3]])
  
        
    def test_isRecommendationValid(self):
        """
        Tests the function isRecommendationValid
        """
        dependencyPriority = ["requires","recommends","enhancedBy",None]

        validSet1 = [self.Mechanics,self.Advanced_Maths,self.Basic_Maths]
        self.assertTrue(isRecommendationValid(validSet1,dependencyPriority))
        validSet2 = [self.Quantum_Physics,self.Physics,self.Further_Maths,self.Basic_Maths,self.Coding_Workshop]
        self.assertTrue(isRecommendationValid(validSet2,dependencyPriority))
                        
        invalidSet1 = [self.Addition,self.Basic_Maths]
        self.assertFalse(isRecommendationValid(invalidSet1,dependencyPriority))
        invalidSet2 = [self.Further_Maths,self.Advanced_Maths,self.Basic_Maths,self.Quantum_Physics]
        self.assertFalse(isRecommendationValid(invalidSet2,dependencyPriority))

    def test_recommendOrder(self):
        """
        Tests the function recommendOrder
        """
        dependencyPriority = ["requires","recommends","enhancedBy",None]

        material1Set = [self.Addition,self.Subtraction,self.Basic_Maths,self.Advanced_Maths,self.Further_Maths,self.Quantum_Physics,self.Mechanics,self.Computer_Science,self.Coding_Workshop,self.Engineering]
        test1Set = recommendOrder(material1Set, dependencyPriority)
        self.assertTrue(isRecommendationValid(test1Set,dependencyPriority))


        material2Set = [self.Quantum_Physics,self.Computer_Science,self.Advanced_Maths,self.Addition,self.Mechanics]
        test2Set = recommendOrder(material2Set,dependencyPriority)
        self.assertTrue(isRecommendationValid(test2Set,dependencyPriority))

        

        

        
        