<?php

    /*\
    |*| AUTHOR: NATHAN MOORE
    |*| URL: http://lyle.smu.edu/~ndmoore/4353/Hwk11/Hwk11Moore.php
    |*| LIST OF FUNCTIONS/CLASSES IN THE ORDER THEY APPEAR:
    |*|     1) Class Cell
    |*|     2) Function getMove()
    |*|     3) Function move()
    |*|     4) Function determineJump()
    |*|     5) Function initGame()
    |*|     6) Function setPieces()
    |*|     7) Function setDestinations()
    |*|     8) Function checkIfArrived()
    \*/

    /*\
    |*| Class: Cell
    |*|     => Description:
    |*|         Intended to represent pieces and destinations
    |*|     => Class variables:
    |*|         -> int x: coordinate on game board
    |*|         -> int y: coordinate on game board
    |*|         * Upper left corner of board is 0,0
    |*|     => Class methods:
    |*|         -> Getters for x and y
    |*|         -> Setters for all variables
    |*|         -> Function: isArrived
    |*|             # getter for arrived variable
    \*/
    class Cell {

        var $x;
        var $y;
        private $arrived = false;

        public function __construct($x, $y) {
            $this->x = $x;
            $this->y = $y;
        }

        public function getX() {
            return $this->x;
        }

        public function getY() {
            return $this->y;
        }

        public function isArrived() {
            return $this->arrived;
        }

        public function setX($x) {
            $this->x = $x;
        }

        public function setY($y) {
            $this->y = $y;
        }

        public function setArrived() {
            $this->arrived = true;
        }

    }

    /*\
    |*| Function: getMove
    |*|     => Description: 
    |*|         Calculates the next move the AI should make
    |*|     => Parameters:
    |*|         -> pieces: array of cells representing the pieces on
    |*|             the board
    |*|         -> destRegion: array of cells representing the
    |*|             destination area
    |*|         -> enemy: array of enemy pieces
    |*|     => Returns:
    |*|         -> nextMove: array with the location of the piece to 
    |*|             move and the location to move that piece to             
    \*/
    function getMove($pieces,$destRegion,$enemy) {

        $nextMove = array();

        /**
          * Select piece to move and destination to move to:
          * Make sure that the piece isn't already in the destination
          *     region and that the destination cell selected is not
          *     already occupied
          */
        $pieceToMove = new Cell(0,0);
        $destCell = new Cell(0,0);
        $numPieces = sizeof($pieces);
        $piece=0;
        $numDestinations = sizeof($destRegion);
        $destination = 0;

        while ($piece < $numPieces) { 
                
            //if piece is not in destination region
            if (!$pieces[$piece]->isArrived()) {

                //select it
                $pieceToMove->setX($pieces[$piece]->getX());
                $pieceToMove->setY($pieces[$piece]->getY());

                //if the usual way of picking a desition cell
                //is a cell that is already occupied
                if ($destRegion[$piece]->isArrived()) {

                    //choose another destination cell
                    while ($destination < $numDestinations) {

                        //destination cell is unoccupied
                        if (!$destRegion[$destination]-> isArrived()) {

                            //select it
                            $destCell->
                                setX($destRegion[$destination]-> 
                                    getX());
                            $destCell->
                                setY($destRegion[$destination]->
                                    getY());
                            break;

                        }

                        $destination++;

                    }

                } else { //destination cell is unoccupied

                $destCell->setX($destRegion[$piece]->getX());
                $destCell->setY($destRegion[$piece]->getY());

                }

                array_push($nextMove,$pieceToMove);
                break;

            }

            $piece++;

        }

        //simulate the next move to take
        $directMove = move($pieceToMove,$destCell);

        /**
          * Modify the move if a jump is available
          *  Check if a piece is already in the location you want to
          *     move to
          *  if yes: check next location along path
          *      if yet another piece: move that other piece along path
          *         instead of the original piece selected
          *      if not: move to that second location (jump)
          *  if no: move to location
          */
        $nextMove = 
            determineJump($pieces,$piece,$directMove,1,$destCell,
                $enemy);

        return $nextMove;

    }

    /*\
    |*| Function: move
    |*|     => Description:
    |*|         Simulates the move for the selected piece to the 
    |*|         desired destination directly (preferred: diagonal move)
    |*|     => Parameters:
    |*|         -> Cell pieceToMove: cell representing the piece to
    |*|             move
    |*|         -> Cell destCell: cell representing the destination
    |*|     => Returns:
    |*|         -> Cell directMove: cell representing the cell to move
    |*|             to
    \*/
    function move($pieceToMove,$destCell) {

        //calculate direct move toward destination
        $directMove = new Cell(0,0);

        if ($pieceToMove->getX() > $destCell->getX()) {

            //move left
            $directMove->setX($pieceToMove->getX()-1);

        } else if ($pieceToMove->getX() < $destCell->getX()) {

            //move right
            $directMove->setX($pieceToMove->getX()+1);

        } else {

            //don't move
            $directMove->setX($pieceToMove->getX());

        }

        //calculate vertical movement
        if ($pieceToMove->getY() > $destCell->getY()) {

            //move down
            $directMove->setY($pieceToMove->getY()-1);

        } else if ($pieceToMove->getY() < $destCell->getY()) {

            //move up
            $directMove->setY($pieceToMove->getY()+1);

        } else {

            //don't move
            $directMove->setY($pieceToMove->getY());
            
        }

        return $directMove;

    }

    /*\
    |*| Function: move
    |*|     => Description:
    |*|         Moves the piece backward in case too many pieces in the
    |*|         way
    |*|     => Parameters:
    |*|         -> Cell pieceToMove: cell representing the piece to
    |*|             move
    |*|         -> Cell destCell: cell representing the destination
    |*|     => Returns:
    |*|         -> Cell directMove: cell representing the cell to move
    |*|             to
    \*/
    function antiMove($pieceToMove,$destCell) {

        //calculate direct move toward destination
        $directMove = new Cell(0,0);

        if ($pieceToMove->getX() > $destCell->getX()) {

            //move left
            $directMove->setX($pieceToMove->getX()+1);

        } else if ($pieceToMove->getX() < $destCell->getX()) {

            //move right
            $directMove->setX($pieceToMove->getX()-1);

        } else {

            //don't move
            $directMove->setX($pieceToMove->getX());

        }

        //calculate vertical movement
        if ($pieceToMove->getY() > $destCell->getY()) {

            //move down
            $directMove->setY($pieceToMove->getY()+1);

        } else if ($pieceToMove->getY() < $destCell->getY()) {

            //move up
            $directMove->setY($pieceToMove->getY()-1);

        } else {

            //don't move
            $directMove->setY($pieceToMove->getY());
            
        }

        return $directMove;

    }

    /*\
    |*| Function: determineJump
    |*|     => Description:
    |*|         Determines if there is a piece to jump along the direct 
    |*|         path to the destination and adjusts the next move to 
    |*|         account for such a jump
    |*|         If there is a piece at the location you want to jump
    |*|             to, move that piece first (also sees if that piece
    |*|             can jump, and so on, until a piece is found that
    |*|             can be moved)
    |*|     => Parameters:
    |*|         -> pieces: array of cells representing pieces
    |*|         -> Int pieceToMove: index of the piece to move
    |*|         -> move: cell representing the move to make
    |*|         -> Int counter: int showing how many pieces may be in 
    |*|             the way of a direct move of the piece
    |*|         -> Cell destCell: cell representing the destination
    |*|         -> enemy: array of enemy pieces
    |*|     => Returns:
    |*|         -> Cell newMove: the cell to move to
    |*| 
    \*/
    function determineJump($pieces,$pieceToMove,$move,$counter,
        $destCell,$enemy) {

        $numPieces = sizeof($pieces);
        $newMove = array();
        $newMove["destx"] = $move->getX();
        $newMove["desty"] = $move->getY();
        $newMove["piecex"] = $pieces[$pieceToMove]->getX();
        $newMove["piecey"] = $pieces[$pieceToMove]->getY();

        //check location of pieces to find if there is one to jump
        for ($piece = 0; $piece < $numPieces; $piece++) {
            
            //if there's a piece to jump
            if ( ($pieces[$piece]->getX() === $move->getX() &&
                $pieces[$piece]->getY() === $move->getY()) ||
                ($enemy[$piece]->getX() === $move->getX() &&
                $enemy[$piece]->getY() === $move->getY() &&
                $counter < 2) ) {

                //look at next cell until a piece is found that can be
                //moved                
                $jumpMove = move($move,$destCell);
                $newMove = determineJump($pieces,$piece,$jumpMove,
                    $counter+1,$destCell,$enemy);
                break;

              //else if there is an enemy in the way further down too
            } else if ($enemy[$piece]->getX() === $move->getX() &&
                $enemy[$piece]->getY() === $move->getY() &&
                $counter > 1){

                $newMove["jump"] = false;
                break;

            } else {

                //valid jump available
                if ($counter === 2) {
                    
                    if ($newMove["piecex"] !== $newMove["destx"] &&
                        $newMove["piecey"] !== $newMove["desty"]) {

                        $newMove["jump"] = true;
                        
                    }

                }

            }

        }

        //make sure we have the right piece jump
        if (isset($newMove["jump"])) {

            $newMove["piecex"] = $pieces[$pieceToMove]->getX();
            $newMove["piecey"] = $pieces[$pieceToMove]->getY();

            if (!$newMove["jump"]) {

                $newDest = antiMove($pieces[$pieceToMove],$destCell);
                $newMove["destx"] = $newDest->getX();
                $newMove["desty"] = $newDest->getY();

            }

        }

        return $newMove;

    }

    /*\
    |*| Function: initGame
    |*|     => Description:
    |*|         Retrieves the game data from the UI and parses it for
    |*|         use by the AI and then runs the program
    \*/
    function initGame() {

        //get data
        $jsonString = file_get_contents("php://input");
        //echo $jsonString . "<br>";
        $gameData = json_decode($jsonString,true);

        //set pieces as cells
        $pieces = $gameData["pieces"];
        $pieces = setPieces($pieces);

        //set enemy pieces as cells
        $enemy = $gameData["enemy"];
        $enemy = setPieces($enemy);

        //set destinations as cells
        $destRegion = $gameData["destinations"];
        $destRegion = setDestinations($destRegion);

        //check if pieces are in destinations
        checkIfArrived($pieces,$destRegion);

        //make next move
        $nextMove = getMove($pieces,$destRegion,$enemy);

        //return JSON of next move
        $nextMove = array (
            'from' => array('x' => $nextMove['piecex'],
                'y' => $nextMove['piecey']),
            'to' => array(array('x' => $nextMove['destx'],
                'y' => $nextMove['desty']))
        );

        echo json_encode($nextMove);

    }


    /*\
    |*| Function: setPieces
    |*|     => Description:
    |*|         Creates cell objects for each piece x,y coordinate
    |*|     => Parameters:
    |*|         -> pieces: array of piece coordinates
    |*|     => Returns:
    |*|         -> piecesAsCells: array of cells with piece coords
    \*/
    function setPieces($pieces) {

        $piecesAsCells = array();
        $numPieces = sizeof($pieces);

        for ($piece = 0; $piece < $numPieces; $piece++) {

            $newPiece = new Cell($pieces[$piece]["x"],
                $pieces[$piece]["y"]);
            array_push($piecesAsCells, $newPiece);

        }

        return $piecesAsCells;

    }

    /*\
    |*| Function: setDestinations
    |*|     => Description:
    |*|         Creates cell objects for each destination x,y coord
    |*|     => Parameters:
    |*|         -> dests: array of destination coords
    |*|     => Returns:
    |*|         -> destsAsCells: array of cells with destination coords
    \*/
    function setDestinations($dests) {

        $destsAsCells = array();
        $numDests = sizeof($dests);

        for ($dest = 0; $dest < $numDests; $dest++) {

            $newDest = new Cell($dests[$dest]["x"],
                $dests[$dest]["y"]);
            array_push($destsAsCells, $newDest);

        }

        return $destsAsCells;

    }

    /*\
    |*| Function: checkIfArrived
    |*|     => Description:
    |*|         Checks if pieces are at final destinations and sets
    |*|         $arrived to true for each piece at its destination
    |*|         and for each destination cell that is occupied
    |*|     => Parameters:
    |*|         -> pieces: array of piece coords
    |*|         -> dests: array of destination coords
    |*|     => Returns:
    |*|         -> pieces: array of cells with piece coords w/updates
    |*|             for any cell at its final destination
    \*/
    function checkIfArrived(&$pieces,&$dests) {

        $numDests = sizeof($dests);
        $numPieces = sizeof($pieces);

        //check if any pieces at the back of the destination region
        for ($dest = 0; $dest < $numDests; $dest++) {

            for ($piece = 0; $piece < $numPieces; $piece++) {
        
                if ($pieces[$piece]->getX() === 
                        $dests[$dest]->getX() && 
                        $pieces[$piece]->getY() === 
                        $dests[$dest]->getY()) {

                    $pieces[$piece]->setArrived();
                    $dests[$dest]->setArrived();
                    break;

                }

            }

        }

    }

    /*\
    |*| Run AI
    \*/

    initGame();

?>