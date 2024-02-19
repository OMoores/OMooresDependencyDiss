from src.XmlHandler import *
from src.Material import *
from src.Query import *

files = XmlHandler.parseXmlFiles(["./TestMaterial/MathsAndPhysics/MathsAndPhys1.xml"])


# Looks for all lectures that are required
queryForAllRequires = Query()
allRequiresClause = Clause()
allRequiresClause.addVariable(["*"])
allRequiresClause.addDependencyLevel("requires")
queryForAllRequires.addClause(allRequiresClause)

# Look for all recommended or required material
queryForRecommendsOrRequires = Query()
allReqOrRecClause = Clause()
allReqOrRecClause.addVariable(["*"])
allReqOrRecClause.addDependencyLevels(["requires","recommends"])
queryForRecommendsOrRequires.addClause(allReqOrRecClause)

# Look for all workshops
queryForAllWorkshops = Query()
allWorkshopClause = Clause()
allWorkshopClause.addVariable(["Workshop"])
allWorkshopClause.addDependencyLevel(["*"])
queryForAllWorkshops.addClause(allWorkshopClause)

# Look for all maths lectures OR workshops
queryForMathsLectureORWorkshop = Query()
mathsLectureClause = Clause()
mathsLectureClause.addVariables([["Maths"],["Lecture"]])
mathsLectureClause.addDependencyLevel("*")
queryForMathsLectureORWorkshop.addClause(mathsLectureClause)
queryForMathsLectureORWorkshop.addClause(allWorkshopClause)


def printMaterialSet(materials : [Material]):
    """
    Takes a set of materials and prints all of the materials
    """

    for mat in materials:
        print(mat.name)

def selectMaterialWithName(name : str, materials : [Material]) -> Material|None:
    """
    Takes a set of materials and a name then returns the first material it finds with this name
    """

    for mat in materials:
        if name == mat.name:
            return mat
    
    return None

# EXECUTING QUERIES ON MATERIAL SET

print("\n-Printing all materials in original set of materials")
printMaterialSet(files)


print("\n-Executing query to find all materials required to learn physics")
physicsMat = selectMaterialWithName("Physics",files)
requiredForPhysicsSet = Query.queryDependencies([physicsMat],queryForAllRequires)
print("-Printing set of materials required to learn physics")
printMaterialSet(requiredForPhysicsSet)

print("\n-Executing query to find all material required or recommended to learn quantum physics")
quantumPhysicsMat = selectMaterialWithName("Quantum_Physics",files)
recReqForQuantumPhysicsSet = Query.queryDependencies([quantumPhysicsMat],queryForRecommendsOrRequires)
print("-Printing out set of materials")
printMaterialSet(recReqForQuantumPhysicsSet)
print("-Selecting and printing all materials in this set that are workshops")
printMaterialSet(Query.searchMaterials(recReqForQuantumPhysicsSet,queryForAllWorkshops))

print("\n-Executing query to find all maths lectures or workshops required to learn quantum physics")
mathsLecORworkshopSet = Query.queryDependencies([quantumPhysicsMat],queryForMathsLectureORWorkshop)
print("-Printing out set of materials")
printMaterialSet(mathsLecORworkshopSet)