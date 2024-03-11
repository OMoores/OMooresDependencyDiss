import unittest
from src.XmlHandler import *
from src.Utility import *

class TestParseXmlFiles(unittest.TestCase):

    def test_parseSingleXml(self):
        """
            Description parses an XML file and makes sure all tags and dependencies are present
        """
        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/simpleXml.xml"])
        
        # Looking at material 0 (physics) 
        self.assertEqual(materials[0].dependencies[0],[["OR",[None,materials[1]],["AND",[None,materials[2]],[None,materials[3]]]],"requires"]) 
        self.assertEqual(materials[0].dependencies[1],[[None,materials[4]],"requires"])
        self.assertEqual(materials[0].tags,["lecture"])
                         
        # Looking at material 1 (english_lit)
        self.assertEqual(materials[1].dependencies[0],[[None,materials[2]],"requires"])
        self.assertEqual(materials[1].tags,["lecture","bad"])




        
        
    def test_parseSingleEmptyXml(self):
        """
            Description: Parse an empty xml

            Expected result: An error occurs as the xml file is not valid
        """
        

        with self.assertRaises(Exception):
            materials = XmlHandler.parseXmlFiles(["./tests/testAssets/empty.xml"])


    def test_parseMultipleXml(self):
        """
            Description: Parse 2 xml files that contain references to each other

            Expected result: The objects created should correctly reference each other even if from different files
        """

        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/multiXml1.xml","./tests/testAssets/multiXml2.xml"])

        self.assertEqual(materials[0].name,"english_lit")
        self.assertEqual(materials[1].name,"science")
        self.assertEqual(materials[2].name,"english_lang")

        self.assertEqual(materials[0].dependencies[0][0][1],materials[2])
        self.assertEqual(materials[1].dependencies[0][0][1],materials[2])



    def test_parseWrongOrderXml(self):
        """
        Description: Parse an xml that does not have its tags in the order fileName, tags, dependencies in a material

        Expected result: Should parse like normal
        """

        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/wrongOrder.xml"])

        self.assertEqual(len(materials), 3)

        matNames = list(map(lambda x : x.name, materials))
        
        self.assertTrue(len(list(filter(lambda x : x == 'Addition', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == 'Subtraction', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == 'Basic_Maths', matNames))) == 1)


    def test_getTempDep(self):
        """
        Description: Test the function getTempDep. This function should return a list of formatted dependencies
        """

        tree = etree.parse("./tests/testAssets/testCreateOperation.xml")
        root = tree.getroot()

        test1Set = XmlHandler.getTempDep(root)

        self.assertEqual(test1Set,[[[None,"basic_maths"],"requires"],[["OR",[None,"basic_maths"],[None,"basic_english"]],"requires"],[["OR",["AND",[None,"basic_maths"],[None,"advanced_maths"]],[None,"computer_science"]],"requires"]])

        

    def test_createDependency(self):
        """
        Description: Tests the function createDependency, this function takes an element inside a dependency level element (OR,AND or material) and turns it into a dependency
        """

        # Preparing to read testCreateOperation.xml -> Does not have full structure in so cant use parseXmlFiles
        tree = etree.parse("./tests/testAssets/testCreateOperation.xml")
        root = tree.getroot()[0]

        # Testing to see if can create an operation for requiring a material with no operators
        
        test1Root = root[0]
        test1Result = XmlHandler.createDependency(test1Root)
        self.assertEqual(test1Result,[[None,"basic_maths"],"requires"])

        test2Root = root[1]
        test2Result = XmlHandler.createDependency(test2Root)
        self.assertEqual(test2Result,[["OR",[None,"basic_maths"],[None,"basic_english"]],"requires"])

        test3Root = root[2]
        test3Result = XmlHandler.createDependency(test3Root)
        self.assertEqual(test3Result,[["OR",["AND",[None,"basic_maths"],[None,"advanced_maths"]],[None,"computer_science"]],"requires"])
                                                                    
 

