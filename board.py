from random import shuffle
# ROOT ClASS, CHILD IS pieceMoves.py

class Board(object):
    def __init__(self,squares={},board=[],files=['a','b','c','d','e','f','g','h'],\
    ranks=['1','2','3','4','5','6','7','8'],kingWatcher = [],moveHistory = [],rookWatcher = [],\
    moveFuture = [],currentPlayer = 'w',computerPlayer = ''):
        self.squares = squares
        self.ranks = ranks
        self.files = files
        self.board = board
        self.computerPlayer = computerPlayer
        
        # moveHistory is a list of lists that is started with newGame() and updated at the end of movePiece()
        #  moveHistory will look like this [[MOVENUMBER,[fromSquare,toSquare],pieceThatMoved,boardStateDictionary],...etc
        self.moveHistory = moveHistory
        ########
        self.moveFuture = moveFuture
        self.currentPlayer = currentPlayer
        
        # these look for king or rook movement to allow for castling
        self.kingWatcher = kingWatcher
        self.rookWatcher = rookWatcher
        
        
        # build the board from the lists of ranks and files.
        # The board is just a list of strings representing the squares in an order,
        #     the order could be different depending on how someone thinks about it,
        #       so we have to remember what order we put the squares in
        for x in ranks:
            for y in files:
                board.append(y+x)
        # these 2 forLoops populate the dictionary with an 'empty' value for each square
        # the value isn't actually empty, it is 2 whitespaces. This allows to do things like compare the first 
        #   or second element of an empty square with an occupied square.
        #  the 2 spaces in empty squares also allow for a quick board representation to 
        #     be printed to the screen
        for filey in files:
            for ranky in ranks:
                squares[filey+ranky] = '  '
    
    # go back to before your last move decision
    def undoMove(self):
        if len(self.moveHistory) >= 3:
            self.squares = self.moveHistory[-3][-1].copy() # without .copy() this is confusing behavior!
            self.rookWatcher = self.moveHistory[-3][-2][0]
            self.kingWatcher = self.moveHistory[-3][-2][1]
            self.moveHistory.pop()
            self.moveHistory.pop()
        elif len(self.moveHistory) == 2:
            self.squares = self.moveHistory[-2][-1].copy()
            self.rookWatcher = self.moveHistory[-2][-2][0]
            self.kingWatcher = self.moveHistory[-2][-2][1]
            self.moveHistory.pop()
            self.currentPlayer = 'w'
        
    # Start a new game
    def newGame(self):
        for filey in self.files:
            for ranky in self.ranks:
                self.squares[filey+ranky] = '  '
        self.kingWatcher = []
        self.rookWatcher = []
        self.moveHistory = []
        self.moveFuture = []
        self.currentPlayer = 'w'
        for x in self.files:
            self.squares[x+'2'] = 'wp'
        self.squares['a1'] = 'wr'
        self.squares['h1'] = 'wr'
        self.squares['b1'] = 'wn'
        self.squares['g1'] = 'wn'
        self.squares['c1'] = 'wb'
        self.squares['f1'] = 'wb'
        self.squares['d1'] = 'wq'
        self.squares['e1'] = 'wk'
        
        for x in self.files:
            self.squares[x+'7'] = 'bp'
        self.squares['a8'] = 'br'
        self.squares['h8'] = 'br'
        self.squares['b8'] = 'bn'
        self.squares['g8'] = 'bn'
        self.squares['c8'] = 'bb'
        self.squares['f8'] = 'bb'
        self.squares['d8'] = 'bq'
        self.squares['e8'] = 'bk'
        #initialize moveHistory
        self.moveHistory = [[0,['  ','  '],'  ',[self.rookWatcher[:],self.kingWatcher[:]],self.squares.copy()]]
    