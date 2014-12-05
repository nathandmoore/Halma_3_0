#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

# AUTHOR: NATHAN MOORE
# URL: http://lyle.smu.edu/~ndmoore/cgi-bin/AI.py
# Does not take enemy pieces into account

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
        . bool arrived: true if the piece has arrived at destination
        * Upper left corner of board is 0,0
    """

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.arrived = False


    @property
    def x(self):
        return self.__x


    @property
    def y(self):
        return self.__y


    @property
    def arrived(self):
        return self.__arrived


    @x.setter
    def x(self,x):
        self.__x = x


    @y.setter
    def y(self,y):
        self.__y = y


    @arrived.setter
    def arrived(self,arrived):
        self.__arrived = arrived




def getMove(pieces,destRegion,pieceToMove):
    """ Function: getMove
        => Description:
            Calculates the next move the AI should make
        => Parameters:
            . pieces: list of cells representing the pieces on
                the board
            . destRegion: list of cells representing the
                destination area
            . pieceToMove: the piece to move next
        => Returns:
            . nextMove: list with the location of the piece to
                move and the location to move that piece to
    """

    nextMove = {}
    # Select piece to move and destination to move to:
    # Make sure that the piece isn't already in the destination
    #     region
    nextMove["destx"] = pieces[pieceToMove].x
    nextMove["desty"] = pieces[pieceToMove].y
    nextMove["piecex"] = pieces[pieceToMove].x
    nextMove["piecey"] = pieces[pieceToMove].y

    if pieceToMove > 8:
        destCell = destRegion[pieceToMove-3]
    else:
        destCell = destRegion[pieceToMove]

    if not (pieces[pieceToMove].arrived and destCell.arrived):
        # if the piece to move has not arrived at its destination
        #simulate the next move to take
        directMove = makeMove(pieces[pieceToMove],destCell)
        # Modify the move if a jump is available
        #  Check if a piece is already in the location you want to
        #     move to
        #  if yes: check next location along path
        #      if yet another piece: skip move
        #      if not: move to that second location (jump)
        #  if no: move to location
        nextMove = determineJump(pieces,pieceToMove,directMove,destCell)
    # else skip move

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

    if pieceToMove.x > destCell.x:
        #move left
        directMove.x = pieceToMove.x-1
    elif pieceToMove.x < destCell.x:
        #move right
        directMove.x = pieceToMove.x+1
    else:
        #don't move
        directMove.x = pieceToMove.x

    #calculate vertical movement
    if pieceToMove.y > destCell.y:
        #move down
        directMove.y = pieceToMove.y-1
    elif pieceToMove.y < destCell.y:
        #move up
        directMove.y = pieceToMove.y+1
    else:
        #don't move
        directMove.y = pieceToMove.y

    return directMove


def determineJump(pieces,pieceToMove,move,destCell):
    """ Function: determineJump
         => Description:
             Determines if there is a piece to jump along the direct
             path to the destination and adjusts the next move to
             account for such a jump
             If there is a piece at the location you want to jump
                 to, then skip the move altogether
         => Parameters:
             . pieces: array of cells representing pieces
             . Int pieceToMove: index of the piece to move
             . move: cell representing the move to make
             . Cell destCell: cell representing the destination
         => Returns:
             . Cell newMove: the cell to move to
    """

    numPieces = len(pieces)
    newMove = {}
    newMove["destx"] = move.x
    newMove["desty"] = move.y
    newMove["piecex"] = pieces[pieceToMove].x
    newMove["piecey"] = pieces[pieceToMove].y
    newMove["jump"] = True

    for piece in range(0,numPieces):
        #check location of pieces to find if there is one to jump
        if (pieces[piece].x == move.x and pieces[piece].y == move.y):
            #if there's a piece to jump
            #look at next cell to see if jump is possible
            jumpMove = makeMove(move,destCell)

            for i in range(0,numPieces):

                if (pieces[i].x == jumpMove.x and pieces[i].y == jumpMove.y):
                    # pieces are in the way of jumping and moving so don't move
                    newMove["destx"] = pieces[pieceToMove].x
                    newMove["desty"] = pieces[pieceToMove].y
                    newMove["jump"] = False
                    break

            if (newMove["jump"]):
                newMove["destx"] = jumpMove.x
                newMove["desty"] = jumpMove.y

            break

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

            if (pieces[piece].x == dests[dest].x and
                pieces[piece].y == dests[dest].y):

                pieces[piece].arrived = True
                dests[dest].arrived = True
                break


#------------------------------------------------------------------------------
# get data
# stringJSON = """{
#                     "board": {
#                         "currPiece": 1,
#                         "pieces": [
#                             {"y":0,"x":15},
#                             {"y":15,"x":0},
#                             {"y":16,"x":0},
#                             {"y":17,"x":0},
#                             {"y":14,"x":1},
#                             {"y":15,"x":1},
#                             {"y":16,"x":1},
#                             {"y":17,"x":1},
#                             {"y":14,"x":2},
#                             {"y":15,"x":2},
#                             {"y":16,"x":2},
#                             {"y":17,"x":2}
#                         ],
#                         "destinations": [
#                             {"y":0,"x":17},
#                             {"y":1,"x":17},
#                             {"y":2,"x":17},
#                             {"y":0,"x":16},
#                             {"y":1,"x":16},
#                             {"y":2,"x":16},
#                             {"y":0,"x":15},
#                             {"y":1,"x":15},
#                             {"y":2,"x":15}
#                         ],
#                         "enemy":  [
#                             {"y":11,"x":12},
#                             {"y":11,"x":11},
#                             {"y":14,"x":13},
#                             {"y":17,"x":15},
#                             {"y":12,"x":12},
#                             {"y":10,"x":9},
#                             {"y":15,"x":15},
#                             {"y":17,"x":16},
#                             {"y":9,"x":10},
#                             {"y":14,"x":16},
#                             {"y":14,"x":15},
#                             {"y":14,"x":14}
#                         ],
#                         "moveCount":49
#                     }
#                 }
#             """
# stringJSON = """
#                 {"board":
#                     {
#                         "currPiece": 3,
#                         "pieces":[
#                             {"y":12,"x":2,"team":0},
#                             {"y":12,"x":3,"team":0},
#                             {"y":16,"x":0,"team":0},
#                             {"y":17,"x":0,"team":0},
#                             {"y":14,"x":1,"team":0},
#                             {"y":15,"x":1,"team":0},
#                             {"y":16,"x":1,"team":0},
#                             {"y":17,"x":1,"team":0},
#                             {"y":14,"x":2,"team":0},
#                             {"y":15,"x":2,"team":0},
#                             {"y":16,"x":2,"team":0},
#                             {"y":17,"x":2,"team":0}],"destinations":[{"y":0,"x":17,"team":-1},{"y":1,"x":17,"team":-1},{"y":2,"x":17,"team":-1},{"y":0,"x":16,"team":-1},{"y":1,"x":16,"team":-1},{"y":2,"x":16,"team":-1},{"y":0,"x":15,"team":-1},{"y":1,"x":15,"team":-1},{"y":2,"x":15,"team":-1}],"boardSize":18,"enemy":[{"y":13,"x":14,"team":1},{"y":14,"x":14,"team":1},{"y":15,"x":14,"team":1},{"y":16,"x":14,"team":1},{"y":13,"x":15,"team":1},{"y":14,"x":15,"team":1},{"y":15,"x":15,"team":1},{"y":16,"x":15,"team":1},{"y":13,"x":16,"team":1},{"y":15,"x":17,"team":1},{"y":16,"x":17,"team":1},{"y":17,"x":17,"team":1}],"currPiece":2,"moveCount":3}}"""

# stringJSON = json.loads(stringJSON)
# gameData = stringJSON["board"]

postData = cgi.FieldStorage()
gameData = ast.literal_eval(postData.getvalue('board'))

#set pieces as cells
pieces = gameData["pieces"]
pieces = setPieces(pieces)

#set destinations as cells
destRegion = gameData["destinations"]
destRegion = setDestinations(destRegion)

#get the number of the piece to move
pieceToMove = gameData["currPiece"]

#check if pieces are in destinations
checkIfArrived(pieces,destRegion)

#make next move
nextMove = getMove(pieces,destRegion,pieceToMove)

#return JSON of next move
nextMove = {
    'from': {'x': nextMove['piecex'], 'y': nextMove['piecey']},
    'to': [{'x': nextMove['destx'], 'y': nextMove['desty']}]
    }

# return the next move
print 'Content-Type: application/json\n'
print
print str(json.dumps(nextMove))
