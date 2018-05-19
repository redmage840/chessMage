# ROOT ClASS, CHILD IS pieceMoves.py

class Board(object):
    def __init__(self,squares={},board=[],kingWatcher = [],moveHistory = [],rookWatcher = [],currentPlayer = 'w',computerPlayer = ''):
        self.squares = squares
        self.board = board
        self.computerPlayer = computerPlayer
        # moveHistory is a list of lists that is intialized with Board.newGame() and updated by movePiece()
        #  moveHistory elements look like this [[MOVENUMBER,[fromSquare,toSquare],pieceThatMoved,boardStateDictionary],...etc]
        self.moveHistory = moveHistory
        self.currentPlayer = currentPlayer
        # these watch for king or rook movement to allow/prevent for castling
        self.kingWatcher = kingWatcher
        self.rookWatcher = rookWatcher
        # build the board from the lists of ranks and files.
        for rank in ['1','2','3','4','5','6','7','8']:
            for file in ['a','b','c','d','e','f','g','h']:
                board.append(file+rank)
        # These forLoops populate the dictionary with 2 whitespaces value for each rank/file key. 
        # The 2 spaces in empty squares allow for board representation to 
        #     be printed to the terminal
        for file in ['a','b','c','d','e','f','g','h']:
            for rank in ['1','2','3','4','5','6','7','8']:
                squares[file+rank] = '  '
    
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
        for file in ['a','b','c','d','e','f','g','h']:
            for rank in ['1','2','3','4','5','6','7','8']:
                self.squares[file+rank] = '  '
        self.kingWatcher = []
        self.rookWatcher = []
        self.moveHistory = []
        self.currentPlayer = 'w'
        for x in ['a','b','c','d','e','f','g','h']:
            self.squares[x+'2'] = 'wp'
        self.squares['a1'] = 'wr'
        self.squares['h1'] = 'wr'
        self.squares['b1'] = 'wn'
        self.squares['g1'] = 'wn'
        self.squares['c1'] = 'wb'
        self.squares['f1'] = 'wb'
        self.squares['d1'] = 'wq'
        self.squares['e1'] = 'wk'
        
        for x in ['a','b','c','d','e','f','g','h']:
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