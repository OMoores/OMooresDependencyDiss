import unittest
from src.Utility import *
from src.Material import *

class TestUtility(unittest.TestCase):

    def test_isAinB(self):
        """
            Description: Check the function isAinB correctly returns true or false if item A is in set B

            Expected Result: If item A is in B then returns true, if it is not then returns false
        """

        # Testing on numbers
        list1 = [1,2,3]

        self.assertEqual(Utility.isAinB(1,list1), True)
        self.assertEqual(Utility.isAinB(4,list1), False)
        self.assertEqual(Utility.isAinB(2,list1), True)
        self.assertEqual(Utility.isAinB(0,list1), False)

        # Testing on strings
        list2 = ["String", "Computer", "Lemon"]
        self.assertEqual(Utility.isAinB("String",list2),True)
        self.assertEqual(Utility.isAinB("Lemon",list2),True)
        self.assertEqual(Utility.isAinB("string",list2),False)
        self.assertEqual(Utility.isAinB("ComputerScience",list2),False)

        # Testing on mix of numbers and strings
        list3 = [1,2,"String",4,"Lemon","Matt"]
        self.assertEqual(Utility.isAinB(1,list3),True)
        self.assertEqual(Utility.isAinB(4,list3),True)
        self.assertEqual(Utility.isAinB("String",list3),True)
        self.assertEqual(Utility.isAinB("Lemon",list3),True)
        self.assertEqual(Utility.isAinB("hello",list3),False)
        self.assertEqual(Utility.isAinB("2",list3),True)
        self.assertEqual(Utility.isAinB("4",list3),True)

    def test_isAEquivalentB(self):
        """
        Description: Check if the function isAEquivalentB works properly

        Expected Result: If all items in A are present in B and all in B are present in A returns true, else returns false
        """

        self.assertTrue(Utility.isAEquivalentB([1,2,3],[3,2,1])) # True
        self.assertFalse(Utility.isAEquivalentB([1,2,3],[3,2,2])) # True
        self.assertFalse(Utility.isAEquivalentB([1,2,3],[1,2])) # False

        # Test works with objects
        obj1 = Material("Achim")
        obj2 = Material("David")
        obj3 = Material("Ayah")

        self.assertTrue(Utility.isAEquivalentB([obj1,obj2],[obj2,obj1]))
        self.assertFalse(Utility.isAEquivalentB([obj1,obj2,obj3],[obj2,obj1]))
    
