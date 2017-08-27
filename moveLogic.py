from random import choice
import pieceMoves
# Moves are evaluated and decided upon here
# Extends Board class
class Board(pieceMoves.Board): 

# figure out way to print move chains

# need to make a combined version of isInCheck and hasCheckMate...

# instead of using eval points, maybe just get values of captured pieces 

# need to enforce paradox of pawns


##################################
# stuff below here is very important to increasing move complexity/time/processing

    # used to find legal moves, used in hasCheckMate(), findAllMoves(), findKingMoves()
    # calls findAllThreatenedSquares()
    def isInCheck(self,player):
        if player == 'w':
            enemyMovesDict = self.findAllThreatenedSquares('b')
            for enemyMoves in enemyMovesDict.values():
                if enemyMoves != []:
                    for enemyMove in enemyMoves:
                        if self.squares[enemyMove] == 'wk':
                            return 1
            return 0
        elif player == 'b':
            enemyMovesDict = self.findAllThreatenedSquares('w')
            for enemyMoves in enemyMovesDict.values():
                if enemyMoves != []:
                    for enemyMove in enemyMoves:
                        if self.squares[enemyMove] == 'bk':
                            return 1
            return 0

    def hasCheckMate(self,player):
        if player == 'w':
            if self.findAllMoves('b') == {} and self.isInCheck('b') == True:
                return 1
            else:
                return 0
        elif player == 'b':
            if self.findAllMoves('w') == {} and self.isInCheck('w') == True:
                return 1
            else:
                return 0

    def isLegal(self,moveFrom,moveTo,player):
        playersMoves = self.findAllMoves(player)
        if moveFrom in playersMoves.keys():
            if moveTo in playersMoves[moveFrom]:
                return 1
        else:
            return 0
    
    # current decisions made here, called in randomMove(), filtered with filterDeepThreats() which returns the move, ie ['e2','e4']
    def findDeepThreats(self,player):
        max = -100 # store value of highest move 
        bestMove = []
        myMovesDict = self.findAllMoves(player) # store first level of moves
        myNextThreats = [] 
        startPoints = self.evalPlayerPoints(player)
        if player == 'b':
            enemyPoints = self.evalPlayerPoints('w')
        elif player == 'w':
            enemyPoints = self.evalPlayerPoints('b')
        for pieceSquare,moves in myMovesDict.items(): # For each potential move
            for moveSquare in moves:
                oldFrom = self.squares[pieceSquare] 
                oldTo = self.squares[moveSquare]
                self.safeMovePiece(pieceSquare,moveSquare)# make first hypothetical move
                score = 0
                # begin black player logic, no white player logic (human)
                if player == 'b':
                    # can I checkmate?
                    if self.hasCheckMate('b') == 1:
                        self.squares[pieceSquare] = oldFrom
                        self.squares[moveSquare] = oldTo
                        return [pieceSquare,moveSquare] 
                    # add points for promoting a pawn
                    if oldFrom == 'bp':
                        if moveSquare[1] == '1':
                            score += 6
                        elif moveSquare[1] == '2':
                            score += 2
                        elif moveSquare == 'e5'or moveSquare == 'd6' or moveSquare == 'b6':
                            score += 1
                    elif oldFrom == 'bn':
                        if pieceSquare == 'b8' and moveSquare == 'c6':
                            score += 1
                        elif pieceSquare == 'g8' and moveSquare == 'f6':
                            score += 1
                    elif oldFrom == 'bk':
                        if pieceSquare == 'e8' and (moveSquare == 'g8' or moveSquare == 'c8'):
                            score += 2
                        else:
                            score -= 1
                    elif oldFrom == 'bb':
                        if pieceSquare == 'f8' and moveSquare == 'g7':
                            score += 1
                        elif pieceSquare == 'c8' and moveSquare == 'b7':
                            score += 1
                    newEnemyPoints = self.evalPlayerPoints('w')
                    if enemyPoints > newEnemyPoints:
                        score += (enemyPoints-newEnemyPoints)
                        
                    # should return move

                    bestResponseAndScore = self.bestCapture('w')
                    #print 'potential move chain is ' + pieceSquare,moveSquare,bestResponseAndScore[0],bestResponseAndScore[1]
                    if bestResponseAndScore != []:
                        score -= bestResponseAndScore[-1]
                        
                    if score > max:
                        bestMove = [pieceSquare,moveSquare]
                        max = score
                self.squares[pieceSquare] = oldFrom # undo original move
                self.squares[moveSquare] = oldTo
        return bestMove
        
        
        
    # used in findDeepThreats
    # at this point, a potential move has been made for black, finding best 'w' response
    def bestCapture(self,player):
        if player == 'w':
            moveDict = self.findAllMoves('w')
        elif player == 'b':
            moveDict = self.findAllMoves('b')
        max = -10
        bestMove = []
        for startSquare,moves in moveDict.items():
            for moveSquare in moves: # for each move,
                pieceVal = self.pieceValue(self.squares[moveSquare]) # get the value of piece about to be captured
                oldFrom = self.squares[startSquare] 
                oldTo = self.squares[moveSquare]
                self.safeMovePiece(startSquare,moveSquare) # make the move,

                
                # for the response, what is the best response from 'b'?
                bestCap2 = self.bestCapture2('b')
                
                moveVal = pieceVal - bestCap2-1
                # the lower moveVal, the worse it is for white
                # try to print out the moves that lead up to this point
                self.squares[startSquare] = oldFrom
                self.squares[moveSquare] = oldTo
                if moveVal > max:
                    bestMove = [startSquare,moveSquare,moveVal]
                    max = moveVal
        return bestMove
        
    # should just return int value to bestCapture
    def bestCapture2(self,player):
        if player == 'b':
            moveDict = self.findAllMoves('b')
        elif player == 'w':
            moveDict = self.findAllMoves('w')
        max = -10
        if moveDict == {}:
            return 0
        for startSquare, moves in moveDict.items():
            for moveSquare in moves:
                pieceVal = self.pieceValue(self.squares[moveSquare])
                if pieceVal > max:
                    max = pieceVal
        return max
###############################
    # stuff below here is not very crucial to increasing move complexity
    # it does have some effect
    # makes a random, legal move for a player, takes 'w'|'b' as arg, returns list with move, ie ['e2','e4']
    def randomMove(self,player):
        if player == 'b':
            thinkingMove = self.findDeepThreats(player)
            if thinkingMove != []:
                #print 'thinking move'
                return thinkingMove
            else:
                print 'black random move coming up'
        # make a random move
        moves = self.findAllMoves(player) 
        piecesWithMoves = []
        for key in moves:
            if moves[key] != []:
                piecesWithMoves.append(key)
        if piecesWithMoves == []:
            return []
        fromSquare = choice(piecesWithMoves)
        toSquare = choice(moves[fromSquare])
        return [fromSquare,toSquare]
                
    # takes string piece, ie 'wb' or 'bp', and returns an int 
    def pieceValue(self,piece):
        if piece[1] == 'p':
            return 1
        elif piece[1] == 'n':
            return 3
        elif piece[1] == 'b':
            return 3
        elif piece[1] == 'r':
            return 5
        elif piece[1] == 'q':
            return 9
        elif piece[1] == 'k':
            return 50
        elif piece == '  ':
            return 0
            
    # adds up the point value of each piece from a player ('w'|'b')
    #  and returns int value of all pieces, king's value of 40 is subtracted
    def evalPlayerPoints(self,player):
        tally = 0
        for piece in self.squares.values():
            if piece[0] == player:
                tally += self.pieceValue(piece)
        # subtract the inflated king value
        tally -= 50
        return tally
            