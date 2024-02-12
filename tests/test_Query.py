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


        """ Creating queries for use in tests """
        self.queryForAllMats = Query() # Queries for all materials
        self.queryForAllMats.addClause(self.allMatClause)

        self.queryForRecommendsOrLecture = Query() 
        self.queryForRecommendsOrLecture.addClauses([self.allRecommendsClause,self.allLecturesClause])

        self.queryForRecommendsORMathsANDLecture = Query()
        self.queryForRecommendsORMathsANDLecture.addClauses([self.allRecommendsClause,self.mathsAndLectureClause])

        self.queryForMathsANDLectureORNOTLecture = Query()
        self.queryForMathsANDLectureORNOTLecture.addClauses([self.mathsAndLectureClause,self.allNotLecturesClause])
        


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
            Description: Test the function isQueryValid, this function takes a material and its dependency level along with a query and returns if the material and dependency is valid for this query

            dependency -> [material : Material, dependency level : str]

            Expected results: The function returns true for valid materials and false for invalid ones
        """

        # Test a material to check it is any material - True
        test1 = Query.isQueryValid([self.mathsLectureMat,"Requires"],self.queryForAllMats)
        self.assertTrue(test1)

        # Test if a Recommended workshop is recommended OR a lecture - True
        test2 = Query.isQueryValid([self.mathsWorkshopMat,"Recommends"],self.queryForRecommendsOrLecture)
        self.assertTrue(test2)

        # Test if a Required workshop is recommended OR a lecture - False
        test3 = Query.isQueryValid([self.mathsWorkshopMat,"Recommends"],self.queryForRecommendsOrLecture)
        self.assertFalse(test3)

        # Test if a Required lecture is recommended or a lecture - True
        test4 = Query.isQueryValid([self.mathsLectureMat,"Requires"],self.queryForRecommendsOrLecture)
        self.assertTrue(test4)
        
        # Test if a required maths lecture is recommended OR maths AND a lecture - True
        test5 = Query.isQueryValid([self.mathsLectureMat,"Requires"],self.queryForRecommendsORMathsANDLecture)
        self.assertTrue(test5)

        # Test if a required maths workshop is recommended OR maths AND a lecture - False
        test6 = Query.isQueryValid([self.mathsWorkshopMat,"Requires"],self.queryForRecommendsORMathsANDLecture)
        self.assertFalse(test6)

        # Test if a required maths lecture is maths AND a lecture OR not a lecture - True
        test7 = Query.isQueryValid([self.mathsLectureMat,"Requires"],self.queryForMathsANDLectureORNOTLecture)
        self.assertTrue(test7)

        # Test if a physics lecture is maths AND a lecture OR not a lecture - False
        test8 = Query.isQueryValid([self.physicsLectureMat,"Requires"],self.queryForMathsANDLectureORNOTLecture)
        self.assertFalse(test8)

        # Test if a physics workshop is maths AND a lecture or not a lecture - True
        test9 = Query.isQueryValid([self.physicsWorkshopMat,"Requires"],self.queryForMathsANDLectureORNOTLecture)
        self.assertTrue(test9)
       




    def test_isDependencyValid(self):
        """
            Description: Test the isDependencyValid function, tests a dependency level against a clause to see if the dependency is in the clause

            Expected results: The function returns true when the dependency is present in the clause and false when it is not
        """

        # Testing if a recommended material is recommended - True
        test1 = Query.isDependencyValid("Recommends", self.allRecommendsClause)
        self.assertTrue(test1)

        # Testing if a required material is required - False
        test2 = Query.isDependencyValid("Requires",self.allRecommendsClause)
        self.assertFalse(test2)

        # Testing if a required material is NOT required - False
        test3 = Query.isDependencyValid("Requires", self.allNotRequiresClause)
        self.assertFalse(test3)

        # Testing if a recommended material is NOT required - True
        test4 = Query.isDependencyValid("Recommends", self.allNotRequiresClause)
        self.assertTrue(test4)

        # Testing if a required material is any dependency - True
        test5 = Query.isDependencyValid("Requires", self.allMatClause)
        self.assertTrue(test5)


    def test_findValidMaterials(self):
        """
            Description: Test findValidMaterials function which takes a query and a set of materials and finds all of their valid immediate dependencies

            Expected results: Return the correct sets of materials depending on the query
        """

        # Looking for the all dependencies of the engineering lecture 
        test1 = Query.findValidMaterials([self.engineeringLectureMat],self.queryForAllMats)
        self.assertTrue(Utility.isAEquivalentB(test1, [self.physicsLectureMat,self.mechanicsLectureMat,self.physicsLectureMat]))

        # Looking for all dependencies that are lectures or recommended materials of the engineerinng lecture
        test2 = Query.findValidMaterials([self.engineeringLectureMat],self.queryForRecommendsOrLecture)
        self.assertTrue(Utility.isAEquivalentB(test2,[self.physicsLectureMat,self.mechanicsLectureMat,self.physicsLectureMat]))

        # Looking for all dependencies that are recommended or maths AND a lecture for the mechanics lecture
        test3 = Query.findValidMaterials([self.mechanicsLectureMat],self.queryForRecommendsORMathsANDLecture)
        self.assertTrue(Utility.isAEquivalentB(test3,[self.physicsLectureMat,self.mathsLectureMat]))

        # Looking for all dependencies that are maths AND a lecture or not a lecture of the physics lecture
        test4 = Query.findValidMaterials([self.physicsLectureMat],self.queryForMathsANDLectureORNOTLecture)
        self.assertTrue(Utility.isAEquivalentB(test4,[self.mathsLectureMat,self.physicsWorkshopMat]))


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
