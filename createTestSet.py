from src.Material import Material
from src.XmlHandler import XmlHandler
import random

def createTestSet(filename : str, size : int, minDeps : int, maxDeps, maxChars : int, relationships : [str]):
    
    # Creating list of materials
    materialList = []
    for materialNum in range(size):
        material = Material(str(materialNum))
        

        numDeps = random.randint(minDeps,maxDeps)
        for dep in range(numDeps):
            depName = random.randint(0,size-1)
            material.addDependency([[None,str(depName)],relationships[random.randint(0,len(relationships)-1)]])

        numChars = random.randint(0,maxChars)
        for char in range(numChars):
            material.addTags([str(random.randint(0,maxChars))]) 
        materialList.append(material)

    XmlHandler.createXmlFile(filename,materialList)



def createQuerySet(filename : str, size : int, numChars : int):
    # Creating list of materials
    materialList = []
    for materialNum in range(size):
        material = Material(str(materialNum))
        
        for char in range(numChars):
            material.addTags([str(random.randint(0,numChars))]) 
        materialList.append(material)

    # Setting deps for material 0
    for dep in range(1,size):
        if dep % 4 == 0:        
            materialList[0].addDependency([[None,str(dep)],"requires"])
        else:
            materialList[0].addDependency([[None,str(dep)],"optional"])


    XmlHandler.createXmlFile(filename,materialList)


def sameNameTest(filename : str):
    

    material0 = Material("0",["3"])
    material0.addDependency([[None,"0"],"3req"])
    material1 = Material("1",[])

    materialList = [material0,material1]

    XmlHandler.createXmlFile(filename,materialList)


# createQuerySet("query401",401,12)
# createQuerySet("query801",801,12)
# createTestSet("test25",25,0,12,10,["a","b","c","d","e"])
# createTestSet("test50",50,0,12,10,["a","b","c","d","e"])
# createTestSet("test75",75,0,12,10,["a","b","c","d","e"])
# createTestSet("test100",100,0,12,10,["a","b","c","d","e"])
# createTestSet("test125",125,0,12,10,["a","b","c","d","e"])
# createTestSet("test150",150,0,12,10,["a","b","c","d","e"])
# createTestSet("test175",175,0,12,10,["a","b","c","d","e"])
# createTestSet("test200",200,0,12,10,["a","b","c","d","e"])
sameNameTest("sameName")