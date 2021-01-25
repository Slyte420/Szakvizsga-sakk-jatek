import chess
import pygame
import sys
from pygame.event import event_name
from pygame.math import Vector2
from pygame.time import Clock
from pathlib import Path


class PIECES:
    def __init__(self):
        pass


class BOARD:
    def __init__(self):
        self.Board = chess.Board()
        self.square_dark = pygame.image.load(
            'Assets/square_brown_dark.png').convert_alpha()
        self.square_light = pygame.image.load(
            'Assets/square_brown_light.png').convert_alpha()
        self.legal_move_image = pygame.image.load(
            'Assets/dot.png').convert_alpha()
        self.capture_move_image = pygame.image.load(
            'Assets/capture_ring.png').convert_alpha()
        self.check_image = pygame.image.load(
            'Assets/check_ring.png').convert_alpha()
        self.chessTablePos = str(self.Board)
        self.chessTablePos = self.chessTablePos.replace(" ", "")
        self.chessTablePos = self.chessTablePos.split("\n")
        # print(self.chessTablePos)
        self.Pieces = {
            'b': 'bishop',
            'r': 'rook',
            'n': 'knight',
            'p': 'pawn',
            'q': 'queen',
            'r': 'rook',
            'k': 'king'
        }
        self.move_history_san_white = []
        self.move_history_san_black = []
        self.set = 0
        self.setaddonce = False

    def print_TablePos(self):
        print(self.chessTablePos)

    def get_pos_fromsquare(self, sq):
        # b1
        lets = 'abcdefgh'
        x = lets.index(sq[0])
        y = int(sq[1]) - 1
        return x, y

    def get_square_frompos(self, x, y):
        lets = 'abcdefgh'
        sq = lets[x] + str(y + 1)
        return sq

    def ispieceatpos(self, x, y):
        square = self.get_square_frompos(x, y)
        if (self.Board.piece_at(chess.parse_square(square))):
            return True
        else:
            return False

    def iscolorandpieceatpos(self, x, y):
        square = self.get_square_frompos(x, y)
        if self.Board.piece_at(chess.parse_square(square)) and self.Board.turn == self.Board.color_at(
                chess.parse_square(square)):
            return True
        else:
            return False

    def pieceatpos(self, x, y):
        square = self.get_square_frompos(x, y)
        return self.Board.piece_type_at(chess.parse_square(square))

    def draw_board(self):
        for row in range(square_number):
            if row % 2 == 0:
                for col in range(square_number):
                    if col % 2 == 0:
                        board_rect = pygame.Rect(
                            col * square_size, row * square_size, square_size, square_size)
                        screen.blit(self.square_light, board_rect)
                    else:
                        board_rect = pygame.Rect(
                            col * square_size, row * square_size, square_size, square_size)
                        screen.blit(self.square_dark, board_rect)
            else:
                for col in range(square_number):
                    if col % 2 == 0:
                        board_rect = pygame.Rect(
                            col * square_size, row * square_size, square_size, square_size)
                        screen.blit(self.square_dark, board_rect)
                    else:
                        board_rect = pygame.Rect(
                            col * square_size, row * square_size, square_size, square_size)
                        screen.blit(self.square_light, board_rect)

    def draw_pieces(self):
        path_default = 'Assets/'
        self.update_table()
        for row in range(square_number):
            for col in range(square_number):
                piece = self.chessTablePos[row][col]
                if piece != '.':
                    if piece.isupper():
                        colorPiece = True
                    else:
                        colorPiece = False
                    piece = piece.lower()
                    piece_rect = pygame.Rect(
                        col * square_size, row * square_size, square_size, square_size)
                    if colorPiece:
                        piece_path = path_default + \
                            'w_' + self.Pieces[piece] + '.png'
                    else:
                        piece_path = path_default + \
                            'b_' + self.Pieces[piece] + '.png'
                    # print(path)
                    piece_path = Path(piece_path)

                    piece_image = pygame.image.load(piece_path).convert_alpha()
                    piece_image = pygame.transform.rotozoom(
                        piece_image, 0, 1.5)
                    screen.blit(
                        piece_image, piece_rect)

    def update_table(self):
        self.chessTablePos = str(self.Board)
        self.chessTablePos = self.chessTablePos.replace(" ", "")
        self.chessTablePos = self.chessTablePos.split("\n")

    def push_move(self, table_x, table_y, table_x2, table_y2):
        squarefrom = self.get_square_frompos(table_x, table_y)
        squareto = self.get_square_frompos(table_x2, table_y2)
        print(squarefrom + squareto)
        legal_move = [move.uci() for move in self.Board.generate_legal_moves()]
        legal_captures = [move.uci()
                          for move in self.Board.generate_legal_captures()]
        legal_enpassant = [move.uci()
                           for move in self.Board.generate_legal_ep()]
        legal_promotion = [move[:-1] for move in legal_captures + legal_move]
        move = squarefrom + squareto
        x, y = self.get_pos_fromsquare(squarefrom)
        print(x, y)
        print(self.pieceatpos(x, y))
        print(legal_promotion)
        if move in legal_move or move in legal_captures or move in legal_enpassant:
            print('Moved')
            if self.Board.turn:
                self.move_history_san_white.append(
                    self.Board.san(self.Board.parse_uci(move)))
            else:
                self.move_history_san_black.append(
                    self.Board.san(self.Board.parse_uci(move)))
            self.Board.push_uci(move)
        elif self.pieceatpos(x, y) == 1 and move in legal_promotion:
            piece = ''
            queen_rect = pygame.Rect(
                square_number * square_size, (square_number - 4) * square_size, square_size, square_size)
            knight_rect = pygame.Rect(
                square_number * square_size, (square_number - 3) * square_size, square_size, square_size)
            rook_rect = pygame.Rect(
                square_number * square_size, (square_number - 2) * square_size, square_size, square_size)
            bishop_rect = pygame.Rect(
                square_number * square_size, (square_number - 1) * square_size, square_size, square_size)
            con = True
            while con:
                if self.Board.turn:
                    path_default = 'Assets/'
                    queen_path = path_default + 'w_' + \
                        self.Pieces['q'] + '.png'
                    knight_path = path_default + \
                        'w_' + self.Pieces['n'] + '.png'
                    rook_path = path_default + 'w_' + self.Pieces['r'] + '.png'
                    bishop_path = path_default + \
                        'w_' + self.Pieces['b'] + '.png'
                    queen_path = Path(queen_path)
                    knight_path = Path(knight_path)
                    rook_path = Path(rook_path)
                    bishop_path = Path(bishop_path)
                    queen_image = pygame.image.load(queen_path).convert_alpha()
                    knight_image = pygame.image.load(
                        knight_path).convert_alpha()
                    rook_image = pygame.image.load(rook_path).convert_alpha()
                    bishop_image = pygame.image.load(
                        bishop_path).convert_alpha()
                    screen.blit(queen_image, queen_rect)
                    screen.blit(knight_image, knight_rect)
                    screen.blit(rook_image, rook_rect)
                    screen.blit(bishop_image, bishop_rect)
                else:
                    path_default = 'Assets/'
                    queen_path = path_default + \
                        'b_' + self.Pieces['q'] + '.png'
                    knight_path = path_default + \
                        'b_' + self.Pieces['n'] + '.png'
                    rook_path = path_default + \
                        'b_' + self.Pieces['r'] + '.png'
                    bishop_path = path_default + \
                        'b_' + self.Pieces['b'] + '.png'
                    queen_path = Path(queen_path)
                    knight_path = Path(knight_path)
                    rook_path = Path(rook_path)
                    bishop_path = Path(bishop_path)
                    queen_image = pygame.image.load(
                        queen_path).convert_alpha()
                    knight_image = pygame.image.load(
                        knight_path).convert_alpha()
                    rook_image = pygame.image.load(rook_path).convert_alpha()
                    bishop_image = pygame.image.load(
                        bishop_path).convert_alpha()
                    screen.blit(queen_image, queen_rect)
                    screen.blit(knight_image, knight_rect)
                    screen.blit(rook_image, rook_rect)
                    screen.blit(bishop_image, bishop_rect)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                        con = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if x >= square_number * square_size and x <= square_number * square_size + square_size:
                            if y >= (square_number - 4) * square_size and y <= ((square_number - 3) * square_size):
                                piece = 'q'
                            elif y >= (square_number - 3) * square_size and y <= ((square_number - 2) * square_size):
                                piece = 'n'
                            elif y >= (square_number - 2) * square_size and y <= ((square_number - 1) * square_size):
                                piece = 'r'
                            elif y >= (square_number - 1) * square_size and y <= (square_number * square_size):
                                piece = 'b'
                            con = False

            move = move + piece
            if move in legal_move or move in legal_captures or move in legal_enpassant:
                if self.Board.turn:
                    self.move_history_san_white.append(
                        self.Board.san(self.Board.parse_uci(move)))
                else:
                    self.move_history_san_black.append(
                        self.Board.san(self.Board.parse_uci(move)))
                self.Board.push_uci(move)
                print('Moved')
        else:
            print('Illegal')
        print('White' + str(self.move_history_san_white))
        print('Black' + str(self.move_history_san_black))

    def draw_legalmoves_piece(self, x, y, table_x, table_y):
        legal_moves = [move.uci()
                       for move in self.Board.generate_legal_moves()]
        squarepiece = self.get_square_frompos(table_x, table_y)
        for lmove in legal_moves:
            if squarepiece in lmove:
                x_l, y_l = self.get_pos_fromsquare(lmove[2:])
                y_le = 7 - y_l
                # print(x_l, y_l, y_le)
                legal_rect = pygame.Rect(
                    x_l * square_size, y_le * square_size, square_size, square_size)
                if not self.pieceatpos(x_l, y_l):
                    screen.blit(self.legal_move_image, legal_rect)
                else:
                    screen.blit(self.capture_move_image, legal_rect)
                # print(self.get_pos_fromsquare(lmove[2:]))

    def draw_check(self):
        if self.Board.is_check():
            if self.Board.turn:
                for col in range(square_number):
                    for row in range(square_number):
                        if self.chessTablePos[row][col] == 'K':
                            check_rect = pygame.Rect(
                                col * square_size, row * square_size, square_size, square_size)
                            screen.blit(self.check_image, check_rect)

            else:
                for col in range(square_number):
                    for row in range(square_number):
                        if self.chessTablePos[row][col] == 'k':
                            check_rect = pygame.Rect(
                                col * square_size, row * square_size, square_size, square_size)
                            screen.blit(self.check_image, check_rect)

    def draw_history(self):
        white_move_number = len(self.move_history_san_white)
        black_move_number = len(self.move_history_san_black)
        move_number = white_move_number
        if move_number % 5 == 0 and move_number != 0 and not self.setaddonce:
            self.set = self.set + 5
            self.setaddonce = True
        elif move_number % 5 != 0:
            self.setaddonce = False
        print(move_number, self.set)
        if self.set == move_number and self.set:
            self.set = self.set-1
        for move in range(self.set, move_number):
            move_rect1 = pygame.Rect(
                square_number * square_size, ((move-self.set)*0.39+1) * square_size, square_size/2 + 2 * square_size, square_size*0.4)
            turn_text = str(move+1) + ' '
            turn_text = turn_text + self.move_history_san_white[move] + ' '
            if move <= black_move_number-1:
                turn_text = turn_text + self.move_history_san_black[move]
            turn_rect = game_font.render(
                turn_text, True, pygame.Color('Black'))
            #pygame.draw.rect(screen, pygame.Color('Green'), move_rect1)
            #pygame.draw.rect(screen, pygame.Color('Blue'), move_rect2)
            #pygame.draw.rect(screen, pygame.Color('Red'), move_rect3)
            screen.blit(turn_rect, move_rect1)


class MAIN:
    def __init__(self):
        self.board = BOARD()
        self.selected = False
        self.x = 0
        self.y = 0
        self.game_loop()

    def game_loop(self):
        while not self.board.Board.is_game_over():
            screen.fill((94, 93, 96))
            self.board.draw_board()
            self.board.draw_pieces()
            self.board.draw_history()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    self.selected = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.selected:
                        self.x, self.y = pygame.mouse.get_pos()
                        self.x_table = int(self.x / square_size)
                        self.y_table = 7 - int(self.y / square_size)
                        self.x = int(self.x / square_size)
                        self.y = int(self.y / square_size)
                    if self.x_table >= 0 and self.x_table < square_number and self.y_table >= 0 and self.y_table < square_number:
                        if self.board.iscolorandpieceatpos(self.x_table, self.y_table) and not self.selected:
                            self.selected = True
                        elif self.selected:
                            x2, y2 = pygame.mouse.get_pos()
                            x2_table = int(x2 / square_size)
                            y2_table = 7 - int(y2 / square_size)
                            self.board.push_move(
                                self.x_table, self.y_table, x2_table, y2_table)
                            self.selected = False

            if self.selected:
                self.board.draw_legalmoves_piece(
                    self.x, self.y, self.x_table, self.y_table)
            self.board.draw_history()
            self.board.draw_check()
            pygame.display.update()
            clock.tick(60)
            # print(self.x, self.y, x2, y2)
            # print(self.x_table, self.y_table,
            #     x2_table, y2_table)
            # print(self.board.pieceatpos(
            #    self.x_table, self.y_table))
            # print(self.board.print_TablePos())
            # print('------')
            # print(self.selected)
            # print(self.selected)
            # print(x_table, y_table)
            # print(self.x, self.y)
            # print(self.board.get_square_frompos(
            #    x_table, y_table))
            # print(self.board.print_TablePos())
            # print(self.board.Board.is_check())
            # print(self.board.pieceatpos(0, 0))
            # print(self.board.chessTablePos[0][2])
            # print(self.board.get_square_frompos(4, 6))
            # Draw the pieces
            # Update the screen


pygame.init()
square_size = 128
square_number = 8
game_font = pygame.font.Font('Assets/gamefont.ttf', 55)
screen = pygame.display.set_mode(
    (square_size * (square_number + 3), square_size * square_number))
clock = pygame.time.Clock()

main_game = MAIN()
