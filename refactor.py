# lowest level, board rep or primitive functions?
# should make functions that take board "types"
# completely primitive functions are:




# FEN
# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
# 1) piece placement
# 2) w or b to move
# 3) castle availability ( - if none), K is white kingside castle etc...
# 4) en passant square, after e2-e4 this field would contain e3
# 5) half-move clock, number of moves since the last capture or pawn advance
# 6) full move number, advanced after black's move
# 7) whitespace delimited (one space), no leading or trailing space(s)
# after e4:
# rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1




# Make FEN to my Board class repr
#