import unittest
from src.Material import *


class TestMaterial(unittest.TestCase):

    def test_initialiseMaterial(self):
        """
            Description: Creating materials and checking they initialised properly

            Expected result: Objects initialised properly with all names, tags and dependencies properly initialised (dependency not implemented yet)
        """

        material1 = Material("bob")
        material2 = Material("")

        self.assertEqual(material1.name,"bob")
        self.assertEqual(material2.name, "")

        material3 = Material("achim", ["computer science", "dissertation"])

        self.assertEqual(material3.name, "achim")
        self.assertEqual(material3.tags, ["computer science", "dissertation"])

    def test_setName(self):
        """
            Description: Testing that setName works as intended

            Expected result: When setName is used on an object its name returns as the value the name is set as
        """

        material4 = Material("Bob")
        self.assertEqual(material4.name, "Bob")
        material4.setName("David Wakeling")
        self.assertEqual(material4.name, "David Wakeling")

    def test_addTags(self):
        """
            Description: Testing that addTags works as intended

            Expected result: When addTags is called the list of tags of an object includes any new tags, duplicate tags are not added
        """
        material5 = Material("Matt Collinson", ["Man"])
        self.assertEqual(material5.tags, ["Man"])

        # Testing adding new tags
        material5.addTags(["Computer science", "HTML"])
        self.assertEqual(material5.tags, ["Man","Computer science", "HTML"])

        # Testing adding tags that already exist
        material5.addTags(["Man", "CSS", "HTML", "Computer science"])
        self.assertEqual(material5.tags, ["Man","Computer science", "HTML", "CSS"])


        

    