from ast import MatchStar
from src.Utility import Utility
from src.Material import Material
from src.Query import Clause, Query

def recommendOrder(materials : [Material], dependencyPriority : [str]) -> [Material]:
    """
    Takes a set of materials and recommends an order to learn the materials in based of the materials 
    dependencies and the priority of the dependency levels

    Params:
    materials : A set of materials 
    dependencyPriority : A list of dependency levels in order of importance

    Returns:
    A set of materials in a recommended order
    """
    ...

def isRecommendationValid(recommendation : [Material], dependencyPriority : [str]) -> bool:
    """
    Takes a set of materials and returns if the order they are in is a valid order to recommend the materials in

    Params:
    recommendation : A set of materials in order recommended
    dependencyPriority : A list of dependency levels in order of importance

    Returns: 
    A boolean representing if the recommendation is valid
    """
    
    for matAIndex in range(0,len(recommendation)):


        # If material A recommends materials B... then material B... must recommend or enhance A
        for matBIndex in range(matAIndex+1,len(recommendation)):
            AdepB = findDependenfindcyLevel(recommendation[matAIndex],recommendation[matBIndex],dependencyPriority)
            BdepA = findDependencyLevel(recommendation[matAIndex],recommendation[matBIndex],dependencyPriority)

            # If B depends on A more then A depends on B recommendation is not valid
            if not greaterOrEqualPriority(AdepB,BdepA,dependencyPriority):
                return False
            
    return False
    
            
            



        
def greaterOrEqualPriority(dependencyA : str, dependencyB : str, dependencyPriority : [str]) -> bool:
    """
    Finds if dependencyA is a highter or the same priority as dependencyB then return true, else return false

    Params:
    dependencyA : A dependency level
    dependencyB : A dependency level
    dependencyPriority : A list of dependency levels in order of importance

    Returns:   
    A boolean returning if dependency A is greater than or equal to the priority of B
    """

    if dependencyA == dependencyB:
        return True

    # The index of each dependency in the priority list
    indexA = len(dependencyPriority)
    indexB = -1

    # Finding the index of each dependency in the priority list
    for index in range(0,len(dependencyPriority)):
        if dependencyA == dependencyPriority[index]:
            indexA = index

        if dependencyB == dependencyPriority[index]:
            indexB = index

    if indexA <= indexB:
        return True
    
    return False




def createDependencyWeb(materials : [Material], dependencyPriority : [str]) -> [[str]]: 
    """
    Creates a datastructure that shows the indirect dependency level of every material on every other material

    Params:
    materials :  A set of materials 
    dependencyPriority : A list of dependency levels in order of importance

    Returns:
    A list of lists shwoing the dependency level of each material on every other material in the list

    [[None,requires,recommends],[requires,None,recommends],[requires,requires,None]] Example return. [a][b] -> access mat a dependency on mat b. 
    Only includes materials in original material list in web
    """
    
    web = []

    # Finding the indirect dependencies of every material
    for matIndex in range(0,len(materials)):
        matDepArray = []

        indirectDeps = findIndirectDependencyLevels(materials[matIndex],dependencyPriority)      




        # Ordering the dependencies 
        for orderIndex in range(0,len(materials)):
            if matIndex == len(matDepArray): # If we are trying to find the dependency of a material on itself then add None, as a material is not dependent on itself
                matDepArray.append(None)
                continue
            # Find the dep level of material material[orderIndex]
            matDepArray.append(findDepPriority(materials[orderIndex].name,indirectDeps,dependencyPriority))


    
        web.append(matDepArray)

    print(web)

    return web

            

                



def findIndirectDependencyLevels(material : Material, dependencyPriority : [str]) -> [[Material]]:
    """
    Finds the indirect dependency levels of a material on every other material it is indirectly dependent on.
    
    This function works by querying the material.
    First it queries the material with the highest priority dependency level, finding the materials that have this indirect dependency.
    To find the materials with the next level of dependency query the material with the previous dependency levels AND the new one, materials in this new set that are not in the previous set are the materials with the next level of dependency.

    Params:
    material : The material that is having its indirect dependencies examined
    dependencyPriority : A list of dependency levels in order of highest priority to lowest priority

    Returns:
    A list of lists of materials, each list of material holds the materials with the level of indirect dependency with the dependency of the same index in the dependencyPriority list
    if depPriority is [A,B,C] then [[Materials in this list have an indirect dep of A],...]
    """
    returnList = []
    # This will hold the result of the query in the previous itteration of the loop
    previousSet = []

    for depIndex in range(0,len(dependencyPriority)):
        # Creating the query for this itteration of the loop
        query = Query()
        clause = Clause()
        clause.addVariable(["*"])
        clause.addDependencyLevels(dependencyPriority[:depIndex+1])
        query.addClause(clause)

        currentSet = Query.queryDependencies([material],query)
        # Find the items in the new set that arent in the previous itterations
        newItems = Utility.findAnotinB(currentSet,previousSet)
        previousSet = currentSet

        returnList.append(newItems)
  
    return returnList

def findDepPriority(name : str, materials : [[Material]], dependencyPriority : [str]) -> str|None:
    """
    Takes the return of findIndirectDependencyLevels and a material name and returns the materials dependency priority

    Params:
    name : A materials name
    materials : A list of materials in sublists dependeing on their dependency prioirty
    dependencyPriority : A list of dependency priorities

    Returns:
    The dependency priority of the material specified
    """

    for i in range(0,len(materials)):
        # If material is located in list i then it has dependencyPriority[i]
        if selectMaterialWithName(name,materials[i]) != None:
            return dependencyPriority[i] 
    return None

        
def selectMaterialWithName(name : str, materials : [Material]) -> Material|None:
    """
    Takes a set of materials and a name then returns the first material it finds with this name
    """

    for mat in materials:
        if name == mat.name:
            return mat

    return None
    
                
        


