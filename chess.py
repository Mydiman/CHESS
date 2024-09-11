"""CHESS"""



from copy import deepcopy
from typing import *



def clear_screen() -> None:
    try:
        from os import system
        from platform import system as platform_system
        if platform_system() == 'Windows':
            system('cls')
        else:
            system('clear')
    except ImportError:
        print('\n' * 20)



class Colour:
    Reset: str = '\033[0m\033[K'
    Red: str = '\033[31m'
    Green: str = '\033[32m'
    Yellow: str = '\033[33m'
    OnWhite: str = '\033[30;47m'
    Underline: str = '\033[4m'



class BoardCell:
    def __init__(self: Self, player: str, piece: str) -> None:
        self.player: str = player
        self.piece: str = piece
    
    def change_cell(self: Self, player: str, piece:str) -> None:
        self.player, self.piece = player, piece
    
    def print_cell(self: Self) -> None:
        piece_list: List[List[str]] = [['pawn', u'\u2659', u'\u265F'],
                                       ['knight', u'\u2658', u'\u265E'],
                                       ['bishop', u'\u2657', u'\u265D'],
                                       ['rook', u'\u2656', u'\u265C'],
                                       ['queen', u'\u2655', u'\u265B'],
                                       ['king', u'\u2654', u'\u265A']
                                       ]
        if self.player == 'white':
            for i in range(6):
                if self.piece == piece_list [i][0]:
                    print(' ' + piece_list [i][1], end = '  |')
        elif self.player == 'black':
            for i in range(6):
                if self.piece == piece_list [i][0]:
                    print(' ' + piece_list [i][2], end = '  |')
        else:
            print('    ', end = '|')



class Game:
    def __init__(self: Self, board: list) -> None:
        self.board: List[List[BoardCell]] = [[BoardCell(board [i][j][0], board [i][j][1]) for j in range(8)] for i in range(8)]
        
        self.player: str = 'black'
        self.oppo_player: str = 'white'
        
        self.white_king_corr: List[int] = []
        self.black_king_corr: List[int] = []
        self.update_king_corr()
        
        self.white_captured_piece: List[str] = []
        self.white_remaining_piece: List[str] = []
        self.update_remaining_captured_piece()
        
        self.enpassant: List[List[int]] = [8, 8]
        self.castling_already: List[bool] = [False, False, False, False]  # Wq, Wk, Bq, Bk
        self.castling_available: List[bool] = [False, False, False, False]  # Wq, Wk, Bq, Bk
        
        self.white_possible: List[List[BoardCell]] = []
        self.white_possible_corr: List[List[List[int]]] = []
        self.black_possible: List[List[BoardCell]] = []
        self.black_possible_corr: List[List[List[int]]] = []
        self.update_posssible_move()
        
        self.fifty_move: int = 0
        self.offer_draw: bool = False
        
        self.winner: str = 'empty'
        self.ended: bool = False
        self.ended_type: str = ''
    
    
    def switch_player(self: Self) -> None:
        if self.player == 'white':
            self.player: str = 'black'
            self.oppo_player: str = 'white'
        else:
            self.player: str = 'white'
            self.oppo_player: str = 'black'
    
    def change_cell(self: Self, row: int, column: int, player: str, piece: str) -> None:
        self.board [row][column].change_cell(player, piece)
        self.update_posssible_move()
    
    
    # not yet done
    def undercheck(self: Self, checked_player: str, corr: List[int] = None) -> True:
        if corr is None:
            if checked_player == 'white':
                corr = self.white_king_corr
            else:
                corr = self.black_king_corr
        ...

    # not yet done
    def check_draw(self: Self, fifty_move_reset: bool = False) -> None:
        #stalement
        #insufficient material
        #threefold repetition draw
        self.fifty_move_draw(fifty_move_reset)
    
    def fifty_move_draw(self: Self, reset: bool) -> None:
        if reset:
            self.fifty_move: int = 0
        self.fifty_move += 1
        if not self.ended:
            if self.fifty_move == 101:
                self.ended: bool = True
                self.ended_type: str = 'fifty move rule.'
    
    
    def update_enpassant(self: Self, row: int = 8, column: int = 8) -> None:
        self.enpassant: List[List[int]] = [row, column]
    
    def update_castling_already(self: Self) -> None:
        if not self.castling_already [0]:
            if self.board [0][0].piece != 'rook' and self.board [0][0].player != 'white':
                self.castling_already [0] = True
            if self.board [0][4].piece != 'king' and self.board [0][4].player != 'white':
                self.castling_already [0] = True
        
        if not self.castling_already [1]:
            if self.board [0][7].piece != 'rook' and self.board [0][7].player != 'white':
                self.castling_already [1] = True
            if self.board [0][4].piece != 'king' and self.board [0][4].player != 'white':
                self.castling_already [1] = True
        
        if not self.castling_already [2]:
            if self.board [7][0].piece != 'rook' and self.board [7][0].player != 'black':
                self.castling_already [2] = True
            if self.board [7][4].piece != 'king' and self.board [7][4].player != 'black':
                self.castling_already [2] = True
        
        if not self.castling_already [3]:
            if self.board [7][7].piece != 'rook' and self.board [7][7].player != 'black':
                self.castling_already [3] = True
            if self.board [7][4].piece != 'king' and self.board [7][4].player != 'black':
                self.castling_already [3] = True
    
    def update_castling_available(self: Self) -> None:
        if not self.castling_already [0]:
            temp = self.board [0][0:5]
            if no_blocking_include_moving_piece(temp) == 5:
                if self.undercheck('white', [0, 1]) or self.undercheck('white', [0, 2]) or self.undercheck('white', [0, 3]) or self.undercheck('white', [0, 4]):
                    self.castling_available [0] = False
                else:
                    self.castling_available [0] = True
            else:
                self.castling_available [0] = False
        
        if not self.castling_already [1]:
            temp = self.board [0][4:8]
            if no_blocking_include_moving_piece(temp) == 4:
                if self.undercheck('white', [0, 4]) or self.undercheck('white', [0, 5]) or self.undercheck('white', [0, 6]):
                    self.castling_available [1] = False
                else:
                    self.castling_available [1] = True
            else:
                self.castling_available [1] = False
        
        if not self.castling_already [2]:
            temp = self.board [7][0:5]
            if no_blocking_include_moving_piece(temp) == 5:
                if self.undercheck('black', [7, 1]) or self.undercheck('black', [7, 2]) or self.undercheck('black', [7, 3]) or self.undercheck('black', [7, 4]):
                    self.castling_available [2] = False
                else:
                    self.castling_available [2] = True
            else:
                self.castling_available [2] = False
        
        if not self.castling_already [3]:
            temp = self.board [7][4:8]
            if no_blocking_include_moving_piece(temp) == 4:
                if self.undercheck('black', [7, 4]) or self.undercheck('black', [7, 5]) or self.undercheck('black', [7, 6]):
                    self.castling_available [3] = False
                else:
                    self.castling_available [3] = True
            else:
                self.castling_available [3] = False
    
    def update_remaining_captured_piece(self: Self) -> None:
        captured_piece: List[str] = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'bishop', 'bishop', 'knight', 'knight', 'rook', 'rook', 'queen', 'king']
        remaining_piece: List[str] = []
        for i in self.board:
            for j in i:
                if j.player == 'white':
                    if j.piece in captured_piece:
                        captured_piece.remove(j.piece)
                        remaining_piece.append(j.piece)
                    else:
                        remaining_piece.append(j.piece)
        remaining_piece.remove('king')
        self.white_captured_piece: List[str] = captured_piece
        self.white_remaining_piece: List[str] = sorting_piece(remaining_piece)
        
        captured_piece: List[str] = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'bishop', 'bishop', 'knight', 'knight', 'rook', 'rook', 'queen', 'king']
        remaining_piece: List[str] = []
        for i in self.board:
            for j in i:
                if j.player == 'black':
                    if j.piece in captured_piece:
                        captured_piece.remove(j.piece)
                        remaining_piece.append(j.piece)
                    else:
                        remaining_piece.append(j.piece)
        remaining_piece.remove('king')
        self.black_captured_piece: List[str] = captured_piece
        self.black_remaining_piece: List[str] = sorting_piece(remaining_piece)
    
    def update_king_corr(self: Self) -> None:
        for i in range(8):
            for j in range(8):
                if self.board [i][j].piece == 'king':
                    if self.board [i][j].player == 'white':
                        self.white_king_corr: List[int] = [i, j]
                    else:
                        self.black_king_corr: List[int] = [i, j]
    
    
    def update_possible_row(self: Self) -> None:
        for i in range(8):
            for j in range(8):
                if self.board [i][j].piece == 'rook' or self.board [i][j].piece == 'queen':
                    temp = [self.board [i][0:j + 1], self.board [i][j:8]]
                    temp1 = [[[i, k] for k in range(j + 1)], [[i, k] for k in range(j, 8)]]
                    temp [0].reverse()
                    temp1 [0].reverse()
                    
                    for k in range(2):
                        if self.board [i][j].player == 'white':
                            temp1 [k] = temp1 [k][0:no_blocking_include_moving_piece(temp[k])]
                            temp [k] = temp [k][0:no_blocking_include_moving_piece(temp[k])]
                            if len(temp [k]) != 1:
                                if temp [k][-1].player == 'white':
                                    del temp [k][-1]
                                    del temp1 [k][-1]
                            self.white_possible.append(temp [k])
                            self.white_possible_corr.append(temp1 [k])
                        
                        else:
                            temp1 [k] = temp1 [k][0:no_blocking_include_moving_piece(temp[k])]
                            temp [k] = temp [k][0:no_blocking_include_moving_piece(temp[k])]
                            if len(temp [k]) != 1:
                                if temp [k][-1].player == 'black':
                                    del temp [k][-1]
                                    del temp1 [k][-1]
                            self.black_possible.append(temp [k])
                            self.black_possible_corr.append(temp1 [k])
    
    def update_possible_column(self: Self) -> None:
        for i in range(8):
            for j in range(8):
                if self.board [i][j].piece == 'rook' or self.board [i][j].piece == 'queen':
                    temp = [[], []]
                    temp [0] = [self.board [k][j] for k in range(i + 1)]
                    temp [1] = [self.board [k][j] for k in range(i, 8)]
                    temp1 = [[[k, j] for k in range(i + 1)], [[k, j] for k in range(i, 8)]]
                    temp [0].reverse()
                    temp1 [0].reverse()
                    
                    for k in range(2):
                        if self.board [i][j].player == 'white':
                            temp1 [k] = temp1 [k][0:no_blocking_include_moving_piece(temp[k])]
                            temp [k] = temp [k][0:no_blocking_include_moving_piece(temp[k])]
                            if len(temp [k]) != 1:
                                if temp [k][-1].player == 'white':
                                    del temp [k][-1]
                                    del temp1 [k][-1]
                            self.white_possible.append(temp [k])
                            self.white_possible_corr.append(temp1 [k])
                        
                        else:
                            temp1 [k] = temp1 [k][0:no_blocking_include_moving_piece(temp[k])]
                            temp [k] = temp [k][0:no_blocking_include_moving_piece(temp[k])]
                            if len(temp [k]) != 1:
                                if temp [k][-1].player == 'black':
                                    del temp [k][-1]
                                    del temp1 [k][-1]
                            self.black_possible.append(temp [k])
                            self.black_possible_corr.append(temp1 [k])
    
    def update_possible_cross(self: Self) -> None:
        for i in range(8):
            for j in range(8):
                if self.board [i][j].piece == 'bishop' or self.board [i][j].piece == 'queen':
                    temp = [[], [], [], []]
                    temp1 = [[], [], [], []]
                    bishop_move = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
                    for k in range(4):
                        x, y = i, j
                        while 0 <= x <= 7 and 0 <= y <= 7:
                            temp [k].append(self.board [x][y])
                            temp1 [k].append([x, y])
                            x += bishop_move [k][0]
                            y += bishop_move [k][1]
                        
                        if self.board [i][j].player == 'white':
                            temp1 [k] = temp1 [k][0:no_blocking_include_moving_piece(temp[k])]
                            temp [k] = temp [k][0:no_blocking_include_moving_piece(temp[k])]
                            if len(temp [k]) != 1:
                                if temp [k][-1].player == 'white':
                                    del temp [k][-1]
                                    del temp1 [k][-1]
                            self.white_possible.append(temp [k])
                            self.white_possible_corr.append(temp1 [k])
                        
                        else:
                            temp1 [k] = temp1 [k][0:no_blocking_include_moving_piece(temp[k])]
                            temp [k] = temp [k][0:no_blocking_include_moving_piece(temp[k])]
                            if len(temp [k]) != 1:
                                if temp [k][-1].player == 'black':
                                    del temp [k][-1]
                                    del temp1 [k][-1]
                            self.black_possible.append(temp [k])
                            self.black_possible_corr.append(temp1 [k])
    
    def update_possible_knight(self: Self) -> None:
        knight_move = [[0, 0], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
        for i in range(8):
            for j in range(8):
                if self.board [i][j].piece == 'knight':
                    temp = []
                    temp1 = []
                    for m in knight_move:
                        if 0 <= i + m[0] <= 7 and 0 <= j + m[1] <= 7:
                            if self.board [i][j].player != self.board [i + m[0]][j + m[1]].player or m[0] == m[1] == 0:
                                temp.append(self.board [i + m[0]][j + m[1]])
                                temp1.append([i + m[0], j + m[1]])
                    if self.board [i][j].player == 'white':
                        self.white_possible.append(temp)
                        self.white_possible_corr.append(temp1)
                    else:
                        self.black_possible.append(temp)
                        self.black_possible_corr.append(temp1)
    
    def update_possible_king(self: Self) -> None:
        #not include special move (castling)
        self.update_king_corr()
        king_move = [[0, 0], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        i, j = self.white_king_corr
        temp = []
        temp1 = []
        for k in king_move:
            if 0 <= i + k[0] <= 7 and 0 <= j + k[1] <= 7:
                if self.board [i + k[0]][j + k[1]].player != 'white' or k[0] == k[1] == 0:
                    temp.append(self.board [i + k[0]][j + k[1]])
                    temp1.append([i + k[0], j + k[1]])
        self.white_possible.append(temp)
        self.white_possible_corr.append(temp1)
        
        i, j = self.black_king_corr
        temp = []
        temp1 = []
        for k in king_move:
            if 0 <= i + k[0] <= 7 and 0 <= j + k[1] <= 7:
                if self.board [i + k[0]][j + k[1]].player != 'black' or k[0] == k[1] == 0:
                    temp.append(self.board [i + k[0]][j + k[1]])
                    temp1.append([i + k[0], j + k[1]])
        self.black_possible.append(temp)
        self.black_possible_corr.append(temp1)
    
    def update_possible_pawn(self: Self) -> None:
        #not include special move (Enpass & promotion)
        for i in range(8):
            for j in range(8):
                if self.board [i][j].piece == 'pawn':
                    temp = []
                    temp1 = []
                    if self.board [i][j].player == 'white':
                        temp.append(self.board [i][j])
                        temp1.append([i, j])
                        for k in [-1, 1]:
                            if 0 <= i + 1 <= 6 and 0 <= j + k <= 7:
                                if self.board [i + 1][j + k].player == 'black':
                                    temp.append(self.board [i + 1][j + k])
                                    temp1.append([i + 1, j + k])
                        if 0 <= i + 1 <= 6:
                            if self.board [i + 1][j].player == 'empty':
                                temp.append(self.board [i + 1][j])
                                temp1.append([i + 1, j])
                        if i == 1:
                            if self.board [i + 1][j].player == self.board [i + 2][j].player == 'empty':
                                temp.append(self.board [i + 2][j])
                                temp1.append([i + 2, j])
                        self.white_possible.append(temp)
                        self.white_possible_corr.append(temp1)
                    
                    else:
                        temp.append(self.board [i][j])
                        temp1.append([i, j])
                        for k in [-1, 1]:
                            if 1 <= i - 1 <= 7 and 0 <= j + k <= 7:
                                if self.board [i - 1][j + k].player == 'white':
                                    temp.append(self.board [i - 1][j + k])
                                    temp1.append([i - 1, j + k])
                        if 1 <= i - 1 <= 7:
                            if self.board [i - 1][j].player == 'empty':
                                temp.append(self.board [i - 1][j])
                                temp1.append([i - 1, j])
                        if i == 6:
                            if self.board [i - 1][j].player == self.board [i - 2][j].player == 'empty':
                                temp.append(self.board [i - 2][j])
                                temp1.append([i - 2, j])
                        self.black_possible.append(temp)
                        self.black_possible_corr.append(temp1)
    
    def update_possible_enpassant(self: Self):
        if self.enpassant != [8, 8]:
            ...
    
    def update_possible_castling(self: Self):
        ...
    
    def update_possible_promotion(self: Self):
        ...
    
    def update_posssible_move(self: Self) -> None:
        self.white_possible: List[List[BoardCell]] = []
        self.white_possible_corr: List[List[List[int]]] = []
        self.black_possible: List[List[BoardCell]] = []
        self.black_possible_corr: List[List[List[int]]] = []
        self.update_king_corr()
        self.update_possible_row()
        self.update_possible_column()
        self.update_possible_cross()
        self.update_possible_knight()
        self.update_possible_king()
        self.update_possible_pawn()
        #sepcial move will not be contain in self.possible_move
    
    
    def display_board(self: Self) -> None:
        clear_screen()
        
        half_to_full = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
        half_to_full [0x20] = 0x3000
        #Convert all ASCII characters to the full-width counterpart.
        def fullen(string: str) -> str:
            return str(string).translate(half_to_full)
        
        def print_captured_list(player: str) -> str:
            piece_point: list = [['pawn', 1], ['bishop', 3], ['knight', 3], ['rook', 5], ['queen', 9]]
            white_piece: list = [u'\u2659', u'\u2657', u'\u2658', u'\u2656', u'\u2655']
            black_piece: list = [u'\u265F', u'\u265D', u'\u265E', u'\u265C', u'\u265B']
            total_point: int = 0
            return_string: str = ''
            for i in self.white_captured_piece:
                for j in range(5):
                    if piece_point [j][0] == i:
                        if player == 'white':
                            return_string += white_piece [j] + ' '
            
            for i in self.black_captured_piece:
                for j in range(5):
                    if piece_point [j][0] == i:
                        if player == 'black':
                            return_string += black_piece [j] + ' '
            
            for i in self.white_remaining_piece:
                for j in range(5):
                    if piece_point [j][0] == i:
                        if player == 'white':
                            total_point -= piece_point [j][1]
                        else:
                            total_point += piece_point [j][1]
            
            for i in self.black_remaining_piece:
                for j in range(5):
                    if piece_point [j][0] == i:
                        if player == 'black':
                            total_point -= piece_point [j][1]
                        else:
                            total_point += piece_point [j][1]
            
            if total_point <= 0:
                return_string += '    '
            elif total_point < 10:
                return_string += '+  ' + str(total_point)
            elif total_point < 100:
                return_string += '+ ' + str(total_point)
            else:
                return_string += '+' + str(total_point)
            while len(return_string) < 34:
                return_string += ' '
            return return_string
        
        if self.player == 'white':
            print(Colour.Underline + 'White\'s turn' + Colour.Reset + '\n')
            print('      ' + fullen('a') + '   ' + fullen('b') + '   ' + fullen('c') + '   ' + fullen('d') + '   ' + fullen('e') + '   ' + fullen('f') + '   ' + fullen('g') + '   ' + fullen('h') + f'        {Colour.Underline}Input Examples{Colour.Reset}')
            for i in range(8):
                list_print: list = ['Moving from a1 to a2    ->  a1a2', 'Queenside castling      ->  0-0-0', 'Promote to a rook       ->  a7a8=R', 'Promote to a knight     ->  a7a8=N', 'Offer or accept a draw  ->  draw', '', '', f'{Colour.OnWhite}                                  {Colour.Reset}']  # '' = print nothing
                print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      {list_print [i]}')
                
                print(' ' + fullen(f'{8 - i}') + ' ', end = f'{Colour.OnWhite}|')
                # print cell
                for j in range(8):
                    self.board [7 - i][j].print_cell()
                        
                list_print: list = ['Kingside castling       ->  0-0', 'Promote to a queen      ->  a7a8=Q', 'Promote to a bishop     ->  a7a8=B', 'En passant              ->  a5b6', 'Resign                  ->  resign', '', Colour.OnWhite + print_captured_list('white') + Colour.Reset, f'{Colour.OnWhite}                                  {Colour.Reset}']  # '' = print nothing
                print(f'{Colour.Reset} ' + fullen(f'{8 - i}') + f'   {list_print [i]}')
            
            print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ' + Colour.OnWhite + print_captured_list('black') + Colour.Reset)
            print('      ' + fullen('a') + '   ' + fullen('b') + '   ' + fullen('c') + '   ' + fullen('d') + '   ' + fullen('e') + '   ' + fullen('f') + '   ' + fullen('g') + '   ' + fullen('h') + '        \n')
        
        else:
            print(Colour.Underline + 'Black\'s turn' + Colour.Reset + '\n')
            print('      ' + fullen('h') + '   ' + fullen('g') + '   ' + fullen('f') + '   ' + fullen('e') + '   ' + fullen('d') + '   ' + fullen('c') + '   ' + fullen('b') + '   ' + fullen('a') + f'        {Colour.Underline}Input Examples{Colour.Reset}')
            for i in range(8):
                list_print: list = ['Moving from a1 to a2    ->  a1a2', 'Queenside castling      ->  0-0-0', 'Promote to a rook       ->  a2a1=R', 'Promote to a knight     ->  a2a1=N', 'Offer or accept a draw  ->  draw', '', '', f'{Colour.OnWhite}                                  {Colour.Reset}']  # '' = print nothing
                print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      {list_print[i]}')
                
                print(' ' + fullen(f'{i + 1}') + ' ', end = f'{Colour.OnWhite}|')
                # print cell
                for j in range(8):
                    self.board [i][7 - j].print_cell()
                
                list_print: list = ['Kingside castling       ->  0-0', 'Promote to a queen      ->  a2a1=Q', 'Promote to a bishop     ->  a2a1=B', 'En passant              ->  a4b3', 'Resign                  ->  resign', '', Colour.OnWhite + print_captured_list('black') + Colour.Reset, f'{Colour.OnWhite}                                  {Colour.Reset}']  # '' = print nothing
                print(f'{Colour.Reset} ' + fullen(f'{i + 1}') + f'   {list_print [i]}')
            
            print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ' + Colour.OnWhite + print_captured_list('white') + Colour.Reset)
            print('      ' + fullen('h') + '   ' + fullen('g') + '   ' + fullen('f') + '   ' + fullen('e') + '   ' + fullen('d') + '   ' + fullen('c') + '   ' + fullen('b') + '   ' + fullen('a') + '   ' + '     \n')
    
    def testing_print_board(self: Self) -> None:
        print(Colour.Reset + '\nwhite\n' + Colour.OnWhite)
        for i in self.white_possible:
            for j in i:
                j.print_cell()
            print()
        
        print(Colour.Reset + '\nblack\n' + Colour.OnWhite)
        for i in self.black_possible:
            for j in i:
                j.print_cell()
            print()



def no_blocking_include_moving_piece(array: List[BoardCell]) -> int:
    count = 1
    flag = True
    while count < len(array) and flag:
        if array [count].player != 'empty':
            flag = False
        count += 1
    return count



def sorting_piece(array: List[str]) -> List[str]:
    def sorting_key(n) -> Literal [1, 2, 3, 4, 5, 6]:
        match n:
            case 'pawn':
                return 1
            case 'bishop':
                return 2
            case 'knight':
                return 3
            case 'rook':
                return 4
            case 'queen':
                return 5
            case 'king':
                return 6
    array.sort(key = sorting_key)
    return array



def deepcopy_board(main_game: Game) -> Game:
    copy_game = deepcopy(main_game)
    return copy_game



def compare_game(main_game: Game, compared_game: Game) -> bool:
    if main_game.board != compared_game.board:
        return False
    if main_game.player != compared_game.player:
        return False
    if main_game.enpassant != compared_game.enpassant:
        return False
    if main_game.castling_already != compared_game.castling_already:
        return False
    if main_game.castling_available != compared_game.castling_available:
        return False



def moving_input_vaild(board, player, str_input: str) -> List[int]:
    if str_input == "0-0":
        if player == "white":
            return [4, 7]
        return [60, 63]
    
    if len(str_input) == 4:
        if str_input [0].isalpha() and str_input [1].isdecimal() and str_input [2].isalpha() and str_input [3].isdecimal():
            column, row = ord(str_input [0]) - 65, int(str_input [1]) - 1
            column1, row1 = ord(str_input [2]) - 65, int(str_input [3]) - 1
            if 0 <= row < 8 and 0 <= column < 8 and 0 <= row1 < 8 and 0 <= column1 < 8:
                if board [row][column].player == player and (not board [row1][column1].player == player):
                    return [row * 8 + column, row1 * 8 + column1]
    
    if str_input == "0-0-0":
        if player == "white":
            return [4, 0]
        return [60, 56]
    
    if len(str_input) == 6 and str_input [0].isalpha() and str_input [1].isdecimal() and str_input [2].isalpha() and str_input [3].isdecimal():
        if str_input [4] == "=" and (str_input [5] == "Q" or str_input [5] == "R" or str_input [5] == "B" or str_input [5] == "N"):
            column, row = ord(str_input [0]) - 65, int(str_input [1]) - 1
            column1, row1 = ord(str_input [2]) - 65, int(str_input [3]) - 1
            if 0 <= row < 8 and 0 <= column < 8 and 0 <= row1 < 8 and 0 <= column1 < 8:
                if board [row][column].player == player and (not board [row1][column1].player == player):
                    return [row * 8 + column, row1 * 8 + column1]
        
    if str_input == "RESIGN":
        return [64, 64]
    
    if str_input == "DRAW":
        return [65, 65]
    
    return [-1, -1]



def moving_vaild(game: Game, selete_place, moving_place, moving_input: str = '') -> bool:
    row_selete, column_selete = selete_place // 8, selete_place % 8
    row_moving, column_moving = moving_place // 8, moving_place % 8
    if moving_input == '0-0' or moving_input == '0-0-0':
        ...
    elif len(moving_input) == 6:
        ...
    else:
        ...
        #remember to add en passant in else




def init_setup() -> list:
    board = [['' for i in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            if i == 0:
                board [i][j] = ['white', ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'] [j]]
            elif i == 1:
                board [i][j] = ['white', 'pawn']
            elif i == 7:
                board [i][j] = ['black', ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'] [j]]
            elif i == 6:
                board [i][j] = ['black', 'pawn']
            else:
                board [i][j] = ['empty', 'empty']
    return board



def test() -> list:
    board = [['' for i in range(8)] for i in range(8)]
    testing_board = [
        'RNBQKBNR',
        'PPPPPPPP',
        '        ',
        '        ',
        '        ',
        '        ',
        'pppppppp',
        'rnbqkbnr'
        ]  #for testing
    for i in range(8):
        for j in range(8):
            match testing_board [i][j]:
                case 'K':
                    board [i][j] = ['white', 'king']
                case 'Q':
                    board [i][j] = ['white', 'queen']
                case 'R':
                    board [i][j] = ['white', 'rook']
                case 'N':
                    board [i][j] = ['white', 'knight']
                case 'B':
                    board [i][j] = ['white', 'bishop']
                case 'P':
                    board [i][j] = ['white', 'pawn']
                case 'k':
                    board [i][j] = ['black', 'king']
                case 'q':
                    board [i][j] = ['black', 'queen']
                case 'r':
                    board [i][j] = ['black', 'rook']
                case 'n':
                    board [i][j] = ['black', 'knight']
                case 'b':
                    board [i][j] = ['black', 'bishop']
                case 'p':
                    board [i][j] = ['black', 'pawn']
                case ' ':
                    board [i][j] = ['empty', 'empty']
    return board



def main() -> None:
    main_game: Game = Game(test())
    while not main_game.ended:
        main_game.switch_player()
        while True:
            clear_screen()
            main_game.display_board()
            main_game.testing_print_board()
            if main_game.offer_draw:
                print("Your opponent is offering a draw")
                move_input = input("Input \"draw\" for accepting: ")
            else:
                move_input = input('Input the move: ')
            move_input = move_input.replace(' ', '')
            move_input = move_input.upper()
            selete_place, moving_place = moving_input_vaild(main_game.board, main_game.player, move_input)
            
            if main_game.offer_draw:
                if selete_place == moving_place == 65:
                    main_game.ended_type = "agreement"
                    main_game.ended = True
                main_game.offer_draw = False
                break
            
            if selete_place == moving_place == 64:
                main_game.winner = main_game.oppo_player
                main_game.ended_type = "resignation"
                main_game.ended = True
                break
            
            elif selete_place == moving_place == 65:
                main_game.offer_draw = True
                break
            
            elif selete_place == moving_place == -1:
                input(Colour.Red + "INPUT INCORRECT" + Colour.Reset + "\n" + Colour.Yellow + "ENTER TO RETRY" + Colour.Reset)
            
            else:
                ...
    
    clear_screen()
    main_game.display_board()
    if main_game.winner == "empty":
        input(f"Draw by {main_game.ended_type}\nEnter for next game")
    else:
        input(f"{main_game.winner.upper()} win by {main_game.ended_type}\nEnter for next game")



while True:
    clear_screen()
    main()