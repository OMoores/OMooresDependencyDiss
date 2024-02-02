from pydoc import classify_class_attrs
import unittest
from src.Query import Clause, Query
from src.XmlHandler import XmlHandler
from src.Material import Material


class TestQuery(unittest.TestCase):

    def test_solveSimpleQueryRequired(self):
        """
            Description: Create a query that selects all materials that are required to learn material 1

            Expected result: Returns material 1,2,3,4,5
        """

        # Parse an XML file to get materials
        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/123.xml","./tests/testAssets/456.xml"])

        query = Query() # Create an empty query

        # Create a clause that selects all required dependencies 
        clause = Clause()
        clause.addTags(["*"]) # This should select every tag
        clause.addDependencyLevels(["requires"]) # Select every required dependency
        query.addClauses([clause])

        solved = query.solveQuery() # Returns the list of solved materials

        # Check to see that the correct materials were returned
        self.assertTrue(len(list(filter(lambda x : x == '1', solved))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '2', solved))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '3', solved))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '4', solved))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '5', solved))) == 1)

    def test_solveComplexQueryRequired(self):
        """
            Description: Create a query 
        """

        
        

        


class TestClause(unittest.TestCase):
    """
        Testing clause functionality works as intended
    """

    def test_addTags(self):
        """
            Description: Create clauses and test that tags are added correctly

            Expected result: Correct tags are added 
        """
        
        clause = Clause()

        # Test adding no tag to an empty clause
        clause.addTags([])
        self.assertEqual(clause.tags, [])
        # Test adding a single tag
        clause.addTags(["Apple"]) 
        self.assertEqual(clause.tags,["Apple"])
        # Testing adding multiple tags
        clause.addTags(["Bannana","Pear"])
        self.assertEqual(clause.tags, ["Apple","Bannana","Pear"])
        # Testing adding no tags
        clause.addTags([])
        self.assertEqual(clause.tags, ["Apple","Bannana","Pear"])

        

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