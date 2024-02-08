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

        # Query looking for all materials
        self.allMatsQuery = Query()
        self.allMatClause = Clause()
        self.allMatClause.addDependencyLevel("*")
        self.allMatClause.addVariable(["*"])
        self.allMatsQuery.addClause(self.allMatClause)

        # Query looking for all required materials
        self.allRequiredMatsQuery = Query()
        self.allRequiredClause = Clause()
        self.allRequiredClause.addDependencyLevel("Requires")
        self.allRequiredClause.addVariable(["*"]) # * means all tags -> Will accept any tag
        self.allRequiredMatsQuery.addClause(self.allRequiredClause)

        # A query looking to select all required and recommended materials
        self.allRecommendedMatsQuery = Query()
        self.allRecommendedClause = Clause()
        self.allRecommendedClause.addDependencyLevel("Recommends")
        self.allRecommendedClause.addDependencyLevel("Requires")
        self.allRecommendedClause.addVariable(["*"])
        self.allRecommendedMatsQuery.addClauses([self.allRecommendedClause])

        # A query looking for all required lectures
        self.allRequiredLecturesQuery = Query()
        self.lectureClause = Clause()
        self.lectureClause.addVariable(["Lecture"])
        self.lectureClause.addDependencyLevel(["*"]) # * will accept any dependency level
        self.allRequiredLecturesQuery.addClauses([self.lectureClause,self.allRequiredClause]) # Will look for materials that fulfil the condition "required" AND "lectures"

        # A query looking for all required materials that are not lectures
        self.notLectureQuery = Query()
        self.notLectureClause = Clause()
        self.notLectureClause.addVariable(["-Lecture"]) # The - is a negation of lecture so a material not having a lecture tag will make this variable true
        self.notLectureClause.addDependencyLevel("Requires")
        self.notLectureQuery.addClause(self.notLectureClause)

        # A query looking for all material that is not required
        self.notRequiredQuery = Query()
        self.notRequiredClause = Clause()
        self.notRequiredClause.addVariable(["Lecture"])
        self.notRequiredClause.addDependencyLevel("-Requires") # The - is a negation of Requires so this query will be true only if the dependency level is not requires
        self.notRequiredQuery.addClause(self.notRequiredClause)

        # Query that looks for recommended not lectures and workshops
        self.notLectureAndWorkshopQuery = Query()
        self.recommendedNotLectureClause = Clause()
        self.recommendedNotLectureClause.addVariable(["-Lecture"])
        self.recommendedNotLectureClause.addDependencyLevel("Recommends")
        self.workshopClause = Clause()
        self.workshopClause.addDependencyLevel("*")
        self.workshopClause.addVariable(["Workshop"])

    def test_isMaterialValid(self):
        """
            Description: Test the function isMaterialValid, this function takes a material and its dependency level along with a query and returns if the dependency is valid for this query

            dependency -> [material : Material, dependency level : str]

            Expected results: The function returns true for valid materials and false for invalid ones
        """


        # Testing to see if physics workshop is a required material whilst it is recommended - False
        self.assertFalse(Query.isMaterialValid([self.physicsWorkshopMat,"Recommends"],self.allRequiredMatsQuery))
        
        # Testing to see if a Maths lecture is a required material whilst it is required - True
        self.assertTrue(Query.isMaterialValid([self.mathsLectureMat,"Requires"],self.allRequiredMatsQuery))

        # Testing to see if Mechanics lecture is a required lecture whilst it is required - True
        self.assertTrue(Query.isMaterialValid([self.mechanicsLectureMat,"Requires"],self.allRequiredLecturesQuery))

        # Testing to see if Mechanics lecture is a required lecture whilst it is recommended - False
        self.assertFalse(Query.isMaterialValid([self.mechanicsLectureMat,"Recommends"],self.allRequiredLecturesQuery))

        # Testing to see if maths workshop is a required lecture whilst it is required - False
        self.assertFalse(Query.isMaterialValid([self.mathsWorkshopMat,"Requires"],self.allRequiredLecturesQuery))

        # Testing to see if a maths workshop is a required lecture whilst it is recommended - False
        self.assertFalse(Query.isMaterialValid([self.mathsWorkshopMat,"Recommends"],self.allRequiredLecturesQuery))

        # Testing to see if a required maths lecture is not a lecture and required - False
        self.assertFalse(Query.isMaterialValid([self.mathsLectureMat,"Requires"],self.notLectureQuery))

        # Testing to see if a recommended maths lecture is not a lecture and required - False
        self.assertFalse(Query.isMaterialValid([self.mathsLectureMat,"Recommends"],self.notLectureQuery))

        # Testing to see if a required maths workshop is not a lecture and required - True
        self.assertTrue(Query.isMaterialValid([self.mathsWorkshopMat,"Requires"],self.notLectureQuery))

        # Testing to see if a recommended maths workshop is not a lecture and required - False
        self.assertFalse(Query.isMaterialValid([self.mathsWorkshopMat,"Recommends"],self.notLectureQuery))

        # Testing to see if a required maths lecture is a lecture and not required - False
        self.assertFalse(Query.isMaterialValid([self.mathsLectureMat,"Requires"],self.notRequiredQuery))

        # Testing to see if a recommended maths lecture is a lecture and not required - True
        self.assertTrue(Query.isMaterialValid([self.mathsLectureMat,"Recommends"],self.notRequiredQuery))

        # Testing to see if a recommended maths workshop is a lecture and not required - False
        self.assertFalse(Query.isMaterialValid([self.mathsWorkshopMat,"Recommends"],self.notRequiredQuery))

    def test_isDependencyValid(self):
        """
            Description: Test the isDependencyValid function, tests a dependency against a clause to see if the dependency is in the clause

            Expected results: The function returns true when the dependency is present in the clause and false when it is not
        """

        # Tests Requires to see if it is required - True
        self.assertTrue(Query.isDependencyValid("Requires", self.allRequiredClause))

        # Test Recommends to see if it is required - False
        self.assertFalse(Query.isDependencyValid("Recommends", self.allRequiredClause))

        # Test Requires to see if it is * - True
        self.assertTrue(Query.isDependencyValid("Requires", self.lectureClause))

        # Test Requires to see if it is not requires - False
        self.assertFalse(Query.isDependencyValid("Requires", self.notRequiredClause))

        # Test Recommends to see if it is not requires - True
        self.assertTrue(Query.isDependencyValid("Recommends", self.notRequiredClause))




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

    def test_findValidMaterials(self):
        """
            Description: Test findValidMaterials function which takes a query and a set of materials and finds all of their valid immediate dependencies

            Expected results: Return the correct sets of materials depending on the query
        """

        # For engineering lecture look for all materials - Physics workshop, physics lecture, mechanics
        test1Set = Query.findValidMaterials([self.engineeringLectureMat], self.allMatsQuery)
        self.assertTrue(Utility.isASubsetB(test1Set,[self.physicsLectureMat,self.physicsWorkshopMat,self.engineeringLectureMat]))

        # For engineering lecture look for all required materials - Physics lecture
        test2Set = Query.findValidMaterials([self.engineeringLectureMat], self.allRequiredMatsQuery)
        self.assertTrue(Utility.isASubsetB(test2Set, [self.physicsLectureMat]))

        # For engineering lecture look for required lectures - Physics lecture
        test3Set = Query.findValidMaterials([self.engineeringLectureMat], self.allRequiredLecturesQuery)
        self.assertTrue(Utility.isASubsetB(test3Set,[self.physicsLectureMat]))

        # For engineering lecture look for all materials that are not required - Mechanics lecture, physics workshop
        test4Set = Query.findValidMaterials([self.engineeringLectureMat], self.notRequiredQuery)
        self.assertTrue(Utility.isASubsetB(test4Set, [self.mechanicsLectureMat, self.physicsWorkshopMat]))

        # For engineering lecture look for all materials that arent lectures - Physics workshop
        test5Set = Query.findValidMaterials([self.engineeringLectureMat], self.notLectureQuery)
        self.assertTrue(Utility.isASubsetB(test5Set, [self.physicsWorkshopMat]))

        # For engineering lecture look for all materials that are not workshops that are required and all lectures that are not required - Physics lecture, mechanics lecture
        test6Set = Query.findValidMaterials([self.engineeringLectureMat], self.notLectureAndWorkshopQuery)
        self.assertTrue(Utility.isASubsetB(test6Set,[self.physicsLectureMat,self.mechanicsLectureMat]))

        # For Physics lecture and mechanics lecture look for all materials that are required - Maths lecture
        test7Set = Query.findValidMaterials([self.physicsLectureMat,self.mechanicsLectureMat], self.allRequiredMatsQuery)
        self.assertTrue(Utility.isASubsetB(test7Set,[self.mathsLectureMat]))

        # For maths workshop look for all required materials - None
        test8Set = Query.findValidMaterials([self.mathsWorkshopMat],self.allMatsQuery)
        self.assertEqual(len(test8Set),0)

        # For no materials look for all required materials - None
        test9Set = Query.findValidMaterials([],self.allMatsQuery)
        self.assertEqual(len(test9Set),0)

