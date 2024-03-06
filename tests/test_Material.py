import unittest
from src.Material import *
from src.XmlHandler import *
from src.Recommendations import selectMaterialWithName



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
        """
        Description: Tests the method for Material getDependencies. This method returns a list of pairs of dependencies and their dependency level
        It can take a set of resolvers that are used to resolve any OR statements
        """

        files = XmlHandler.parseXmlFiles(["./tests/testAssets/MathsAndPhys2.xml"])
        self.Mechanics = selectMaterialWithName("Mechanics",files)
        self.Physics = selectMaterialWithName("Physics",files)
        self.Further_Maths = selectMaterialWithName("Further_Maths",files)
        self.Basic_Maths = selectMaterialWithName("Basic_Maths",files)
        self.Subtraction = selectMaterialWithName("Subtraction",files)
        self.Addition = selectMaterialWithName("Addition",files)

        resolvers1 = [[None,"lecture","maths"],["Physics"]]

        dependencies1 = self.Mechanics.getDependencies(resolvers1) # Testing can get and OR dependency correctly
        self.assertEqual(dependencies1,[[self.Physics,"requires"]])

        dependencies2 = self.Basic_Maths.getDependencies()
        self.assertEqual(dependencies2,[[self.Addition,"requires"],[self.Subtraction,"requires"],[self.Further_Maths,"enhancedBy"]])



    def test_extractOperation(self):
        """
        Description: Tests the function resolveOperation, the function should return a list of materials paired with a dependency level.
            his is being tested by parsing it different operations and materials to check they all have the expected return
        """
        
        material1 = Material("maths", ["maths","lecture"])
        operation1 = [None,material1]
        self.assertEqual(extractOperation(operation1, "requires"),[[material1,"requires"]]) # Testing returns basic operation correctly

        operation2 = ["AND",[None,material1],[None,material1]] 
        self.assertEqual(extractOperation(operation2,"requires"),[[material1,"requires"],[material1,"requires"]]) # Testomg returns AND operation correctly

        material2 = Material("english",["english","lecture"])
        operation3 = ["OR",[None,material1],[None,material2]]
        resolvers1 = [[None,"maths","workshop"],[None,"english"]] # This should return material2 over material1
        self.assertEqual(extractOperation(operation3,"requires",resolvers1),[[material2,"requires"]]) # Testing can resolve OR when one material is favoured over another by the resolvers

        self.assertRaises(Exception,extractOperation,operation3,"requires") # Testing returns error when an OR operation does not have any resolvers
        resolvers2 = [[None,"lecture"]]
        self.assertRaises(Exception,extractOperation,operation3,"requires",resolvers2) # Testing returns an error when resolvers are insufficient to support a decision

        operation4 = ["OR",["OR",[None,material1],[None,material2]],[None,material2]]
        resolvers3 = [[None,"maths","lecture"]]
        self.assertEqual(extractOperation(operation4,"requires",resolvers3),[[material1,"requires"]]) # Testing returned stacked ORs correctly

    
    def test_resolveOperation(self): # Requires extractOperation to work as intended
        """
        Description: Tests the function resolveOperation, the function should return a list with an int and a list of materials paired with a dependency level.
            This is being tested by parsing it different operations and materials to check they all have the expected return
        """
        # Testing to check resolves name correctly
        material1 = Material("maths", ["maths","lecture"])
        operation1 = [None,material1]
        resolvers1 = [["maths"]]
        resolvers2 = [[None,"maths","workshop"],["maths"]]
        self.assertEqual(resolveOperation(operation1, "requires", resolvers1),[0,[[material1,"requires"]]])
        self.assertEqual(resolveOperation(operation1, "requires", resolvers2),[1,[[material1,"requires"]]]) # This also checks doesnt resolve partial tag matches

        # Testing to check resolves tags correctly
        resolvers3 = [["moths"],[None,"maths","lecture"]]
        self.assertEqual(resolveOperation(operation1, "requires", resolvers3),[1,[[material1,"requires"]]])

        # Check can resolve operations with OR in 
        material2 = Material("english",["english","lecture"])
        operation2 = ["OR",[None,material1],[None,material2]]
        self.assertEqual(resolveOperation(operation2,"requires",resolvers3),[1,[[material1,"requires"]]])

        

    