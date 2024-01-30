from os import error, name
import unittest
from uu import Error
from src.XmlHandler import *
from src.Utility import *

class TestParseXmlFiles(unittest.TestCase):

    def test_parseSingleXml(self):
        """
            Description: Parse in a single xml file and check the objects returned are correct

            Expected result: Returns 3 objects: 4,5,6 with the appropriate tags and dependencies 
        """
        

        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/456.xml"])

        # Material names should be [4,5,6]
        self.assertEqual(materials[0].name,'4')
        self.assertEqual(materials[1].name,'5')
        self.assertEqual(materials[2].name,'6')

        # Checking tags
        self.assertEqual(materials[0].tags,['2','4','3','6'])
        self.assertEqual(materials[1].tags,['5'])
        self.assertEqual(materials[2].tags,['6'])

        # Checking dependencies 
        self.assertEqual(materials[0].dependencies, [materials[2]])
        self.assertEqual(len(materials[1].dependencies), 0)
        self.assertEqual(len(materials[2].dependencies), 0)




    def test_parseMultipleXml(self):
        """
            Description: Parse in 2 xml files and check the objects returned are correct

            Expected result: Returns 6 objects: 1,2,3,4,5,6 with the appropriate tags and dependencies
        """

        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/123.xml","./tests/testAssets/456.xml"])

        # Material names should be [1,2,3,4,5,6]
        self.assertEqual(materials[0].name,'1')
        self.assertEqual(materials[1].name,'2')
        self.assertEqual(materials[2].name,'3')
        self.assertEqual(materials[3].name,'4')
        self.assertEqual(materials[4].name,'5')
        self.assertEqual(materials[5].name,'6')


    def test_parseSingleXmlWithDuplicates(self):
        """
            Description: Parse in an xml file that has 2 of the same named objects

            Expected result: An error is returned with the name of the objects that are in conflict
        """

        with self.assertRaises(Error):
            self.assertRaises(Error ,XmlHandler.parseXmlFiles(["./tests/testAssets/443.xml"]))
        

    def test_parseMultipleXmlWithDuplicates(self):
        """
            Description: Parse 2 xml files, both of these files will have a material with the same name in
            
            Expected result: An error is returned with the name of the objects that are in conflict
        """
        
        with self.assertRaises(Error):
            XmlHandler.parseXmlFiles(["./tests/testAssets/123.xml","./tests/testAssets/34.xml"])

        
    def test_parseSingleEmptyXml(self):
        """
            Description: Parse an empty xml

            Expected result: An error occurs as the xml file is not valid
        """
        

        with self.assertRaises(Error):
            materials = XmlHandler.parseXmlFiles(["./tests/testAssets/empty.xml"])





    def test_parseXmlWithNoExistDep(self):
        """
            Description: Parse an xml that references a file that does not exist

            Expected result: A material is created for this non existant material with the tag "placeholder" and the user is alerted
        """
        
        
        materials = XmlHandler.parseXmlFiles(["./tests/testAssets/123.xml"])

        self.assertEqual(len(materials), 6) # Check correct number of materials created

        # Check materials 1,2,3,4,5,6 all exist 
        matNames = list(map(lambda x : x.name, materials))

        self.assertTrue(len(list(filter(lambda x : x == '1', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '2', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '3', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '4', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '5', matNames))) == 1)
        self.assertTrue(len(list(filter(lambda x : x == '6', matNames))) == 1)




    
