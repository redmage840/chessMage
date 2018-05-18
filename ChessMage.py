# Porting to Python3
# Current error:
'''
debug in coordsToSquare
debug in coordsToSquare
Exception in Tkinter callback
Traceback (most recent call last):
  File "/Users/crazyfox/anaconda3/lib/python3.6/tkinter/__init__.py", line 1699, in __call__
    return self.func(*args)
  File "ChessMage.py", line 81, in callBackLeftClick
    self.storeMove(squareName)
  File "ChessMage.py", line 86, in storeMove
    self.oldColor = self.canvas.itemconfigure(square,'fill')[-1]
  File "/Users/crazyfox/anaconda3/lib/python3.6/tkinter/__init__.py", line 2572, in itemconfigure
    return self._configure(('itemconfigure', tagOrId), cnf, kw)
  File "/Users/crazyfox/anaconda3/lib/python3.6/tkinter/__init__.py", line 1469, in _configure
    return self._getconfigure1(_flatten((self._w, cmd, '-'+cnf)))
  File "/Users/crazyfox/anaconda3/lib/python3.6/tkinter/__init__.py", line 1458, in _getconfigure1
    return (x[0][1:],) + x[1:]
IndexError: tuple index out of range
'''

import tkinter as tk
from tkinter import ttk
# from ttk import Button, Label
import sys,moveLogic
# Need to fix: add 3 time board repetition, 50 move king stalemate, checkmate with en passant move available to remove check, make en passant and castling aware to findDeepThreats()
# Need to add: more efficient find checkmates. Player is able to draw by moving king back and forth when threatened by the queen alone.
# 
# GameBoard.board.moveHistory has 4 elems; moveNumber,[rookWatcher,kingWatcher], [moveFromSquare,moveToSquare], pieceMoved,[rookWatcher,kingWatcher] self.squares.copy()
class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=64, color1="white", color2="lightgreen", oldColor='',\
    firstSquare='  ',secondSquare='  '):
        self.rows = rows
        self.columns = columns 
        self.size = size # size is individual square size in pixels
        self.color1 = color1 # light color, ie white
        self.color2 = color2 # dark color, ie darkgreen
        self.oldColor = oldColor # this holds the old square color for highlighting selected square
        self.firstSquare = firstSquare # holds first square clicked
        self.secondSquare = secondSquare # holds second square clicked
        
        self.nameToCoords = {} # {'wp3':(6,2)...}
        self.squaresToName = {} # this will map squares to pieces, {'c2':'wp3'...}
        
        # initialize underlying board class (does underlying game logic)
        self.board = moveLogic.Board()
        
        canvas_width = columns * size 
        canvas_height = rows * size
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self)
        label1.pack()
        button1 = ttk.Button(label1,text="QUIT!",command=sys.exit)
        button1.pack(side=tk.LEFT)
        button2 = ttk.Button(label1,text="New Game",command=self.newGame)
        button2.pack(side=tk.LEFT)
        button3 = ttk.Button(label1,text="Undo Move",command=self.undoMove)
        button3.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height)
        self.canvas.bind("<Button-1>",self.callBackLeftClick)
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        self.canvas.bind("<Configure>", self.refresh)
        
        self.board.newGame()
        
    def undoMove(self):
        self.board.undoMove()
        self.refreshPiecePositions()

    def endOfGameButton(self,popup):
        self.newGame()
        popup.destroy()
        
    def popupWindowCheckMate(self,msg):
        popup = tk.Tk()
        popup.wm_attributes("-topmost",1)
        popup.focus_force()
        popup.wm_title("End of Game!")
        label = ttk.Label(popup, text=msg,font=("Helvetica", 16),anchor=tk.CENTER,relief='groove')
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="??????  Start New Game  ??????", command = lambda popup=popup: self.endOfGameButton(popup))
        B1.pack()
        popup.mainloop()
        
    def popupWindowStaleMate(self,msg):
        popup = tk.Tk()
        popup.wm_attributes("-topmost",1)
        popup.focus_force()
        popup.wm_title("End of Game!")
        label = ttk.Label(popup, text=msg,font=("Helvetica", 16),anchor=tk.CENTER,relief='groove')
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="??????  Start New Game  ??????", command = lambda popup=popup: self.endOfGameButton(popup))
        B1.pack()
        popup.mainloop()
        
        # left click on board
    def callBackLeftClick(self,event):
        file = (event.x / self.size) 
        rank = (event.y / self.size)
        squareName = self.coordsToSquare(file,rank)
        self.storeMove(squareName)
        
        # store board click, check for legality, check for checkmate
    def storeMove(self,square): 
        if self.firstSquare == '  ':
            self.oldColor = self.canvas.itemconfigure(square,'fill')[-1]
            self.canvas.itemconfigure(square,fill='darkblue')
            self.firstSquare = square

        else:
            if square == self.firstSquare:
                self.canvas.itemconfigure(self.firstSquare,fill=self.oldColor)
                self.firstSquare = '  '
            elif self.board.isLegal(self.firstSquare,square,self.board.currentPlayer):
                self.secondSquare = square
                self.makeMove(self.firstSquare,self.secondSquare)
                if self.board.hasCheckMate(self.board.currentPlayer) == 1:
                    self.popupWindowCheckMate('checkmate!')
                self.switchCurrentPlayer()
                self.canvas.itemconfigure(self.firstSquare,fill=self.oldColor)
                self.firstSquare = '  '
                self.secondSquare = '  '
                if self.board.currentPlayer == 'b':
                    if self.board.findAllMoves(self.board.currentPlayer) == {}:
                        self.popupWindowStaleMate('stalemate')
                    move = self.board.randomMove('b')
                    self.makeMove(move[0],move[1])
                    if self.board.hasCheckMate(self.board.currentPlayer) == 1:
                        self.popupWindowCheckMate('checkmate!')
                    self.switchCurrentPlayer()
                    if self.board.findAllMoves(self.board.currentPlayer) == {}:
                        self.popupWindowStaleMate('stalemate')
        # move the piece(s) on the board and underlying board class
    def makeMove(self,fromSquare,toSquare):
        self.board.movePiece(fromSquare,toSquare)
        self.refreshPiecePositions()
        
        # called at end of makeMove
    def refreshPiecePositions(self):
        self.squaresToName = {}
        self.nameToCoords = {}
        newSquaresToName = {}
        for square, piece in self.board.squares.items():
            if piece == '  ':
                continue
            if piece not in newSquaresToName.values():
                newSquaresToName[square] = piece
            else:
                count = 0
                for x in newSquaresToName.values():
                    if x[0:2] == piece:
                        count += 1
                newSquaresToName[square] = piece+str(count)
        self.canvas.delete('piece')
        self.squaresToName = newSquaresToName.copy()
        for square,name in newSquaresToName.items():
            coords = self.squareToCoords(square)
            imageName = self.getImage(name)
            self.addPiece(name,imageName,coords[0],coords[1])
            
        # called in refreshPiecePositions
    def getImage(self,pieceName):
        x = pieceName[0:2]
        if x == 'wp':
            return whitePawn
        elif x == 'bp':
            return blackPawn
        elif x == 'wn':
            return whiteKnight
        elif x == 'bn':
            return blackKnight
        elif x == 'wb':
            return whiteBishop
        elif x == 'bb':
            return blackBishop
        elif x == 'wr':
            return whiteRook
        elif x == 'br':
            return blackRook
        elif x == 'wq':
            return whiteQueen
        elif x == 'bq':
            return blackQueen
        elif x == 'wk':
            return whiteKing
        elif x == 'bk':
            return blackKing
    
        # called by storeMove
    def switchCurrentPlayer(self):
        if self.board.currentPlayer == 'w':
            self.board.currentPlayer = 'b'
        elif self.board.currentPlayer == 'b':
            self.board.currentPlayer = 'w'
            
        # create image with name and image object on canvas
    def addPiece(self, name, image, row=0, column=0):
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placePiece(name, row, column)
        
        # move an image by name on the canvas
    def placePiece(self, name, row, column):
        self.nameToCoords[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)
        
        # reset underlying board and images
    def newGame(self):
        self.board.newGame() # reset underlying board class
        self.squaresToName = {}
        self.canvas.delete("piece") # this deletes all images with tag 'piece' (all of them)
        self.addPiece("br1", blackRook, 0,0)
        self.addPiece("bn1", blackKnight, 0,1)
        self.addPiece("bb1", blackBishop, 0,2)
        self.addPiece("bq", blackQueen, 0,3)
        self.addPiece("bk", blackKing, 0,4)
        self.addPiece("bb2", blackBishop, 0,5)
        self.addPiece("bn2", blackKnight, 0,6)
        self.addPiece("br2", blackRook, 0,7)
        for x in range(8):
            self.addPiece("bp"+str(x),blackPawn,1,x)
        self.addPiece("wr1", whiteRook, 7,0)
        self.addPiece("wn1", whiteKnight, 7,1)
        self.addPiece("wb1", whiteBishop, 7,2)
        self.addPiece("wq", whiteQueen, 7,3)
        self.addPiece("wk", whiteKing, 7,4)
        self.addPiece("wb2", whiteBishop, 7,5)
        self.addPiece("wn2", whiteKnight, 7,6)
        self.addPiece("wr2", whiteRook, 7,7)
        for x in range(8):
            self.addPiece("wp"+str(x), whitePawn, 6,x)
        for piece,coords in self.nameToCoords.items():
            square = self.coordsToSquare(coords[1],coords[0])
            self.squaresToName[square] = piece
            
        # refresh board on resize of window
    def refresh(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                # get square name of rectangle object here, ie 'e2'
                fileRank = ''
                if col == 0:
                    fileRank = 'a'
                elif col == 1:
                    fileRank = 'b'
                elif col == 2:
                    fileRank = 'c'
                elif col == 3:
                    fileRank = 'd'
                elif col == 4:
                    fileRank = 'e'
                elif col == 5:
                    fileRank = 'f'
                elif col == 6:
                    fileRank = 'g'
                elif col == 7:
                    fileRank = 'h'
                if row == 0:
                    fileRank += '8'
                elif row == 1:
                    fileRank += '7'
                elif row == 2:
                    fileRank += '6'
                elif row == 3:
                    fileRank += '5'
                elif row == 4:
                    fileRank += '4'
                elif row == 5:
                    fileRank += '3'
                elif row == 6:
                    fileRank += '2'
                elif row == 7:
                    fileRank += '1'
                x = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags=("square",fileRank))
                color = self.color1 if color == self.color2 else self.color2
        for name in self.nameToCoords:
            self.placePiece(name, self.nameToCoords[name][0], self.nameToCoords[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        
        # examples: (0,0) returns 'a8' , (0,1) returns 'a7'
    def coordsToSquare(self,row,column):
        file = ''
        rank = ''
        if row == 0:
            file = 'a'
        elif row == 1:
            file = 'b'
        elif row == 2:
            file = 'c'
        elif row == 3:
            file = 'd'
        elif row == 4:
            file = 'e'
        elif row == 5:
            file = 'f'
        elif row == 6:
            file = 'g'
        elif row == 7:
            file = 'h'
        else:
            print('debug in coordsToSquare')
        if column == 0:
            rank = '8'
        elif column == 1:
            rank = '7'
        elif column == 2:
            rank = '6'
        elif column == 3:
            rank = '5'
        elif column == 4:
            rank = '4'
        elif column == 5:
            rank = '3'
        elif column == 6:
            rank = '2'
        elif column == 7:
            rank = '1'
        else:
            print('debug in coordsToSquare')
        return file+rank
        
        # examples: 'a8' returns (0,0) , 'a7' returns (0,1)
    def squareToCoords(self,square):
        row = 0
        column = 0
        if square[0] == 'a':
            column = 0
        elif square[0] == 'b':
            column = 1
        elif square[0] == 'c':
            column = 2
        elif square[0] == 'd':
            column = 3
        elif square[0] == 'e':
            column = 4
        elif square[0] == 'f':
            column = 5
        elif square[0] == 'g':
            column = 6
        elif square[0] == 'h':
            column = 7
        if square[1] == '8':
            row = 0
        elif square[1] == '7':
            row = 1
        elif square[1] == '6':
            row = 2
        elif square[1] == '5':
            row = 3
        elif square[1] == '4':
            row = 4
        elif square[1] == '3':
            row = 5
        elif square[1] == '2':
            row = 6
        elif square[1] == '1':
            row = 7
        return (row,column)
            
        
if __name__ == "__main__":
    guiBoard = GameBoard(tk.Tk().title('`.-~<@*.*,*~~<!|!->-~ChessMage~-<-!|!>~~*,*.*@>~-.`'))
    guiBoard.pack(side="top", fill="both", expand="true", padx=0, pady=0)
    whiteKing = tk.PhotoImage(file="wk.gif")
    blackPawn = tk.PhotoImage(file="bp.gif")
    blackKnight = tk.PhotoImage(file="bn.gif")
    blackRook = tk.PhotoImage(file="br.gif")
    blackBishop = tk.PhotoImage(file="bb.gif")
    blackQueen = tk.PhotoImage(file="bq.gif")
    blackKing = tk.PhotoImage(file="bk.gif")
    whitePawn = tk.PhotoImage(file="wp.gif")
    whiteKnight = tk.PhotoImage(file="wn.gif")
    whiteRook = tk.PhotoImage(file="wr.gif")
    whiteBishop = tk.PhotoImage(file="wb.gif")
    whiteQueen = tk.PhotoImage(file="wq.gif")
    
    guiBoard.newGame()
    
    guiBoard.mainloop()