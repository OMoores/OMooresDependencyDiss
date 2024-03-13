from src.Utility import Utility
from src.Material import Material
from src.Query import *
from z3 import *

def recommendOrder(materials : [Material], dependencyPriority : [str], resolvers = []) -> [Material]:
    """
    Takes a set of materials and recommends an order to learn the materials in based of the materials 
    dependencies and the priority of the dependency levels
    
    Does this using the z3 SAT solver

    Params:
    materials : A set of materials 
    dependencyPriority : A list of dependency levels in order of importance

    Returns:
    A set of materials in a recommended order. The first material in the list is the last to learn
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
    
    for i in range(len(depWeb)-1,-1,-1):
        for j in range(len(depWeb)-1,i-1,-1):
            solver.add(symbolic_depWeb[order[i] * len(depWeb) + order[j]] <= symbolic_depWeb[order[j] * len(depWeb) + order[i]])


    solver.check()
    model = solver.model()
    order_values = [model[i].as_long() for i in order]
    return_materials = [materials[order_values[i]] for i in range(0,len(order_values))]

    return return_materials





    
    

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
    A list of lists shwoing the dependency level of each material on every other material in the list

    [[None,requires,recommends],[requires,None,recommends],[requires,requires,None]] Example return. [a][b] -> access mat a dependency on mat b. 
    Only includes materials in original material list in web
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
    
                
        


