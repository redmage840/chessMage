import Tkinter as tk
import board
# PARENT IS board.py, CHILD IS moveLogic.py
# Calls findAllMoves, which calls subroutines to return dictionary,
#   Where key is a potential square(string) to be moved FROM,
#   Where value is potential squares(list) to be moved TO
# Example:
#     allMovesGivenBoard = someBoardInstance.findAllMoves('w')
#       gives
#     {'a2':['a3','a4'],'b2':['b3','b4'], etc...}

# these globals are used in promotion, computer defaults to queen
selectedWhitePiece = 'wq'
selectedBlackPiece = 'bq'

# Extend Board class with methods for finding squares to move to
class Board(board.Board):
    # find all squares up, down, left, and right from a given square
    # takes a string ('a2'), returns list of strings (['a3','a4'])
    def findLateralMoves(self,square):
        moves = []
        up = self.board.index(square)+8
        while up < 64:
            if self.squares[self.board[up]] != '  ':
                if self.squares[self.board[up]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[up])
                break
            else:
                moves.append(self.board[up])
                up += 8
        down = self.board.index(square)-8
        while down > 0:
            if self.squares[self.board[down]] != '  ':
                if self.squares[self.board[down]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[down])
                break
            else:
                moves.append(self.board[down])
                down -= 8
        left = self.board.index(square)-1
        while left % 8 != 7:
            if self.board[left][0] == 'a':
                if self.squares[self.board[left]][0] == self.squares[square][0]:
                    break
                else:
                    moves.append(self.board[left])
                    break
            if self.squares[self.board[left]] != '  ':
                if self.squares[self.board[left]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[left])
                break
            else:
                moves.append(self.board[left])
                left -= 1
        right = self.board.index(square) + 1
        while right % 8 != 0:
            if self.board[right][0] == 'h':
                if self.squares[self.board[right]][0] == self.squares[square][0]:
                    break
                else:
                    moves.append(self.board[right])
                    break
            if self.squares[self.board[right]] != '  ':
                if self.squares[self.board[right]][0] == self.squares[square][0]:
                    break
                else:
                    moves.append(self.board[right])
                    break
            else:
                moves.append(self.board[right])
                right += 1
        return moves
    # Finds all diagonals from a given square
    # Takes a string ('a2'), returns a list (['b3','c4',etc])
    def findDiagMoves(self,square):
        moves = []
        topright = self.board.index(square)+9
        while topright < 64 and square[0] != 'h':
            if self.board[topright][0] == 'h':
                if self.squares[self.board[topright]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[topright])
                break
            if self.squares[self.board[topright]] != '  ':
                if self.squares[self.board[topright]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[topright])
                break
            else:
                moves.append(self.board[topright])
                topright += 9
        botright = self.board.index(square)-7
        while botright >= 0 and square[0] != 'h':
            if self.board[botright][0] == 'h':
                if self.squares[self.board[botright]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[botright])
                break
            if self.squares[self.board[botright]] != '  ':
                if self.squares[self.board[botright]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[botright])
                break
            else:
                moves.append(self.board[botright])
                botright -= 7
        topleft = self.board.index(square)+7
        while topleft < 64 and square[0] != 'a':
            if self.board[topleft][0] == 'a':
                if self.squares[self.board[topleft]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[topleft])
                break
            if self.squares[self.board[topleft]] != '  ':
                if self.squares[self.board[topleft]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[topleft])
                break
            else:
                moves.append(self.board[topleft])
                topleft += 7
        botleft = self.board.index(square)-9
        while botleft >= 0 and square[0] != 'a':
            if self.board[botleft][0] == 'a':
                if self.squares[self.board[botleft]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[botleft])
                break
            if self.squares[self.board[botleft]] != '  ':
                if self.squares[self.board[botleft]][0] == self.squares[square][0]:
                    break
                moves.append(self.board[botleft])
                break
            else:
                moves.append(self.board[botleft])
                botleft -= 9
        return moves
    
    # Working on our Knight Moves, Trying to lose the awkward teenage blues
    # Finds Knight moves (L shape) from a given square
    # Takes a string ('c4') returns a list (['b2','d3',etc])
    def findKnightMoves(self,square):
        moves = []
        botLeft = self.board.index(square)
        moveGrid = []
        moveLeft = 2
        moveRight = 2
        moveUp = 2
        moveDown = 2
        if square[0] == 'a':
            moveLeft = 0
        if square[0] == 'b':
            moveLeft = 1
        if square[0] == 'g':
            moveRight = 1
        if square[0] == 'h':
            moveRight = 0
        if square[1] == '8':
            moveUp = 0
        if square[1] == '7':
            moveUp = 1
        if square[1] == '1':
            moveDown = 0
        if square[1] == '2':
            moveDown = 1
        for x in range(moveDown):
            botLeft -= 8
        for x in range(moveLeft):
            botLeft -= 1
        botLeftCopy = botLeft
        for x in range(moveLeft+moveRight+1):
            moveGrid.append(self.board[botLeftCopy])
            botLeftCopy += 1
        for x in range(moveDown+moveUp):
            botLeft += 8
            for x in range(moveLeft+moveRight+1):
                moveGrid.append(self.board[botLeft])
                botLeft += 1
            botLeft -= (moveLeft+moveRight+1)
        #find 5x5 grid with square as center
        scope = [6,-6,10,-10,15,-15,17,-17]
        for x in scope:
            if 0 <= (x + self.board.index(square)) <= 63:
                moves.append(self.board[self.board.index(square)+x])
        newMoves = []
        for x in moves:
            if x in moveGrid:
                if self.squares[x][0] != self.squares[square][0]:
                    newMoves.append(x)
        return newMoves
        
    def findQueenMoves(self,square):
    
        diags = self.findDiagMoves(square)
        lateral = self.findLateralMoves(square)
        moves = diags+lateral
        return moves
        
    def findRookMoves(self,square):
        moves = self.findLateralMoves(square)
        return moves
        
    def findBishopMoves(self,square):
        moves = self.findDiagMoves(square)
        return moves
        
    # en passant moves added, maybe make more apparent that they are captures for board evaluation
    def findPawnMoves(self,square):
        moves = []
        #edge pawns en passant
        if square == 'a5' and self.squares[square] == 'wp':
            lastMovedPiece = self.moveHistory[-1][2]
            lastFromTo = self.moveHistory[-1][1]
            if lastMovedPiece == 'bp':
                if self.board.index(lastFromTo[0])-self.board.index(lastFromTo[1]) == 16:
                    if self.board.index(lastFromTo[1]) == self.board.index(square)+1:
                        moves.append('b6') 
        elif square == 'h5' and self.squares[square] == 'wp':
            lastMovedPiece = self.moveHistory[-1][2]
            lastFromTo = self.moveHistory[-1][1]
            if lastMovedPiece == 'bp':
                if self.board.index(lastFromTo[0])-self.board.index(lastFromTo[1]) == 16:
                    if self.board.index(lastFromTo[1]) == self.board.index(square)-1:
                        moves.append('g6')
        # other en passant 
        elif self.squares[square] == 'wp' and square[1] == '5': #if not an edge pawn and on the 5th rank
            lastMovedPiece = self.moveHistory[-1][2]
            lastFromTo = self.moveHistory[-1][1]
            if lastMovedPiece == 'bp':
                if self.board.index(lastFromTo[0])-self.board.index(lastFromTo[1]) == 16:
                    if self.board.index(lastFromTo[1]) == self.board.index(square)+1:
                        moves.append(self.board[self.board.index(square)+9])
                    if self.board.index(lastFromTo[1]) == self.board.index(square)-1:
                        moves.append(self.board[self.board.index(square)+7])
        # end en passant
        #white pawns can move two squares forward if on starting square
        if self.squares[square] == 'wp' and square[1] == '2':
            if self.squares[self.board[self.board.index(square)+8]] == '  ':
                moves.append(self.board[self.board.index(square)+8])
                if self.squares[self.board[self.board.index(square)+16]] == '  ':
                    moves.append(self.board[self.board.index(square)+16])
            if square[0] == 'h' and self.squares[self.board[self.board.index(square)+7]][0] == 'b':
                moves.append(self.board[self.board.index(square)+7])
            elif square[0] == 'a' and self.squares[self.board[self.board.index(square)+9]][0] == 'b':
                moves.append(self.board[self.board.index(square)+9])
            else:
                if self.squares[self.board[self.board.index(square)+7]][0] == 'b':
                    moves.append(self.board[self.board.index(square)+7])
                if self.squares[self.board[self.board.index(square)+9]][0] == 'b':
                    moves.append(self.board[self.board.index(square)+9])
        #other white pawn moves
        elif self.squares[square] == 'wp':
            if self.board.index(square)+8 < 64 and self.squares[self.board[self.board.index(square)+8]] == '  ':
                moves.append(self.board[self.board.index(square)+8])
            if self.board.index(square)+8 < 64 and square[0] == 'h' and self.squares[self.board[self.board.index(square)+7]][0] == 'b':
                moves.append(self.board[self.board.index(square)+7])
            elif self.board.index(square)+8 < 64 and square[0] == 'a' and self.squares[self.board[self.board.index(square)+9]][0] == 'b':
                moves.append(self.board[self.board.index(square)+9])
                
            else:
                if self.board.index(square)+8 < 64:# problem is here
                    if self.squares[self.board[self.board.index(square)+7]][0] == 'b' and square[0] != 'a':
                        moves.append(self.board[self.board.index(square)+7])
                    if square[0] != 'h':
                        if self.squares[self.board[self.board.index(square)+9]][0] == 'b':
                            moves.append(self.board[self.board.index(square)+9])
                        
        #black's pawns ##################
        # begin black pawn en passant, edge pawns first
        if square == 'a4' and self.squares[square] == 'bp':
            lastMovedPiece = self.moveHistory[-1][2]
            lastFromTo = self.moveHistory[-1][1]
            if lastMovedPiece == 'wp':
                if self.board.index(lastFromTo[1])-self.board.index(lastFromTo[0]) == 16:
                    if self.board.index(lastFromTo[1]) == self.board.index(square)+1:
                        moves.append('b3') 
        elif square == 'h4' and self.squares[square] == 'bp':
            lastMovedPiece = self.moveHistory[-1][2]
            lastFromTo = self.moveHistory[-1][1]
            if lastMovedPiece == 'wp':
                if self.board.index(lastFromTo[1])-self.board.index(lastFromTo[0]) == 16:
                    if self.board.index(lastFromTo[1]) == self.board.index(square)-1:
                        moves.append('g3')
        elif self.squares[square] == 'bp' and square[1] == '4': #if not an edge pawn
            lastMovedPiece = self.moveHistory[-1][2]
            lastFromTo = self.moveHistory[-1][1]
            if lastMovedPiece == 'wp':
                if self.board.index(lastFromTo[1])-self.board.index(lastFromTo[0]) == 16:
                    if self.board.index(lastFromTo[1]) == self.board.index(square)+1:
                        moves.append(self.board[self.board.index(square)-7])
                    if self.board.index(lastFromTo[1]) == self.board.index(square)-1:
                        moves.append(self.board[self.board.index(square)-9])
            # end black pawn en passant
                
        #black pawns can move 2 squares forward from starting square
        if self.squares[square][0] == 'b' and square[1] == '7':
            if self.squares[self.board[self.board.index(square)-8]] == '  ':
                moves.append(self.board[self.board.index(square)-8])
                if self.squares[self.board[self.board.index(square)-16]] == '  ':
                    moves.append(self.board[self.board.index(square)-16])
            if square[0] == 'h':
                if self.squares[self.board[self.board.index(square)-9]][0] == 'w':
                    moves.append(self.board[self.board.index(square)-9])
            elif square[0] == 'a':
                if self.squares[self.board[self.board.index(square)-7]][0] == 'w':
                    moves.append(self.board[self.board.index(square)-7])
            else:
                if self.squares[self.board[self.board.index(square)-7]][0] == 'w':
                    moves.append(self.board[self.board.index(square)-7])
                if self.squares[self.board[self.board.index(square)-9]][0] == 'w':
                    moves.append(self.board[self.board.index(square)-9])
        #other black pawn moves
        elif self.squares[square][0] == 'b':
            if self.board.index(square)-8 >= 0 and self.squares[self.board[self.board.index(square)-8]] == '  ':
                moves.append(self.board[self.board.index(square)-8])
            if self.board.index(square)-8 >= 0 and square[0] == 'h':
                if self.squares[self.board[self.board.index(square)-9]][0] == 'w':
                    moves.append(self.board[self.board.index(square)-9])
            elif self.board.index(square)-8 >= 0 and square[0] == 'a':
                if self.squares[self.board[self.board.index(square)-7]][0] == 'w':
                    moves.append(self.board[self.board.index(square)-7])
            else:
                if self.board.index(square)-8 >= 0:
                    if self.squares[self.board[self.board.index(square)-7]][0] == 'w' and square[0] != 'h':
                        moves.append(self.board[self.board.index(square)-7])
                    if self.squares[self.board[self.board.index(square)-9]][0] == 'w' and square[0] != 'a':
                        moves.append(self.board[self.board.index(square)-9])
                        
        return moves
    #############################
    # these are used to find the king's legal moves
    def kingGrid(self,square):
        moveGrid = []
        
        #find normal king moves
        botLeft = self.board.index(square)
        up,down,left,right = 1,1,1,1
        if square[0] == 'a':
            left -= 1
        if square[0] == 'h':
            right -= 1
        if square[1] == '1':
            down -= 1
        if square[1]== '8':
            up -= 1
        for x in range(down):
            botLeft -= 8
        for x in range(left):
            botLeft -=1
        botLeftCopy = botLeft
        for x in range(left+right+1):
            moveGrid.append(self.board[botLeftCopy])
            botLeftCopy += 1
        for x in range(up+down):
            botLeft += 8
            for y in range(left+right+1):
                moveGrid.append(self.board[botLeft])
                botLeft += 1
            botLeft -= (left+right+1)
        
        return moveGrid
        
    # check for legal castle moves and add to king's moves
    def addCastleMoves(self,square):
        moveGrid = []
        if self.currentPlayer == 'w':
            enemyThreatenedSquares = self.findAllThreatenedSquares('b')
        elif self.currentPlayer == 'b':
            enemyThreatenedSquares = self.findAllThreatenedSquares('w')
        #add castle white queenside to potential moves, castle movement should be resolved in movePiece
        if self.squares[square] == 'wk' and self.squares['b1'] == '  ' \
        and self.squares['c1'] == '  ' and self.squares['d1'] == '  ':
            castle = 0
                #has rook moved? move up
            if 'a1' in self.rookWatcher:
                castle += 1
            for piece,moves in enemyThreatenedSquares.items():
                for move in moves:
                    if move == 'c1' or move == 'd1':
                        castle += 1
            if self.squares['a1'] != 'wr':
                castle += 1
            if castle == 0:
                moveGrid.append('c1')
            #add castle white kingside to potential moves, castle movement should be resolved in movePiece
        if self.squares[square] == 'wk' and self.squares['f1'] == '  ' and self.squares['g1'] == '  ':
            castle = 0
                #has rook moved?
            if 'h1' in self.rookWatcher:
                castle += 1
            for piece,moves in enemyThreatenedSquares.items():
                for move in moves:
                    if move == 'f1' or move == 'g1':
                        castle += 1
            if self.squares['h1'] != 'wr':
                castle += 1
            if castle == 0:
                moveGrid.append('g1')
            #add castle black queenside to potential moves, castle movement resolved in movePiece
        if self.squares[square] == 'bk' and self.squares['b8'] == '  ' and self.squares['c8'] == '  ' and self.squares['d8'] == '  ':
            castle = 0
                #has rook moved?
            if 'a8' in self.rookWatcher:
                castle += 1
            for piece,moves in enemyThreatenedSquares.items():
                for move in moves:
                    if move == 'c8' or move == 'd8':
                        castle += 1
            if self.squares['a8'] != 'br':
                castle += 1
            if castle == 0:
                moveGrid.append('c8')
            #add castle black kingside to potential moves, castle movement resolved in movePiece
        if self.squares[square] == 'bk' and self.squares['f8'] == '  ' and self.squares['g8'] == '  ':
            castle = 0
                #has rook moved?
            if 'h8' in self.rookWatcher:
                castle += 1
            for piece,moves in enemyThreatenedSquares.items():
                for move in moves:
                    if move == 'f8' or move == 'g8':
                        castle += 1
            if self.squares['h8'] != 'br':
                castle += 1
            if castle == 0:
                moveGrid.append('g8')
        return moveGrid
        
    def findKingMoves(self,square):
        movesList = []
        maybeMoves = []
        ####  CASTLING !!!!!! ######## 
        if (self.squares[square] not in self.kingWatcher) and (self.squares[square][1] == 'k')\
         and self.isInCheck(self.currentPlayer) == 0:
            tmp = self.addCastleMoves(square)
            maybeMoves += tmp
        nextToKing = self.kingGrid(square)
        maybeMoves += nextToKing
        movesList += maybeMoves
        if self.squares[square] == 'wk':
            enemyMoveDict = self.findAllThreatenedSquares('b')
        if self.squares[square] == 'bk':
            enemyMoveDict = self.findAllThreatenedSquares('w')
        for move in maybeMoves:
        #  remove squares occupied by friendly pieces
            if self.squares[square][0] == self.squares[move][0]:
                movesList.remove(move)
            # remove moves that put you in check
        for enemyMoves in enemyMoveDict.values():
            if enemyMoves != []:
                for enemyMove in enemyMoves:
                    if enemyMove in movesList:
                        movesList.remove(enemyMove)
        return movesList
        
    ######################################
    # all of these are used to return piece choice in promotion window to underlying game logic
    def promoteChoice(self,piece,popup):
        if piece[0] == 'w':
            global selectedWhitePiece
            selectedWhitePiece = piece
        elif piece[0] == 'b':
            global selectedBlackPiece
            selectedBlackPiece = piece
        popup.quit()
        popup.destroy()
        
    def whitePawnPromote(self):
        self.promoteWhitePopup('Promote!')
        x = selectedWhitePiece
        return x
        
    def blackPawnPromote(self):
        return 'bq'
#         self.promoteBlackPopup('Promote!')
#         x = selectedBlackPiece
#         return x
        
    def promoteWhitePopup(self,msg):
        popup = tk.Tk()
        popup.wm_attributes("-topmost", 1)
        popup.focus_force()
        popup.wm_title("Promote!")
        whiteRook = tk.PhotoImage(master=popup,file='wr.gif')
        whiteKnight = tk.PhotoImage(master=popup,file='wn.gif')
        whiteBishop = tk.PhotoImage(master=popup,file='wb.gif')
        whiteQueen = tk.PhotoImage(master=popup,file='wq.gif')
        label = ttk.Label(popup, text=msg,font=("Helvetica", 16),anchor=tk.CENTER,relief='groove')
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup,image=whiteRook,command=lambda popup=popup:self.promoteChoice('wr',popup))
        B1.pack(side=tk.LEFT)
        B2 = ttk.Button(popup,image=whiteBishop,command=lambda popup=popup:self.promoteChoice('wb',popup))
        B2.pack(side=tk.LEFT)
        B3 = ttk.Button(popup,image=whiteKnight,command=lambda popup=popup:self.promoteChoice('wn',popup))
        B3.pack(side=tk.LEFT)
        B4 = ttk.Button(popup,image=whiteQueen,command=lambda popup=popup:self.promoteChoice('wq',popup))
        B4.pack(side=tk.LEFT)
        popup.mainloop()
        
    def promoteBlackPopup(self,msg):
        popup = tk.Tk()
        popup.wm_attributes("-topmost", 1)
        popup.focus_force()
        popup.wm_title("Promote!")
        blackRook = tk.PhotoImage(master=popup,file='br.gif')
        blackKnight = tk.PhotoImage(master=popup,file='bn.gif')
        blackBishop = tk.PhotoImage(master=popup,file='bb.gif')
        blackQueen = tk.PhotoImage(master=popup,file='bq.gif')
        label = ttk.Label(popup, text=msg,font=("Helvetica", 16),anchor=tk.CENTER,relief='groove')
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup,image=blackRook,command=lambda popup=popup:self.promoteChoice('br',popup))
        B1.pack(side=tk.LEFT)
        B2 = ttk.Button(popup,image=blackBishop,command=lambda popup=popup:self.promoteChoice('bb',popup))
        B2.pack(side=tk.LEFT)
        B3 = ttk.Button(popup,image=blackKnight,command=lambda popup=popup:self.promoteChoice('bn',popup))
        B3.pack(side=tk.LEFT)
        B4 = ttk.Button(popup,image=blackQueen,command=lambda popup=popup:self.promoteChoice('bq',popup))
        B4.pack(side=tk.LEFT)
        popup.mainloop()
    #######################################
    # these find squares that are threatened
    def findPawnDiagonals(self,square):
        pawnDiagonals = []
        if self.squares[square] == 'wp':
            if square[0] == 'a':
                if self.board.index(square)+9 < 64:
                    pawnDiagonals.append(self.board[self.board.index(square)+9])
            elif square[0] == 'h':
                if self.board.index(square)+7 < 64:
                    pawnDiagonals.append(self.board[self.board.index(square)+7])
            else:
                if self.board.index(square)+9 < 64:
                    pawnDiagonals.append(self.board[self.board.index(square)+9])
                if self.board.index(square)+7 < 64:
                    pawnDiagonals.append(self.board[self.board.index(square)+7])
        elif self.squares[square] == 'bp':
            if square[0] == 'a':
                if self.board.index(square)-7 >= 0:
                    pawnDiagonals.append(self.board[self.board.index(square)-7])
            elif square[0] == 'h':
                if self.board.index(square)-9 >= 0:
                    pawnDiagonals.append(self.board[self.board.index(square)-9])
            else:
                if self.board.index(square)-9 >= 0:
                    pawnDiagonals.append(self.board[self.board.index(square)-9])
                if self.board.index(square)-7 >= 0:
                    pawnDiagonals.append(self.board[self.board.index(square)-7])
        return pawnDiagonals
        
    # pass ('w'|'b') to see what squares that player currently threatens, returns dictionary
    def findAllThreatenedSquares(self, player):
    # returns dict of each square to each threaten
        moveHolder = {}
        for square in self.board:
            if self.squares[square][0] == player:
                if self.squares[square][1] == 'p':
                    moveHolder[square] = self.findPawnDiagonals(square)
                if self.squares[square][1] == 'n':
                    moveHolder[square] = self.findKnightMoves(square)
                if self.squares[square][1] == 'b':
                    moveHolder[square] = self.findBishopMoves(square)
                if self.squares[square][1] == 'r':
                    moveHolder[square] = self.findRookMoves(square)
                if self.squares[square][1] == 'k':
                    moveHolder[square] = self.kingGrid(square)
                if self.squares[square][1] == 'q':
                    moveHolder[square] = self.findQueenMoves(square)
        return moveHolder
    #######################################
    # accounts for castling, en passant, promotion
    def movePiece(self, fromSquare, toSquare):
        # en passant
        if self.squares[fromSquare] == 'wp':
            if self.squares[toSquare] == '  ':#if white pawn is moving to empty square
                if (self.board.index(fromSquare) - self.board.index(toSquare)) % 2 != 0:#square is not in front
                    self.squares[self.board[self.board.index(toSquare)-8]] = '  '#remove the piece en passant
        elif self.squares[fromSquare] == 'bp':
            if self.squares[toSquare] == '  ':
                if (self.board.index(fromSquare) - self.board.index(toSquare)) % 2 != 0:
                    self.squares[self.board[self.board.index(toSquare)+8]] = '  '
        # end en passant   
        
        #have rooks moved?
        if fromSquare == 'a1':
            if 'a1' not in self.rookWatcher:
                self.rookWatcher.append('a1')
        elif fromSquare == 'h1':
            if 'h1' not in self.rookWatcher:
                self.rookWatcher.append('h1')
        elif fromSquare == 'a8':
            if 'a8' not in self.rookWatcher:
                self.rookWatcher.append('a8')
        elif fromSquare == 'h8':
            if 'h8' not in self.rookWatcher:
                self.rookWatcher.append('h8')
        #has king moved?
        if self.squares[fromSquare] == 'wk':
            if 'wk' not in self.kingWatcher:
                self.kingWatcher.append('wk')
        elif self.squares[fromSquare] == 'bk':
            if 'bk' not in self.kingWatcher:
                self.kingWatcher.append('bk')
        #pawn promote
        elif self.squares[fromSquare] == 'wp' and toSquare[1] == '8':
            self.squares[fromSquare] = self.whitePawnPromote()
        elif self.squares[fromSquare] == 'bp' and toSquare[1] == '1':
            self.squares[fromSquare] = self.blackPawnPromote()
        #normal move
        self.squares[toSquare] = self.squares[fromSquare]
        self.squares[fromSquare] = '  '
        
        #move rook if white just castled queenside
        if fromSquare == 'e1' and toSquare == 'c1' and self.squares['c1'] == 'wk':
            self.safeMovePiece('a1','d1')
        #move rook if white just castled kingside
        elif fromSquare == 'e1' and toSquare == 'g1' and self.squares['g1'] == 'wk':
            self.safeMovePiece('h1','f1')
        #move rook if black just castled queenside
        elif fromSquare == 'e8' and toSquare == 'c8' and self.squares['c8'] == 'bk':
            self.safeMovePiece('a8','d8')
        #move rook if black just castled kingside
        elif fromSquare == 'e8' and toSquare == 'g8' and self.squares['g8'] == 'bk':
            self.safeMovePiece('h8','f8')
            
        # UPDATE MOVE HISTORY, pieces have already been moved,
        moveNumber = len(self.moveHistory)
        self.moveHistory.append([moveNumber,[fromSquare,toSquare],self.squares[self.board[self.board.index(toSquare)]],[self.rookWatcher[:],self.kingWatcher[:]],self.squares.copy()])
        
    # just move the piece, without accounting for game rules
    def safeMovePiece(self,fromSquare,toSquare):
        self.squares[toSquare] = self.squares[fromSquare]
        self.squares[fromSquare] = '  '
    #######################################
    #returns dictionary of square to move map, ie 'e4':['e5','d5','f5']
    def findAllMoves(self,player):
        moveDict = {}
        for x in self.board:
            if self.squares[x][0] == player:
                if self.squares[x][1] == 'p':
                    moveDict[x] = self.findPawnMoves(x)
                elif self.squares[x][1] == 'n':
                    moveDict[x] = self.findKnightMoves(x)
                elif self.squares[x][1] == 'b':
                    moveDict[x] = self.findBishopMoves(x)
                elif self.squares[x][1] == 'r':
                    moveDict[x] = self.findRookMoves(x)
                elif self.squares[x][1] == 'k':
                    moveDict[x] = self.findKingMoves(x)
                elif self.squares[x][1] == 'q':
                    moveDict[x] = self.findQueenMoves(x)
        # strip off moves that move you into check or discover check on your king
          # must be careful not to strip all moves if already in check
        if self.isInCheck(player) == False:
            strippedMoves = {}
            for piece, moves in moveDict.items():
                if moves != []:
                    for move in moves:
                        oldFrom = self.squares[piece]
                        oldTo = self.squares[move]
                        # right here is the problem with "only move to escape mate is en passant capture"
                        # using safeMovePiece to look for a position that escapes check, does not remove
                        # the en passant captured pawn
                        self.safeMovePiece(piece,move)
                        if self.isInCheck(player) == False:
                            # add to newMoveDict
                            if piece not in strippedMoves:
                                strippedMoves[piece] = [move]
                            else:
                                strippedMoves[piece].append(move)
                        #move pieces back
                        self.squares[piece] = oldFrom
                        self.squares[move] = oldTo
            moveDict = strippedMoves
        # if you are in check, can only move so that you are not in check
        if self.isInCheck(player) == 1:
            newMoveDict = {}
            for fromSquare,toSquares in moveDict.items():
                if toSquares != []:
                    for toSquare in toSquares:
                        oldFrom = self.squares[fromSquare]
                        oldTo = self.squares[toSquare]
                        self.safeMovePiece(fromSquare,toSquare)
                        if self.isInCheck(player) == 0:
                            if fromSquare in newMoveDict:
                                newMoveDict[fromSquare].append(toSquare)
                            else:
                                newMoveDict[fromSquare] = [toSquare]
                        self.squares[fromSquare] = oldFrom
                        self.squares[toSquare] = oldTo
            return newMoveDict
        return moveDict
        
