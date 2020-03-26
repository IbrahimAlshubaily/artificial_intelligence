import sys
import numpy as np
from queue import *
from collections import deque
import time
import math

class Node:
    def __init__(self, value):
        self.element = value
        self.cost = 0
        self.depth = 0

goalA = [['1' , '2', '3', '4'],
         ['5' , '6', '7', '8'],
         ['9' , 'A' , 'B' , 'C'],
         ['D' , 'E' , 'F' , ' ']]

goalB = [['1' , '2', '3', '4'],
         ['5' , '6', '7', '8'],
         ['9' , 'A' , 'B' , 'C'],
         ['D' , 'F' , 'E' , ' ']]


############################################## Helper Methods ################################


def swap(instance, iOffset, jOffset):
    blankIndex = np.where(instance==' ')
    i = blankIndex[0][0]
    j = blankIndex[1][0]
    
    instance[i][j] = instance[i+iOffset][j+jOffset]
    instance[i+iOffset][j+jOffset] = ' '
    return instance

########## h1 ###############
def misPlacedTiles(instance):
    numOfMisplacedTiles = 0
    for i in range (0, len(instance)):
        for j in range (0, len(instance)):
            if (instance[i][j] != goalA[i][j] and  instance[i][j] != goalB[i][j]):
                numOfMisplacedTiles +=1
    return numOfMisplacedTiles

########### h2 #################
def manhattanDistance(instance):
    distance = 0
    for i in range (0, len(instance)):
        for j in range (0, len(instance)):
            if (instance[i][j].isnumeric()):
                distance += math.fabs(int (instance[i][j]) - ( len(instance) * i  + j + 1))
            elif (instance[i][j] != ' '):
                distance += math.fabs(ord (instance[i][j]) - 55  - ( len(instance) * i  + j + 1))
    return distance


def getMinCostAStar(fringe):
    minCost = 100;
    indexOfMin = 0
    for i in  range (0, len(fringe)):
        cost = fringe[i].cost + fringe[i].depth
        if (cost < minCost):
            minCost = cost
            indexOfMin = i
    return fringe[indexOfMin]


def getMinCostGreedy(fringe):
    minCost = 100;
    indexOfMin = 0
    for i in  range (0, len(fringe)):
        if (fringe[i].cost < minCost):
            minCost = fringe[i].cost
            indexOfMin = i
    return fringe[indexOfMin]


def setCost(instance, hurestic):
    if (hurestic  == 'h1'):
        instance.cost = misPlacedTiles(instance.element)
    elif (hurestic  == 'h2'):
        instance.cost = manhattanDistance(instance.element)
    else:
        print("invalid hurestic")
        exit(0)

    
def getChildren(instance):
    blankIndex = np.where(instance.element == ' ')
    i = blankIndex[0][0]
    j = blankIndex[1][0]
    instances = list()
    if (j < 3):
        newNode = Node(swap(np.copy(instance.element), 0, 1))
        newNode.depth = instance.depth+1
        instances.append(newNode)#right
    if (i < 3):
        newNode = Node(swap(np.copy(instance.element), 1, 0))
        newNode.depth = instance.depth+1
        instances.append(newNode)#down
    if (j > 0):
        newNode = Node(swap(np.copy(instance.element), 0, -1))
        newNode.depth = instance.depth+1
        instances.append(newNode)#left
    if (i > 0):
        newNode = Node(swap(np.copy(instance.element), -1, 0))
        newNode.depth = instance.depth+1
        instances.append(newNode)#up
    return instances


def contains(theList, theChild):
    for val in theList:
        if (np.array_equal(val.element, theChild.element)):
            return True
    return False


def notFound():
    print(-1, 0, 0, 0)
    
########################################## BFS ####################################
def BFS(instance):

    
    numCreated = 0
    numExpanded = 0
    maxFringe = 0

    
    myQ = deque()
    myQ.append(instance)
    visited = list()

    while len(myQ) > 0:

        curr = myQ.popleft()
        #print(curr.element)
        #time.sleep(3)
          
        if (np.array_equal(curr.element, goalA)
            or np.array_equal(curr.element, goalB)):
            print(curr.depth, numCreated, numExpanded, maxFringe)
            return
        
        for child in getChildren(curr):
            if contains(visited, child):
                continue            
            if not contains(myQ, child):
                numCreated+=1
                myQ.append(child)
                #print (len(myQ))
                maxFringe = max (maxFringe, len(myQ))

        numExpanded+=1
        visited.append(curr)

    notFound()


############################################ DFS ##################################
 
def DFS(instance):
    
    numCreated = 0
    numExpanded = 0
    maxFringe = 0
    
    myQ = deque()
    myQ.append(instance)
    
    visited = list()

    while len(myQ) > 0:
        
        curr = myQ.pop()
        #print(curr.element)
        #time.sleep(3)
        
        if (np.array_equal(curr.element, goalA)
            or np.array_equal(curr.element, goalB)):
            print(curr.depth, numCreated, numExpanded, maxFringe)
            return

        numExpanded +=1
        for child in reversed(getChildren(curr)):
            if contains(visited, child):
                continue
            
            if not contains(visited, child):
                numCreated+=1
                myQ.append(child)
                maxFringe = max (maxFringe, len(myQ))

        visited.append(curr)

    notFound()

############################################## AStar ################################
def aStar (instance, hurestic):
    
    numCreated = 0
    numExpanded = 0
    maxFringe = 0
    
    visited = list()
    fringe = list()
    fringe.append(instance)

    while len(fringe) > 0:
        
        curr= getMinCostAStar(fringe)
        fringe.remove(curr)
        #print(curr.element)
        #time.sleep(3)
        if (np.array_equal(curr.element, goalA)
            or np.array_equal(curr.element, goalB)):
            print(curr.depth, numCreated, numExpanded, maxFringe)
            return
        
        numExpanded+=1
        for child in getChildren(curr):
            if contains(visited, child):
                continue            
            if not contains(fringe, child):
                numCreated+=1
                setCost(child, hurestic)
                child.cost += child.depth
                fringe.append(child)
                maxFringe = max (maxFringe, len(fringe))

        visited.append(curr)

    notFound()

############################################## GBFS ################################
def GBFS(instance, hurestic):
    numCreated = 0
    numExpanded = 0
    maxFringe = 0
    visited = list()
    fringe = list()
    fringe.append(instance)

    while len(fringe) > 0:
        curr= getMinCostGreedy(fringe)
        fringe.remove(curr)
        #print(curr.element)
        #time.sleep(3)
        if (np.array_equal(curr.element, goalA) or np.array_equal(curr.element, goalB)):
            print(curr.depth, numCreated, numExpanded, maxFringe)
            return
        
        numExpanded+=1
        for child in getChildren(curr):
            if contains(visited, child):
                continue            
            if not contains(fringe, child):
                numCreated+=1
                setCost(child, hurestic)
                fringe.append(child)
                maxFringe = max (maxFringe, len(fringe))

        visited.append(curr)

    notFound()

############################################## DLS ################################
def DLS (instance, maxDepth):

    
    numCreated = 0
    numExpanded = 0
    maxFringe = 0
    
    myQ = deque()
    myQ.append(instance)
    
    visited = list()

    while len(myQ) > 0:
        
        curr = myQ.pop()
        #print(curr.element)
        #time.sleep(3)
        if (np.array_equal(curr.element, goalA)
            or np.array_equal(curr.element, goalB)):
            print(curr.depth, numCreated, numExpanded, maxFringe)
            return

        numExpanded +=1
        if (curr.depth == maxDepth):
            visited.append(curr)
            continue
        
        for child in reversed(getChildren(curr)):
            if contains(visited, child):
                continue
            if not contains(visited, child):
                numCreated+=1
                myQ.append(child)
                maxFringe = max (maxFringe, len(myQ))

        visited.append(curr)
        
    notFound()

############################################## MAIN ################################


input = list(sys.argv[1])
input = np.asarray(input).reshape(4,4)
#print(input)
n = Node(input)
n.cost = 0
n.depth = 0

searchAlg = sys.argv[2]
if (searchAlg == 'BFS'):
    #print (searchAlg)
    BFS(n)
        
elif (searchAlg == 'DFS'):
    #print (searchAlg)
    DFS(n)
    
elif (searchAlg == 'AStar'):
    #print (searchAlg,  sys.argv[3])
    aStar(n, sys.argv[3])
    
elif (searchAlg == 'GBFS'):
    #print (searchAlg,  sys.argv[3])
    GBFS(n, sys.argv[3])    

elif (searchAlg == 'DLS'):
    #print (searchAlg,  sys.argv[3])
    DLS(n, int(sys.argv[3]))
