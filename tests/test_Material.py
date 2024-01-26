import unittest
from importlib.machinery import SourceFileLoader
from src.Material import *


class TestMaterial(unittest.TestCase):

    def test_initialiseMaterial(self):
        """
            Description: Creating materials and checking they initialised properly

            Expected result: Objects initialised properly with all names, tags and dependencies properly initialised (dependency not implemented yet)
        """

        material1 = Material("bob")

        self.assertEqual(material1.name,"bob")

    def setName():
        ...

    def setNameList():
        ...

    def addTag():
        ...

    def addTags():
        ...

    def addDuplicateTags():
        ...

    def addNoTags():
        ...

    