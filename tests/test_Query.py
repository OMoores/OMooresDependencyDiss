from pydoc import classify_class_attrs
import unittest
from src.Utility import Utility
from src.Query import Clause, Query
from src.XmlHandler import XmlHandler
from src.Material import Material


class TestQuery(unittest.TestCase):

    def setUp(self):
        # Setting up a set of materials that are dependent on eachother

        # Making materials
        self.physicsLectureMat = Material("PhysicsLecture",["Physics","Lecture"])
        self.physicsWorkshopMat = Material("PhysicsWorkshop",["Physics","Workshop"])
        self.mathsLectureMat = Material("MathsLecture",["Maths","Lecture"])
        self.mathsWorkshopMat = Material("MathsWorkshop",["Maths","Workshop"])
        self.mechanicsLectureMat = Material("MechanicsLecture",["Maths","Physics","Mechanics","Lecture"])
        self.engineeringLectureMat = Material("EngineeringLecture",["Engineering","Lecture"])

        # Adding engineering lecture dependencies
        self.engineeringLectureMat.addDependency(self.physicsWorkshopMat,"Recommends")
        self.engineeringLectureMat.addDependency(self.physicsLectureMat,"Requires")
        self.engineeringLectureMat.addDependency(self.mechanicsLectureMat,"EnhancedBy")

        # Adding physics lecture dependencies
        self.physicsLectureMat.addDependency(self.physicsWorkshopMat,"EnhancedBy")
        self.physicsLectureMat.addDependency(self.mathsLectureMat,"Requires")
        self.physicsLectureMat.addDependency(self.mechanicsLectureMat,"Requires")

        # Adding mechanics lecture dependencies
        self.mechanicsLectureMat.addDependency(self.physicsLectureMat,"Recommends")
        self.mechanicsLectureMat.addDependency(self.mathsLectureMat,"Requires")

        # Adding physics workshop dependencies
        self.physicsWorkshopMat.addDependency(self.physicsLectureMat,"Requires")
        self.physicsWorkshopMat.addDependency(self.mathsLectureMat,"Requires")

        # Adding maths lecture dependencies
        self.mathsLectureMat.addDependency(self.mathsWorkshopMat,"Recommends")

        # Adding maths workshop dependencies
        self.mathsWorkshopMat.addDependency(self.mathsLectureMat,"Requires")


        """ Creating clauses for use in tests """
        self.allMatClause = Clause() # Looks for all materials
        self.allMatClause.addDependencyLevel("*")
        self.allMatClause.addVariable(["*"])

        self.allRecommendsClause = Clause() # Looks for all recommended material
        self.allRecommendsClause.addDependencyLevel("Recommends")
        self.allRecommendsClause.addVariable(["*"])

        self.allLecturesClause = Clause() # Looks for all lectures
        self.allLecturesClause.addDependencyLevel("*")
        self.allLecturesClause.addVariable(["Lecture"])

        self.allNotRequiresClause = Clause() # Looks for all materials that are not required
        self.allNotRequiresClause.addDependencyLevel("-Requires")
        self.allNotRequiresClause.addVariable(["*"])

        self.allNotLecturesClause = Clause() # Looks for all materials that are not lectures
        self.allNotLecturesClause.addDependencyLevel("*")
        self.allNotLecturesClause.addVariable(["-Lecture"])

        self.allReqRecClause = Clause() # Looks for all required or recommended materials
        self.allReqRecClause.addDependencyLevels(["Requires","Recommends"])
        self.allReqRecClause.addVariable(["*"])

        self.allLectureWorkshopClause = Clause() # Looks for all materials that are lectures or workshops
        self.allLectureWorkshopClause.addDependencyLevel("*")
        self.allLectureWorkshopClause.addVariables([["Lecture"],["Workshop"]])
        
        self.mathsAndLectureClause = Clause()
        self.mathsAndLectureClause.addDependencyLevel("*")
        self.mathsAndLectureClause.addVariable([""])

        


        def test_addTags(self):
            """
                Description: Create clauses and test that tags are added correctly

                Expected result: Correct tags are added 
            """
            
            clause = Clause()

            # Test adding no tag to an empty clause
            clause.addVariables([])
            self.assertEqual(clause.variables, [])
            # Test adding a single tag
            clause.addVariables([["Apple"]]) 
            self.assertEqual(clause.variables,[["Apple"]])
            # Testing adding multiple tags
            clause.addVariables([["Bannana","Pear"]])
            self.assertEqual(clause.variables, [["Apple"],["Bannana","Pear"]])
            # Testing adding no tags
            clause.addVariables([])
            self.assertEqual(clause.variables, [["Apple"],["Bannana","Pear"]])

        

    def test_addDependencyLevel(self):
        """
            Description: Create clause and test that dependency levels are added correctly

            Expected result: Correct dependency levels are added
        """

        clause = Clause()

        # Test adding no dependency level to an empty clause
        clause.addDependencyLevels([])
        self.assertEqual(clause.dependencyLevels, [])
        # Test adding a single dependency level
        clause.addDependencyLevels(["Apple"]) 
        self.assertEqual(clause.dependencyLevels,["Apple"])
        # Testing adding multiple dependency levels
        clause.addDependencyLevels(["Bannana","Pear"])
        self.assertEqual(clause.dependencyLevels, ["Apple","Bannana","Pear"])
        # Testing adding no dependency level
        clause.addDependencyLevels([])
        self.assertEqual(clause.dependencyLevels, ["Apple","Bannana","Pear"])

        

    def test_isClauseValid(self):
        """
        Description: Test the function isClauseValid, this function takes a material and its dependency level along with a clause and returns if the material and dependency is valid for this clause
        
        Expected result: The function returns true for all valid materials and false for invalid ones
        """

        # Test required lecture to see if it has * dep and * tags - True
        test1 = Query.isClauseValid(self.allMatClause,[self.mathsLectureMat,"Requires"])
        self.assertTrue(test1)

        # Test Recommends lecture to see if it is recommended - True
        test2 = Query.isClauseValid(self.allRecommendsClause,[self.mathsLectureMat,"Recommends"])
        self.assertTrue(test2)

        # Test Requires lecture to if it is recommended - False
        test3 = Query.isClauseValid(self.allRecommendsClause,[self.mathsLectureMat,"Requires"])
        self.assertFalse(test3)

        # Test Required lecture to see if it is a lecture - True
        test4 = Query.isClauseValid(self.allLecturesClause,[self.mathsLectureMat,"Requires"])
        self.assertTrue(test4)

        # Test Required workshop to see if it is a workshop - False
        test5 = Query.isClauseValid(self.allLecturesClause,[self.mathsWorkshopMat,"Requires"])
        self.assertFalse(test5)

        # Test Required workshop to see if it is not a lecture - True
        test6 = Query.isClauseValid(self.allNotLecturesClause,[self.mathsWorkshopMat,"Requires"])
        self.assertTrue(test6)

        # Test Required lecture to see if it is not a lecture - False
        test7 = Query.isClauseValid(self.allNotLecturesClause,[self.mathsLectureMat,"Requires"])
        self.assertFalse(test7)





    def test_isQueryValid(self):
        """
            Description: Test the function isMaterialValid, this function takes a material and its dependency level along with a query and returns if the material and dependency is valid for this query

            dependency -> [material : Material, dependency level : str]

            Expected results: The function returns true for valid materials and false for invalid ones
        """



    def test_isDependencyValid(self):
        """
            Description: Test the isDependencyValid function, tests a dependency against a clause to see if the dependency is in the clause

            Expected results: The function returns true when the dependency is present in the clause and false when it is not
        """







    def test_findValidMaterials(self):
        """
            Description: Test findValidMaterials function which takes a query and a set of materials and finds all of their valid immediate dependencies

            Expected results: Return the correct sets of materials depending on the query
        """



    def test_queryDependencies(self):
        """
            Description: Testing the function queryDependencies by giving it a set of materials and a query then checking it returns the correct set of dependencies

            Expected results: The function returns the correct set of materials based on the query and materials it is given
        """



    def test_searchMaterials(self):
        """
            Description: Testing the function searchMaterials by giving it a set of materials and a query then checking it returns the correct set of materials

            Expected results: The function returns the correct set of materials based on the query and the materials it is given, unlike queryDependencies searchMaterials selects materials purely based upon tags and does not look at dependencies 
        """
