import unittest
from src.XmlHandler import *
from src.Utility import *
from src.Recommendations import *

class TestRecommendations(unittest.TestCase):

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


    def test_findIndirectDependencyLevels(self):
        """
        Tests the function findIndirectDependencyLevels.
        This function takes a material and a list of dependency levels in order of most to least important and returns a list of lists of materials, with the index of the list corresponding with the dependency levels
        """

        test1Set = findIndirectDependencyLevels(self.Quantum_Physics,["requires","recommends","enhancedBy"])
        self.assertTrue(Utility.isAEquivalentB(test1Set[0],[self.Quantum_Physics,self.Physics,self.Basic_Maths,self.Addition,self.Subtraction]))
        self.assertTrue(Utility.isAEquivalentB(test1Set[1],[self.Further_Maths]))
        self.assertEqual(len(test1Set[2]),0)

        test2Set = findIndirectDependencyLevels(self.Engineering,["requires","recommends","enhancedBy"],[[None,"Physics"]]) # Checking works with OR
        self.assertTrue(Utility.isAEquivalentB(test2Set[0],[self.Engineering,self.Mechanics,self.Physics,self.Basic_Maths,self.Addition,self.Subtraction]))
        self.assertTrue(Utility.isAEquivalentB(test2Set[1],[self.Further_Maths]))
        self.assertEqual(len(test2Set[2]),0)


    def test_createDependencyWeb(self):
        """
        Tests the function createDependencyWeb.
        """
        test1Set = createDependencyWeb([self.Mechanics,self.Physics,self.Further_Maths,self.Addition],["requires","recommends","enhancedBy"],[[None,"Maths"]])
        self.assertEqual(test1Set, [[3,3,0,0],[3,3,2,0],[3,3,3,0],[3,3,3,3]])
    
  
        
    def test_isRecommendationValid(self):
        """
        Tests the function isRecommendationValid
        """
        dependencyPriority = ["requires","recommends","enhancedBy"]

        validSet1 = [self.Further_Maths,self.Basic_Maths,self.Addition,self.Subtraction]
        self.assertTrue(isRecommendationValid(validSet1,dependencyPriority,resolvers=[])) # Testing it works with a set with no OR operations


        orSet1 = [self.Mechanics,self.Physics,self.Basic_Maths]
        self.assertTrue(isRecommendationValid(orSet1,dependencyPriority,resolvers=[[None,"Physics"]]))
        self.assertTrue(isRecommendationValid(orSet1,dependencyPriority,resolvers=[[None,"Maths"]]))

        invalidSet1 = [self.Engineering,self.Basic_Maths,self.Further_Maths]
        self.assertFalse(isRecommendationValid(invalidSet1,dependencyPriority,resolvers=[[None,"Physics"]]))
                        
    

    def test_recommendOrder(self):
        """
        Tests the function recommendOrder
        """
        dependencyPriority = ["requires","recommends","enhancedBy"]

        material1Set = [self.Addition,self.Subtraction,self.Basic_Maths,self.Further_Maths,self.Quantum_Physics,self.Mechanics,self.Engineering]
        resolvers = [[None,"Physics"]]
        test1Set = recommendOrder(material1Set, dependencyPriority,resolvers)
        printOutMaterials(test1Set)
        self.assertTrue(isRecommendationValid(test1Set,dependencyPriority,resolvers = resolvers))


        
        

        

        

        
        