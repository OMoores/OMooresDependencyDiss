from pydoc import resolve
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

    def test_resolutionLevel(self):
        """
            Description: Testing the function resolutionLevel, this function is called on a material and takes a set of tags or names. 
                If the material has any of the sets of tags or the same name then returns the index of the resolver it resolves at
        """

        # Checking can resolve name and tags
        material1 = Material("maths", ["maths","lecture"])
        resolution1 = material1.resolutionLevel([[None,"maths","lecture"]]) # Can resolve tag
        self.assertEqual(resolution1,0)
        resolution2 = material1.resolutionLevel([[None,"maths","workshop"],["further_maths"],[None,"maths","lecture"]]) # Can resolve tag, doesnt resolve partial tag match 
        self.assertEqual(resolution2,2)
        resolution3 = material1.resolutionLevel([["maths"]]) # Can resolve name
        self.assertEqual(resolution3,0)
        resolution4 = material1.resolutionLevel([["english"],[None,"maths","workshop"],["maths"]]) # Can resolve name, not at first item in list
        self.assertEqual(resolution4,2)
        resolution5 = material1.resolutionLevel([["english"],[None,"maths","workshop"]]) # Check not matching works
        self.assertEqual(resolution5,None)

    def test_getDependencies(self):
        ...
    
    def test_resolveOperation(self):
        
        # Testing to check resolves name correctly
        material1 = Material("maths", ["maths","lecture"])
        operation1 = [None,material1]
        resolvers1 = [["maths"]]
        resolvers2 = [[None,"maths","workshop"],["maths"]]
        self.assertEqual(resolveOperation(operation1, "requires", resolvers1),[[0],[material1,"requires"]])
        


        

    