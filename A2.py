import copy 
import numpy as np
import gc
import sys
from itertools import groupby
import itertools as it
import time
# blocking, branching factor decrease as depth increase so we can increase branching factor
class GameBoard:
    def __init__(self):
        self.quadrant = [
            [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']],

            [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']],

            [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']],

            [['.', '.', '.'],
             ['.', '.', '.'],
             ['.', '.', '.']]
                        ]
        self.children = list()

        self.utility = 0


def printBoard(gameBoard, f):
    for i in range(0, 3):
        print >> f, (gameBoard.quadrant[0][i], gameBoard.quadrant[1][i])
        print (gameBoard.quadrant[0][i], gameBoard.quadrant[1][i])

    print >> f, ("")
    print ("")
    for i in range(0, 3):
        print >> f, (gameBoard.quadrant[2][i], gameBoard.quadrant[3][i])
        print(gameBoard.quadrant[2][i], gameBoard.quadrant[3][i])
    print >> f, ("________________________________________________________________________________")
    print("________________________________________________________________________________")
def printBoardToFile(gameBoard, out_file):
    a = (np.hstack((np.asarray(gameBoard.quadrant[0]), np.asarray(gameBoard.quadrant[1]))))
    b = (np.hstack((np.asarray(gameBoard.quadrant[2]), np.asarray(gameBoard.quadrant[3]))))
    board = np.vstack((a,b))
    np.savetxt('output.txt', board)
    '''
    for i in range(0, 3):
        out_file.write((gameBoard.quadrant[0][i], gameBoard.quadrant[1][i]))
        out_file.write("\n\n")
    
    for i in range(0, 3):
        out_file.write((gameBoard.quadrant[2][i], gameBoard.quadrant[3][i]))
        out_file.write("\n\n")
        out_file.write("________________________________________________________________________________")
    '''

def placeToken(gameBoard, block, position, token):
    block = block -1
    position = position-1
    if (gameBoard.quadrant[block][(position)/3][(position)%3]== '.'):
        gameBoard.quadrant[block][position/3][position%3] = token
    

def rotateBlock(gameBoard, block, clockWise):
    if clockWise:
        myGameBoard.quadrant[block-1] = zip (*myGameBoard.quadrant[block-1][::])
    else:
        myGameBoard.quadrant[block-1] = np.rot90(myGameBoard.quadrant[block-1])
        
def getChildren(gameBoard, char):
    
    board = copy.deepcopy(gameBoard.quadrant)
    children = list()
    for block in range (0,4):
        for i in range (1,5):
            for cell in range (1,10):
                if (board[i-1][(cell-1)/3][(cell-1)%3]== '.'):
                    childL = GameBoard()
                    childL.quadrant = copy.deepcopy(board)
                    placeToken(childL, i, cell, char)
                    childL.quadrant[block] = np.rot90(childL.quadrant[block])
                    childL.move = str(i)+"/"+str(cell)+" "+str(block+1)+"L"
                    childL.utility = countUtility(childL, char)
                    children.append(childL)

                    childR = GameBoard()
                    childR.quadrant = copy.deepcopy(board)
                    placeToken(childR, i, cell, char)
                    childR.quadrant[block] = np.rot90(childR.quadrant[block])
                    childR.quadrant[block] = np.rot90(childR.quadrant[block])
                    childR.quadrant[block] = np.rot90(childR.quadrant[block])
                    childR.move = str(i)+"/"+str(cell)+" "+str(block+1)+"R"
                    childR.utility = countUtility(childR, char)
                    children.append(childR)
                    children.sort(key=lambda x: x.utility, reverse=True)
    #print(len(children))                  
    return children
    
def populateChildren(gameBoard, char):
    
    board = copy.deepcopy(gameBoard.quadrant)
    for block in range (0,4):
        for i in range (1,5):
            for cell in range (1,10):
                if (board[i-1][(cell-1)/3][(cell-1)%3]== '.'):
                    childL = GameBoard()
                    childL.quadrant = copy.deepcopy(board)
                    placeToken(childL, i, cell, char)
                    childL.quadrant[block] = np.rot90(childL.quadrant[block])
                    childL.move = str(i)+"/"+str(cell)+" "+str(block+1)+"L"
                    gameBoard.children.append(childL)

                    childR = GameBoard()
                    childR.quadrant = copy.deepcopy(board)
                    placeToken(childR, i, cell, char)
                    childR.quadrant[block] = np.rot90(childR.quadrant[block])
                    childR.quadrant[block] = np.rot90(childR.quadrant[block])
                    childR.quadrant[block] = np.rot90(childR.quadrant[block])
                    childR.move = str(i)+"/"+str(cell)+" "+str(block+1)+"R"
                    gameBoard.children.append(childR)
    #print(len(gameBoard.children))
def isLeaf(myGameBoard):
    for i in range (1,5):
        for cell in range (1,10):
            if (myGameBoard.quadrant[i-1][(cell-1)/3][(cell-1)%3]== '.'):
                return False

    return True
    
    
def countUtility(myGameBoard, char):
    a = (np.hstack((np.asarray(myGameBoard.quadrant[0]), np.asarray(myGameBoard.quadrant[1]))))
    b = (np.hstack((np.asarray(myGameBoard.quadrant[2]), np.asarray(myGameBoard.quadrant[3]))))
    board = np.vstack((a,b))
    longest_seq = 0
    for row in board:
        idx_pairs = np.where(np.diff(np.hstack(([False],row==char,[False]))))[0].reshape(-1,2)
        if len(idx_pairs) > 0:
            longest_seq = max(longest_seq
                              , idx_pairs[np.diff(idx_pairs,axis=1).argmax(),1] - idx_pairs[np.diff(idx_pairs,axis=1).argmax(),0])
        
    for col in board.T:
        idx_pairs = np.where(np.diff(np.hstack(([False],col==char,[False]))))[0].reshape(-1,2)
        if len(idx_pairs) > 0:
            longest_seq = max(longest_seq
                              , idx_pairs[np.diff(idx_pairs,axis=1).argmax(),1] - idx_pairs[np.diff(idx_pairs,axis=1).argmax(),0])

    for i in range(-1,2):
        idx_pairs = np.where(np.diff(np.hstack(([False]
                            ,np.diag(board, k = i)==char,[False]))))[0].reshape(-1,2)
        if len(idx_pairs) > 0:
            longest_seq = max(longest_seq
                          , idx_pairs[np.diff(idx_pairs,axis=1).argmax(),1] - idx_pairs[np.diff(idx_pairs,axis=1).argmax(),0])

    for i in range(-1,2):
        idx_pairs = np.where(np.diff(np.hstack(([False]
                            ,np.diag(np.rot90(board), k = i)==char,[False]))))[0].reshape(-1,2)
        if len(idx_pairs) > 0:
            longest_seq = max(longest_seq
                          , idx_pairs[np.diff(idx_pairs,axis=1).argmax(),1] - idx_pairs[np.diff(idx_pairs,axis=1).argmax(),0])
    if longest_seq >= 5:
        return 1000

    return longest_seq*longest_seq

def getMaxMove(gameBoard):
    retVal = 0
    curUtility = -sys.maxsize -1
    for child in gameBoard.children:
        if child.utility > curUtility:
            curUtility = child.utility
            retVal = child
    return retVal

def getMinMove(gameBoard):
    retVal = 0
    curUtility = sys.maxsize
    print(len(gameBoard.children))
    for child in gameBoard.children:
        #print ("child util: ", child.utility )
        if  child.utility < curUtility:
            curUtility = child.utility
            print ("curr util: ", curUtility )
            retVal = child
            print(printBoard(retVal))
    return retVal

def AI_Move(gameBoard, depth, AiToken, isMax):
    alpha = -sys.maxsize -1
    beta = sys.maxsize
    populateChildren(gameBoard, AiToken)
    minMaxAlphaBetaPruning(gameBoard, alpha, beta, depth, isMax)
    return getMaxMove(gameBoard)

def minMax(gameBoard, depth, isMax):

    if depth == 0 or len(gameBoard.children) == 0:
        if isMax:
            return countUtility(gameBoard, 'W') - countUtility(gameBoard, 'B')
        else:
            return - countUtility(gameBoard, 'B') + countUtility(gameBoard, 'W')

    if isMax:
        populateChildren (gameBoard, 'W')
    else:
        populateChildren (gameBoard, 'B')



    if isMax:
        myMax = -sys.maxsize -1
        for child in gameBoard.children:
            child.utility = minMax(child, depth-1, False)
            myMax = max(child.utility, myMax)
        return myMax
    
    else:
        myMin = sys.maxsize
        for child in gameBoard.children:
            child.utility = minMax(child, depth-1, True)
            myMin = min(child.utility, myMin)
        return myMin
        
  
    
def minMaxAlphaBetaPruning(gameBoard, alpha, beta, depth, isMax):
    
    if depth == 0 or isLeaf(gameBoard):
        if isMax:
            return countUtility(gameBoard, 'W') - countUtility(gameBoard, 'B')
        else:
            return - countUtility(gameBoard, 'B') + countUtility(gameBoard, 'W')
    children = 0
    if isMax:
        util = -sys.maxsize -1
        children = getChildren(gameBoard, 'W')
        for child in children:
            #WIN
            if countUtility(child, 'W') == 1000:
                child.utility = 1000 / (3- (depth%3-1))
                child.utility = child.utility *depth
                gameBoard.children = children
                return child.utility
            #BLOCK
            if countUtility(child, 'B') >= 16:
                child.utility = -800 / (3- (depth%3-1))
                child.utility = child.utility *depth
                gameBoard.children = children

                return child.utility

            child.utility  = minMaxAlphaBetaPruning(child,alpha, beta, depth-1, False)
            util = max(util , child.utility)
            alpha = max(util , alpha)
            if beta <= alpha:
                break
        gameBoard.children = children
        return util
    
    else:
        util = sys.maxsize
        children = getChildren(gameBoard, 'B')
        for child in children:
            #WIN
            if countUtility(child, 'B') == 1000:
                child.utility = - 1000 / (3- (depth%3-1))
                child.utility = child.utility * (depth)
                gameBoard.children = children
                return child.utility
            #Block
            if countUtility(child, 'W') >= 16:
                child.utility =  800 / (3- (depth%3-1))
                child.utility = child.utility * depth
                #print (printBoard(child))
                #print("BLOCK", child.utility)
                return child.utility
                
            child.utility = minMaxAlphaBetaPruning(child,alpha, beta, depth-1, True)
            util  = min(util , child.utility)
            beta = min(util , beta)
            if beta <= alpha:
                break
        
        gameBoard.children = children        
        return util



'''
placeToken(myGameBoard, 1, 1, 'W')
placeToken(myGameBoard, 2, 1, 'W')
placeToken(myGameBoard, 3, 1, 'W')
placeToken(myGameBoard, 4, 1, 'W')

print(printBoard(myGameBoard))
#populateChildren(myGameBoard, 'B')


placeToken(myGameBoard, 1, 1, 'W')
print(printBoard(myGameBoard))
print(printBoard(AI_Move(myGameBoard, False)))


placeToken(myGameBoard, 1, 1, 'W')
placeToken(myGameBoard, 1, 4, 'W')
placeToken(myGameBoard, 1, 7, 'W')
placeToken(myGameBoard, 3, 1, 'W')
placeToken(myGameBoard, 4, 4, 'W')
print(printBoard(myGameBoard))
print countUtility(myGameBoard, 'W')

placeToken(myGameBoard, 1, 7, 'W')
placeToken(myGameBoard, 1, 8, 'W')
placeToken(myGameBoard, 1, 9, 'W')

placeToken(myGameBoard, 4, 1, 'W')
placeToken(myGameBoard, 4, 2, 'B')
placeToken(myGameBoard, 4, 3, 'W')
placeToken(myGameBoard, 4, 4, 'B')
placeToken(myGameBoard, 4, 5, 'B')
placeToken(myGameBoard, 4, 6, 'B')
placeToken(myGameBoard, 4, 7, 'W')
placeToken(myGameBoard, 4, 8, 'W')
placeToken(myGameBoard, 4, 9, 'B')
'''
def gameOver(myGameBoard):

    w = countUtility(myGameBoard, 'W')
    b = countUtility(myGameBoard, 'B')
    if (w >= 1000 and b >= 1000):
        print ("It's a tie!")
        print >> f,  ("It's a tie!")
        return True
    elif(w >=  1000):
        print("W wins!")
        print >> f, ("W wins!")
        return True
    elif(b >= 1000):
        print ("B wins!")
        print >> f,("B wins!")
        return True
    
    return False


def humanFirst(humanToken, AiToken):
    f = open("output2.txt","w")
    depth = 2
    numOfPlays = 0
    myGameBoard = GameBoard()
    for i in range (0,4):
        myGameBoard.quadrant[i] = np.rot90(myGameBoard.quadrant[i])
    while not gameOver(myGameBoard, f):
        depth = depth+(numOfPlays/3)
        print >>f, "It's your turn:\n"
        print "It's your turn:"
        b = raw_input("Which block would you like to place a token in? (1 to 4)")
        print >>f , "Which block would you like to place a token in? (1 to 4)"+b+"\n"
        p = raw_input("Which square? (1 to 9)")
        print >>f , ("Which square? (1 to 9)"+p+"\n")
        placeToken(myGameBoard, int(b), int(p), humanToken)
        if gameOver(myGameBoard, f):
            break
        block = int(raw_input("Which block would you like to rotate? (1 to 4)"))
        print >>f , ("Which block would you like to rotate? (1 to 4)"+str(block)+"\n")
        d = raw_input("Which direction? (R or L)")
        print >>f , ("Which direction? (R or L)"+d+"\n")

                       
        if str(d) == 'R' or str(d) == 'r':
            for i in range(0,3):
                myGameBoard.quadrant[block-1] = np.rot90(myGameBoard.quadrant[block-1])
        else:
                myGameBoard.quadrant[block-1] = np.rot90(myGameBoard.quadrant[block-1])
        printBoard(myGameBoard, f)
        print >>f , ("Your move = "+repr(b)+repr("/")+repr(p)+repr(" ")+repr(block)+repr(d))
        print  ("Your move = "+repr(b)+repr("/")+repr(p)+repr(" ")+repr(block)+repr(d))
        print >>f, ("---------------------------")
        print ("---------------------------")
        if gameOver(myGameBoard, f):
            break

        
        print >>f, ("It's the AI turn: (depth = ", depth,")\n")
        print ("It's the AI turn:", depth)
        myGameBoard = AI_Move(myGameBoard, depth, AiToken, False)
        (printBoard(myGameBoard, f))
        print >>f, ("AI move = ",myGameBoard.move)
        print ("AI move = ",myGameBoard.move)
        print >>f,  ("---------------------------")
        print ("---------------------------")
        numOfPlays+=1



def AiFirst():
    depth = 2
    numOfPlays = 0
    myGameBoard = GameBoard()
    for i in range (0,4):
        myGameBoard.quadrant[i] = np.rot90(myGameBoard.quadrant[i])
    while not gameOver(myGameBoard):
        depth = depth+(numOfPlays/3)
        print("It's the AI turn:")
        myGameBoard = AI_Move(myGameBoard, depth, AiToken, True)
        print(printBoard(myGameBoard))
        print("AI move = ",myGameBoard.move)
        print ("---------------------------")
        if gameOver(myGameBoard):
            break
        print("It's your turn:")       
        b = raw_input("Which block would you like to place a token in? (1 to 4)")
        p = raw_input("Which square? (1 to 9)")
        placeToken(myGameBoard, int(b), int(p), humanToken)
        if gameOver(myGameBoard):
            break
        block = int(raw_input("Which block would you like to rotate? (1 to 4)"))
        d = raw_input("Which direction? (R or L)")

        if gameOver(myGameBoard):
            break
        print d
        if str(d) == 'R' or str(d) == 'r':
            for i in range(0,3):
                myGameBoard.quadrant[block-1] = np.rot90(myGameBoard.quadrant[block-1])
        else:
                myGameBoard.quadrant[block-1] = np.rot90(myGameBoard.quadrant[block-1])
        print(printBoard(myGameBoard))
        move = str(i)+"/"+str(cell)+" "+str(block+1)+"R"
        print("Your move = "+repr(b)+repr("/")+repr(p)+repr(" ")+repr(block)+repr(d))
        print ("---------------------------")
        numOfPlays+=1

    


first = raw_input("Would you like to go first? (Y/N)")        
if (first == 'Y' or first == 'y'):
    humanFirst('W', 'B')
else:
    AiFirst('B', 'W')
    
  
