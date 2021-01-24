import chess

# board = chess.Board("rnbqkbnr/pppppppp/8/5N2/8/5N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1")
# board.push_uci('e2e4')
# print(board)
# board.push_san('f7f5')
# print(board)
# legal_move = [move.uci() for move in board.generate_legal_moves()]
# legal_captures = [move.uci()
#                  for move in board.generate_legal_captures()]
# move = 'a2'
# for lmove in legal_moves:
#    if move in lmove:
#        print(lmove[2:])
#
# attack_moves = []
#
# Move = 'e4f5'
# print('----------')
# print(legal_moves)
# print(Move in attack_moves)
# board.push_uci(Move)
# print(board.piece_at())
# print(board.piece_at(chess.E1))
# print(board.piece_at(chess.E8))
# print(board)
# promotion_moves = [moves[:-1] for moves in legal_move+legal_captures]
# print(promotion_moves)
# move = 'e7e8'
# print(move in (moves[:-1] for moves in legal_move))
# print(board.peek)
# sq = 'f5d4'
# print(board.san(board.parse_uci(sq)))
move_history_san_white = ['e4', 'e5', 'Qh5#']
move_history_san_black = ['f5', 'g5']
white_move_number = len(move_history_san_white)
black_move_number = len(move_history_san_black)
if white_move_number > black_move_number:
    move_number = white_move_number
else:
    move_number = black_move_number
for turn in range(move_number):
    turn_text = str(turn+1) + ' '
    # print(turn_text)
    turn_text = turn_text + move_history_san_white[turn] + ' '
    if turn <= black_move_number-1:
        turn_text = turn_text + move_history_san_black[turn]
    print(turn_text)
