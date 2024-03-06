import unittest
from Query import Clause, Query
from src.XmlHandler import *
from src.Utility import *
from src.Recommendations import selectMaterialWithName


class TestQuery(unittest.TestCase):


    def setUp(self):
        self.materials = XmlHandler(["./tests/testAssets/MathsAndPhys1.xml"])
        
        self.Quantum_Physics = selectMaterialWithName("Quantum_Physics",self.files)
        self.Engineering = selectMaterialWithName("Engineering",self.files)
        self.Mechanics = selectMaterialWithName("Mechanics",self.files)
        self.Physics = selectMaterialWithName("Physics",self.files)
        self.Further_Maths = selectMaterialWithName("Further_Maths",self.files)
        self.Basic_Maths = selectMaterialWithName("Basic_Maths",self.files)
        self.Subtraction = selectMaterialWithName("Subtraction",self.files)
        self.Addition = selectMaterialWithName("Addition",self.files)

        self.lectureQuery = Query()
        allLectureClause = Clause()
        allLectureClause.addDependencyLevel("*")
        allLectureClause.addVariable(["*"])
        self.lectureQuery.addClause(allLectureClause)

    def test_queryDependency(self):
        
        Query.queryDependencies()

    def test_isQueryValid(self):
        ...

    def test_isDependencyValid(self):
        ...

    def test_isClauseValid(self):
        ...
    
    def test_isVariableValid(self):
        ...

