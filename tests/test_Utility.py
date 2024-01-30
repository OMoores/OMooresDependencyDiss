import unittest
from src.Utility import *

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

