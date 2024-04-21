from src.Utility import Utility
from src.Material import Material
from src.Query import *
from z3 import *

def oldrecommendOrder(materials : [Material], dependencyPriority : [str], resolvers = []) -> [Material]:
    """
    Takes a set of materials and recommends an order to learn the materials in based of the materials 
    dependencies and the priority of the dependency levels

    The first item in the recommendation is the first to learn the last item is the last
    
    Does this using the z3 SAT solver

    Params:
    materials : A set of materials 
    dependencyPriority : A list of dependency levels in order of importance

    Returns:
    A set of materials in a recommended order
    """

    solver = Solver()

    

    depWeb = createDependencyWeb(materials,dependencyPriority, resolvers)

    # Creates a list of empty integers for the z3 solver, these will represent the index of materials
    order = [Int(f'{index}') for index in range(len(materials))]
    # Making sure each material is represented in the order
    for i in range(len(materials)):
        solver.add(order[i] >= 0, order[i] < len(order))
    solver.add(Distinct(order))

    # Making symbolic dependeny web and constraining its values to those in depWeb
    symbolic_depWeb = Array('symbolic_depWeb', IntSort(), IntSort())

    for i in range(len(depWeb)):
        for j in range(len(depWeb[0])):
            symbolic_depWeb = Store(symbolic_depWeb, len(depWeb)*i+j, depWeb[i][j])

    # Looking for materials with no dependencies and put these at the start of the list
    noDepPriority = len(dependencyPriority) # The number that represents not having a dep
    noDependencies = []
    for index in range(0,len(depWeb)):
        if all(element == noDepPriority for element in depWeb[index]): # Testing to see if items are all 
            noDependencies.append(index)
    nextToAssignIndex = 0 # Items with no dependencies are put in the order first, this represents the first index of the recommendation that has not been decided
    # Setting these items with no deps to be first items in recomendation
    for index in noDependencies:
        solver.add(order[index] == noDependencies[index])
        nextToAssignIndex = index+1

    # Setting constraints for the rest of the recommendation 
    for i in range(len(depWeb)-1,nextToAssignIndex-1,-1):
        for j in range(len(depWeb)-1,i-1,-1):
            solver.add(symbolic_depWeb[order[i] * len(depWeb) + order[j]] >= symbolic_depWeb[order[j] * len(depWeb) + order[i]])

    solver.check()
    model = solver.model()
    order_values = [model[i].as_long() for i in order]
    return_materials = [materials[order_values[i]] for i in range(0,len(order_values))]

    return return_materials


def recommendOrder(materials : [Material], dependencyPriority : [str], resolvers = []) -> [Material]:
    """
    Takes a set of materials and recommends an order to learn the materials in based of the materials 
    dependencies and the priority of the dependency levels

    The first item in the recommendation is the first to learn the last item is the last
    
    Does this using the z3 SAT solver

    Params:
    materials : A set of materials 
    dependencyPriority : A list of dependency levels in order of importance
    resolvers : A set of resolvers in the form [[None, tag1, tag2],["Name"]]

    Returns:
    A set of materials in a recommended order
    """

    # Add materials with no dependencies to be first in order
    order = []
    toAddToOrder = [] # Materials that have dependencies and need to be ordered

    dependencyWeb = createDependencyWeb(materials, dependencyPriority, resolvers)

    # Adding materials with no relation to other materials to order
    for index in range(0,len(dependencyWeb)):
        if all(element == len(dependencyPriority) for element in dependencyWeb[index]): # Testing to see if items are all same
            order.append(materials[index])
        else:
            toAddToOrder.append(materials[index])

    dependencyWeb = createDependencyWeb(toAddToOrder, dependencyPriority, resolvers)

    # An array of all the materials that each material must be after -> If the array is [[1,2]] then material 0 must come after 1 and 2
    afterArrays = []
    for materialIndex in range(0,len(dependencyWeb)):
        afterArray = [] # The after array for a single material
        for index in range(0,len(dependencyWeb)):
            if dependencyWeb[materialIndex][index] < dependencyWeb[index][materialIndex]: # If this is true then the material represented by materialIndex must come after the material represented by index
                afterArray.append(index)
        afterArrays.append(afterArray)

    # Using z3 to create an order
    solver = Solver()
    # Making a symbolic reperesentation of each afterArray for each material
    symbolic_positionArray = [Int(f'pos_{i}') for i in range(len(afterArrays))] # Stores the position of each material in the order
    
    # Making sure each item in the position array is unique and within bounds
    for i in range(len(symbolic_positionArray)):
        solver.add(symbolic_positionArray[i] >= 0, symbolic_positionArray[i] < len(symbolic_positionArray))
    solver.add(Distinct(symbolic_positionArray))

    for index in range(len(afterArrays)):
        for material in range(len(afterArrays[index])): # Setting "material must be after materials in its after array" constraints
            solver.add(symbolic_positionArray[index] > symbolic_positionArray[afterArrays[index][material]])

    solver.check()
    model = solver.model()
    positionValues = [model[i].as_long() for i in symbolic_positionArray]

    # Adding items to order using position values
    newOrder = [None for i in range(len(toAddToOrder))] 
    for index in range(len(positionValues)):
        newOrder[positionValues[index]] = toAddToOrder[index]

    order = order + newOrder

    return order



        

    
    
        
                       





    
    

def isRecommendationValid(recommendation : [Material], dependencyPriority : [str], depWeb = None, resolvers = []) -> bool:
    """
    Takes a set of materials and returns if the order they are in is a valid order to recommend the materials in

    Params:
    recommendation : A set of materials in order recommended
    dependencyPriority : A list of dependency levels in order of importance
    depWeb : A dependency web, is optional and can be used to reduce processing required when checking in a function that alraedy has a dependency web

    Returns: 
    A boolean representing if the recommendation is valid
    """

    if depWeb == None:
        depWeb = createDependencyWeb(recommendation, dependencyPriority,resolvers)


    for matAIndex in range(0,len(recommendation)):


        # If material A recommends materials B... then material B... must recommend or enhance A
        for matBIndex in range(matAIndex+1,len(recommendation)):
            AdepB = depWeb[matAIndex][matBIndex]
            BdepA = depWeb[matBIndex][matAIndex]

            # If B depends on A more then A depends on B recommendation is not valid
            if not AdepB <= BdepA:
                return False
            
    return True
    
            



        



def createDependencyWeb(materials : [Material], dependencyPriority : [str], resolvers = []) -> [[int]]: 
    """
    Creates a datastructure that shows the indirect dependency level of every material on every other material

    Params:
    materials :  A set of materials 
    dependencyPriority : A list of dependency levels in order of importance

    Returns:
    A list of lists showing the dependency priority of each material on every other material.
    Only includes material in the original set of material.
    [[0,1,2],[2,2,1],[2,2,2]] Example return, each number represents a position in dependency priority and if there is no indirect relationship then the number is the len(dependencyPriority).
    """
    
    web = []

    # Finding the indirect dependencies of every material
    for matIndex in range(0,len(materials)):
        matDepArray = []

        indirectDeps = findIndirectDependencyLevels(materials[matIndex],dependencyPriority, resolvers)      

        # Ordering the dependencies 
        for orderIndex in range(0,len(materials)):
            if matIndex == len(matDepArray): # If we are trying to find the dependency of a material on itself then add None, as a material is not dependent on itself
                matDepArray.append(len(dependencyPriority))
                continue
            # Find the dep level of material material[orderIndex]
            matDepArray.append(findDepPriority(materials[orderIndex].name,indirectDeps,dependencyPriority))


    
        web.append(matDepArray)


    return web

            

                



def findIndirectDependencyLevels(material : Material, dependencyPriority : [str], resolvers = []) -> [[Material]]:
    """
    Finds the indirect dependency levels of a material on every other material it is indirectly dependent on.
    
    This function works by querying the material.
    First it queries the material with the highest priority dependency level, finding the materials that have this indirect dependency.
    To find the materials with the next level of dependency query the material with the previous dependency levels AND the new one, materials in this new set that are not in the previous set are the materials with the next level of dependency.

    Params:
    material : The material that is having its indirect dependencies examined
    dependencyPriority : A list of dependency levels in order of highest priority to lowest priority
    resolvers : Used to resolve OR statements
    
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

        currentSet = queryDependencies([material],query,resolvers)
        # Find the items in the new set that arent in the previous itterations
        newItems = Utility.findAnotinB(currentSet,previousSet)
        previousSet = currentSet

        returnList.append(newItems)
  
    return returnList

def findDepPriority(name : str, materials : [[Material]], dependencyPriority : [str]) -> int:
    """
    Takes the return of findIndirectDependencyLevels and a material name and returns the index of the dependency priority

    Params:
    name : A materials name
    materials : A list of materials in sublists dependeing on their dependency prioirty
    dependencyPriority : A list of dependency priorities

    Returns:
    The dependency priority of the material specified, if it is none it is the priority of the last dependency + 1
    """

    for i in range(0,len(materials)):
        # If material is located in list i then it has dependencyPriority[i]
        if selectMaterialWithName(name,materials[i]) != None:
            return i
    return len(dependencyPriority)

        
def selectMaterialWithName(name : str, materials : [Material]) -> Material:
    """
    Takes a set of materials and a name then returns the first material it finds with this name
    """

    for mat in materials:
        if name == mat.name:
            return mat

    return None
    
def printOutMaterials(materials):
    for mat in materials:
        print(mat.name)
        


