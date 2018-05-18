# eample FEN string: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
# how are primitives going to operate on board rep?
# what is best board rep for moving stuff around




# takes a string someFEN and a string someSquare, returns list of strings ie ['b3','c2','a1']
def findBishopMoves(someFEN, fromSquare):
    pass
def findKnightMoves(someFEN, fromSquare):
    pass
def findRookMoves(someFEN, fromSquare):
    pass
def findQueenMoves(someFEN, fromSquare):
    pass
def findPawnMoves(someFEN, fromSquare):
    pass
def findKingMoves(someFEN, fromSquare):
    pass

# Takes a FEN string
# Returns a new FEN string with an 'e' instead for each empty square,
# strips separators ('/'), strips end of string
def processFEN(someFEN):
    newStr = ''
    for char in someFEN:
        if char == ' ':# end of relevant part of FEN
            return newStr
        elif char == '/':
            pass
        elif str.isdigit(char) == False:
            newStr += char
        else:
            for x in range(int(char)):
                newStr += 'e'

# Takes a FEN string processed by processFEN()
# Returns a dictionary of strings to chars(single length strings)
#       ie boardmap = {'e2':'p','e3':'e', etc...}
def processedFENtoBoardmap(processedFEN):
    boardmap = {}
    for num in range(1,9):
        for letter in ['a','b','c','d','e','f','g','h']:
            square = letter+str(num)
            boardmap[square] = processedFEN[0]
            processedFEN = processedFEN[1:]
    return boardmap





def main():
    assert(processFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') == 'rnbqkbnrppppppppeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeePPPPPPPPRNBQKBNR')
    assert(len(processFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')) == 64)
    assert(processedFENtoBoardmap(processFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')) == {'h8': 'R', 'f1': 'b', 'f2': 'p', 'f3': 'e', 'f4': 'e', 'f5': 'e', 'f6': 'e', 'f7': 'P', 'h2': 'p', 'h3': 'e', 'h1': 'r', 'h6': 'e', 'h7': 'P', 'h4': 'e', 'h5': 'e', 'b4': 'e', 'b5': 'e', 'b6': 'e', 'b7': 'P', 'b1': 'n', 'b2': 'p', 'b3': 'e', 'd6': 'e', 'd7': 'P', 'd4': 'e', 'd5': 'e', 'd2': 'p', 'd3': 'e', 'd1': 'q', 'c7': 'P', 'e5': 'e', 'b8': 'N', 'f8': 'B', 'c5': 'e', 'd8': 'Q', 'c4': 'e', 'g7': 'P', 'g6': 'e', 'g5': 'e', 'g4': 'e', 'g3': 'e', 'g2': 'p', 'g1': 'n', 'e4': 'e', 'g8': 'N', 'a1': 'r', 'a3': 'e', 'a2': 'p', 'a5': 'e', 'a4': 'e', 'a7': 'P', 'a6': 'e', 'c3': 'e', 'c2': 'p', 'c1': 'b', 'e6': 'e', 'e1': 'k', 'c6': 'e', 'e3': 'e', 'e2': 'p', 'e7': 'P', 'a8': 'R', 'c8': 'B', 'e8': 'K'})
    
    
if __name__ == '__main__':
    main()