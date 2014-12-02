#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# AUTHOR: NATHAN MOORE
# URL: http://lyle.smu.edu/~ndmoore/cgi-bin/AI.py

import cgi
import cgitb
import json
import ast

cgitb.enable()

class Cell:
    """ Class: Cell
    => Description:
        Intended to represent pieces and destinations
    => Class variables:
        . int x: coordinate on game board
        . int y: coordinate on game board
        * Upper left corner of board is 0,0
    => Class methods:
        . Getters for x and y
        . Setters for all variables
        . Function: isArrived
            # getter for arrived variable
    """


    __x = 0
    __y = 0
    __arrived = False

    def __init__(self,x,y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def isArrived(self):
        return self.__arrived

    def setX(self,x):
        self.__x = x

    def setY(self,y):
        self.__y = y

    def setArrived(self,arrived):
        self.__arrived = arrived


def getMove(pieces,destRegion,enemy):
    """ Function: getMove
        => Description:
            Calculates the next move the AI should make
        => Parameters:
            . pieces: list of cells representing the pieces on
                the board
            . destRegion: list of cells representing the
                destination area
            . enemy: list of enemy pieces
        => Returns:
            . nextMove: list with the location of the piece to
                move and the location to move that piece to
    """


    nextMove = []
    # Select piece to move and destination to move to:
    # Make sure that the piece isn't already in the destination
    #     region and that the destination cell selected is not
    #     already occupied
    pieceToMove = Cell(0,0)
    destCell = Cell(0,0)
    numPieces = len(pieces)
    piece = 0
    numDestinations = len(destRegion)
    destination = 0

    while piece < numPieces:
        #if piece is not in destination region
        if not pieces[piece].isArrived():
            #select it
            pieceToMove.setX(pieces[piece].getX())
            pieceToMove.setY(pieces[piece].getY())
            #if the usual way of picking a desition cell
            #is a cell that is already occupied
            if destRegion[piece].isArrived():
                #choose another destination cell
                while destination < numDestinations:
                    #destination cell is unoccupied
                    if not destRegion[destination]. isArrived():
                        #select it
                        destCell.setX(destRegion[destination].getX())
                        destCell.setY(destRegion[destination].getY())
                        break

                    destination+=1
            else:
                #destination cell is unoccupied
                destCell.setX(destRegion[piece].getX())
                destCell.setY(destRegion[piece].getY())

            nextMove.append(pieceToMove)
            break

        piece+=1

    #simulate the next move to take
    directMove = makeMove(pieceToMove,destCell)
    # Modify the move if a jump is available
    #  Check if a piece is already in the location you want to
    #     move to
    #  if yes: check next location along path
    #      if yet another piece: move that other piece along path
    #         instead of the original piece selected
    #      if not: move to that second location (jump)
    #  if no: move to location
    nextMove = determineJump(pieces,piece,directMove,1,destCell,enemy)

    return nextMove


def makeMove(pieceToMove,destCell):
    """ Function: move
        => Description:
             Simulates the move for the selected piece to the
             desired destination directly (preferred: diagonal move)
        => Parameters:
             . Cell pieceToMove: cell representing the piece to
                 move
             . Cell destCell: cell representing the destination
        => Returns:
             . Cell directMove: cell representing the cell to move
                 to
    """


    #calculate direct move toward destination
    directMove = Cell(0,0)

    if pieceToMove.getX() > destCell.getX():
        #move left
        directMove.setX(pieceToMove.getX()-1)
    elif pieceToMove.getX() < destCell.getX():
        #move right
        directMove.setX(pieceToMove.getX()+1)
    else:
        #don't move
        directMove.setX(pieceToMove.getX())

    #calculate vertical movement
    if pieceToMove.getY() > destCell.getY():
        #move down
        directMove.setY(pieceToMove.getY()-1)
    elif pieceToMove.getY() < destCell.getY():
        #move up
        directMove.setY(pieceToMove.getY()+1)
    else:
        #don't move
        directMove.setY(pieceToMove.getY())

    return directMove


def antiMove(pieceToMove,destCell):
    """ Function: move
         => Description:
             Moves the piece backward in case too many pieces in the
             way
         => Parameters:
             . Cell pieceToMove: cell representing the piece to
                 move
             . Cell destCell: cell representing the destination
         => Returns:
             . Cell directMove: cell representing the cell to move
                 to
    """


    #calculate direct move toward destination
    directMove = Cell(0,0)

    if pieceToMove.getX() > destCell.getX():
        #move left
        directMove.setX(pieceToMove.getX()+1)
    elif pieceToMove.getX() < destCell.getX():
        #move right
        directMove.setX(pieceToMove.getX()-1)
    else:
        #don't move
        directMove.setX(pieceToMove.getX())

    #calculate vertical movement
    if pieceToMove.getY() > destCell.getY():
        #move down
        directMove.setY(pieceToMove.getY()+1)
    elif pieceToMove.getY() < destCell.getY():
        #move up
        directMove.setY(pieceToMove.getY()-1)
    else:
        #don't move
        directMove.setY(pieceToMove.getY())

    return directMove


def determineJump(pieces,pieceToMove,move,counter,destCell,enemy):
    """ Function: determineJump
         => Description:
             Determines if there is a piece to jump along the direct
             path to the destination and adjusts the next move to
             account for such a jump
             If there is a piece at the location you want to jump
                 to, move that piece first (also sees if that piece
                 can jump, and so on, until a piece is found that
                 can be moved)
         => Parameters:
             . pieces: array of cells representing pieces
             . Int pieceToMove: index of the piece to move
             . move: cell representing the move to make
             . Int counter: int showing how many pieces may be in
                 the way of a direct move of the piece
             . Cell destCell: cell representing the destination
             . enemy: array of enemy pieces
         => Returns:
             . Cell newMove: the cell to move to
    """


    numPieces = len(pieces)
    newMove = {}
    newMove["destx"] = move.getX()
    newMove["desty"] = move.getY()
    newMove["piecex"] = pieces[pieceToMove].getX()
    newMove["piecey"] = pieces[pieceToMove].getY()
    newMove["jump"] = None

    for piece in range(0,numPieces):
        #check location of pieces to find if there is one to jump
        if ((pieces[piece].getX() == move.getX() and
             pieces[piece].getY() == move.getY())
             or
             (enemy[piece].getX() == move.getX() and
              enemy[piece].getY() == move.getY() and counter < 2)):
            #if there's a piece to jump
            #look at next cell until a piece is found that can be
            #moved
            jumpMove = makeMove(move,destCell)
            newMove = determineJump(pieces,piece,jumpMove,
                counter+1,destCell,enemy)
            break
        elif (enemy[piece].getX() == move.getX() and
              enemy[piece].getY() == move.getY() and counter > 1):
            #elif there is an enemy in the way further down too
            newMove["jump"] = False
            break
        else:
            #valid jump available
            if counter == 2:
                if (newMove["piecex"] != newMove["destx"] and
                    newMove["piecey"] != newMove["desty"]):
                    newMove["jump"] = True

    if newMove["jump"] is not None:
        #make sure we have the right piece jump
        newMove["piecex"] = pieces[pieceToMove].getX()
        newMove["piecey"] = pieces[pieceToMove].getY()

        if not newMove["jump"]:
            newDest = antiMove(pieces[pieceToMove],destCell)
            newMove["destx"] = newDest.getX()
            newMove["desty"] = newDest.getY()

    return newMove

def setPieces(pieces):
    """ Function: setPieces
         => Description:
             Creates cell objects for each piece x,y coordinate
         => Parameters:
             . pieces: array of piece coordinates
         => Returns:
             . piecesAsCells: array of cells with piece coords
    """


    piecesAsCells = []
    numPieces = len(pieces)

    for piece in range(0,numPieces):

        newPiece = Cell(pieces[piece]["x"],pieces[piece]["y"])
        piecesAsCells.append(newPiece)

    return piecesAsCells


def setDestinations(dests):
    """ Function: setDestinations
         => Description:
             Creates cell objects for each destination x,y coord
         => Parameters:
             . dests: array of destination coords
         => Returns:
             . destsAsCells: array of cells with destination coords
    """


    destsAsCells = []
    numDests = len(dests)

    for dest in range(0,numDests):

        newDest = Cell(dests[dest]["x"],dests[dest]["y"])
        destsAsCells.append(newDest)

    return destsAsCells


def checkIfArrived(pieces,dests):
    """
     Function: checkIfArrived
         => Description:
             Checks if pieces are at final destinations and sets
             arrived to true for each piece at its destination
             and for each destination cell that is occupied
         => Parameters:
             . pieces: array of piece coords
             . dests: array of destination coords
         => Returns:
             . pieces: array of cells with piece coords w/updates
                 for any cell at its final destination
    """


    numDests = len(dests)
    numPieces = len(pieces)

    #check if any pieces at the back of the destination region
    for dest in range(0,numDests):

        for piece in range(0,numPieces):

            if (pieces[piece].getX() == dests[dest].getX() and
                pieces[piece].getY() == dests[dest].getY()):

                pieces[piece].setArrived(True)
                dests[dest].setArrived(True)
                break


#------------------------------------------------------------------------------
# get data
# stringJSON = """{"board":
#                         {"pieces":
#                                     [{"y":0,"x":15,"team":0},
#                                     {"y":15,"x":0,"team":0},
#                                     {"y":16,"x":0,"team":0},
#                                     {"y":17,"x":0,"team":0},
#                                     {"y":14,"x":1,"team":0},
#                                     {"y":15,"x":1,"team":0},
#                                     {"y":16,"x":1,"team":0},
#                                     {"y":17,"x":1,"team":0},
#                                     {"y":14,"x":2,"team":0},
#                                     {"y":15,"x":2,"team":0},
#                                     {"y":16,"x":2,"team":0},
#                                     {"y":17,"x":2,"team":0}],
#                         "destinations":
#                                     [{"y":0,"x":17,"team":-1},
#                                     {"y":1,"x":17,"team":-1},
#                                     {"y":2,"x":17,"team":-1},
#                                     {"y":0,"x":16,"team":-1},
#                                     {"y":1,"x":16,"team":-1},
#                                     {"y":2,"x":16,"team":-1},
#                                     {"y":0,"x":15,"team":-1},
#                                     {"y":1,"x":15,"team":-1},
#                                     {"y":2,"x":15,"team":-1}],
#                         "boardSize":18,
#                         "enemy":
#                                     [{"y":11,"x":12,"team":1},
#                                     {"y":11,"x":11,"team":1},
#                                     {"y":14,"x":13,"team":1},
#                                     {"y":17,"x":15,"team":1},
#                                     {"y":12,"x":12,"team":1},
#                                     {"y":10,"x":9,"team":1},
#                                     {"y":15,"x":15,"team":1},
#                                     {"y":17,"x":16,"team":1},
#                                     {"y":9,"x":10,"team":1},
#                                     {"y":14,"x":16,"team":1},
#                                     {"y":14,"x":15,"team":1},
#                                     {"y":14,"x":14,"team":1}],
#                         "enemydestinations":
#                                     [{"y":0,"x":0,"team":-1},
#                                     {"y":1,"x":0,"team":-1},
#                                     {"y":2,"x":0,"team":-1},
#                                     {"y":0,"x":1,"team":-1},
#                                     {"y":1,"x":1,"team":-1},
#                                     {"y":2,"x":1,"team":-1},
#                                     {"y":0,"x":2,"team":-1},
#                                     {"y":1,"x":2,"team":-1},
#                                     {"y":2,"x":2,"team":-1}],
#                         "moveCount":49}
#                 }
#             """
# stringJSON = json.loads(stringJSON)
# gameData = stringJSON["board"]
postData = cgi.FieldStorage()
gameData = ast.literal_eval(postData.getvalue('board'))

#set pieces as cells
pieces = gameData["pieces"]
pieces = setPieces(pieces)

#set enemy pieces as cells
enemy = gameData["enemy"]
enemy = setPieces(enemy)

#set destinations as cells
destRegion = gameData["destinations"]
destRegion = setDestinations(destRegion)

#check if pieces are in destinations
checkIfArrived(pieces,destRegion)

#make next move
nextMove = getMove(pieces,destRegion,enemy)

#return JSON of next move
nextMove = {
    'from': {'x': nextMove['piecex'], 'y': nextMove['piecey']},
    'to': [{'x': nextMove['destx'], 'y': nextMove['desty']}]
    }

print 'Content-Type: application/json\n'
print
print str(json.dumps(nextMove))

