'''CHESS'''


if __name__ == '__main__':
    try:
        input("\033[31mPlease run { __main__.py } in the root directory of this project\033[K")
    finally:
        quit()



try:
    from copy import deepcopy
    from typing import *
    from random import choice
    from time import sleep
except:
    try:
        input('Import error')
    finally:
        quit()



def clear_screen(menu_or_player_turns: str | None = None) -> None:
    try:
        from os import system
        from platform import system as platform_system
        if platform_system() == 'Windows':
            system('cls')
        else:
            system('clear')
    except:
        print('\n' * 20)
    finally:
        if menu_or_player_turns is None:
            return
        print(Colour.Underline + f'{menu_or_player_turns}' + Colour.Reset)
        print('')



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
    
    def change_cell(self: Self, player: str, piece: str) -> None:
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
    def __init__(self: Self, board: List[List[str]]) -> None:
        self.board: List[List[BoardCell]] = [[BoardCell(board [i][j][0], board [i][j][1]) for j in range(8)] for i in range(8)]
        
        self.player: str = 'black'
        self.oppo_player: str = 'white'
        
        self.enpass: int = 64
        
        ...
        #init by position of king and rooks
        self.castling: List[bool] = [False, False] #True = not ok
        self.castling_rook: List[bool] = [False, False, False, False] #WQ, WK, BQ, BK
        
        #Above involve repetition
        self.repet: list = [[deepcopy(board), 'black', 'white', 64, [False, False], [False, False, False, False]]]
        
        self.player_possible: List[List[int]] = []
        self.oppo_player_possible: List[List[int]] = []
        
        self.fifty_move: int = 0 #101 -> draw
        self.offer_draw: bool = False
        
        self.winner: str = 'empty'
        self.ended: bool = False
        self.ended_type: str = ''
    
    
    def return_board_str(self: Self) -> List[List[List[str]]]:
        temp = [[[] for i in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                temp [i][j] = [self.board [i][j].player, self.board [i][j].piece]
        return temp
    
    
    def switch_player(self: Self) -> None:
        if self.player == 'white':
            self.player: str = 'black'
            self.oppo_player: str = 'white'
        else:
            self.player: str = 'white'
            self.oppo_player: str = 'black'
    
    def enpass_update(self: Self, value: int = 64) -> None:
        self.enpass = value
    
    def castling_update(self: Self, poss: List[int]) -> None:
        if poss [0] == 4:
            self.castling [0] = True
        elif poss [0] == 60:
            self.castling [1] = True
    
    def castling_rook_update(self: Self, poss: List[int]) -> None:
        if poss [0] == 0:
            self.castling_rook [0] = True
        elif poss [0] == 7:
            self.castling_rook [1] = True
        elif poss [0] == 56:
            self.castling_rook [2] = True
        elif poss [0] == 63:
            self.castling_rook [3] = True
    
    
    def move(self: Self, poss: List[int], promote_piece: str = 'Q') -> None:
        #Poss [2]
        #0 -> non-special
        #1 -> castling
        #2 -> enpass (another function)
        #3 -> promote
        #4 -> allow enpass
        piece_row, piece_col = c1d_2d(poss [0])
        place_row, place_col = c1d_2d(poss [1])
        player = self.board [piece_row][piece_col].player
        
        #50 move draw reset
        # += 1 at the lowest of move()
        if self.board [place_row][place_col].player != player and self.board [place_row][place_col].player != 'empty':
            self.fifty_move = 0
        if self.board [piece_row][piece_col].piece == 'pawn':
            self.fifty_move = 0
        
        #Move
        if poss [2] == 0:
            self.board [place_row][place_col].change_cell(player, self.board [piece_row][piece_col].piece)
            self.board [piece_row][piece_col].change_cell('empty', 'empty')
            self.enpass_update()
            self.castling_update(poss)
            self.castling_rook_update(poss)
        
        elif poss [2] == 1:
            if poss == [4, 0, 1]:
                self.board [0][4].change_cell('empty', 'empty')
                self.board [0][3].change_cell('white', 'rook')
                self.board [0][2].change_cell('white', 'king')
                self.board [0][0].change_cell('empty', 'empty')
            elif poss == [4, 7, 1]:
                self.board [0][4].change_cell('empty', 'empty')
                self.board [0][5].change_cell('white', 'rook')
                self.board [0][6].change_cell('white', 'king')
                self.board [0][7].change_cell('empty', 'empty')
            elif poss == [60, 56, 1]:
                self.board [7][4].change_cell('empty', 'empty')
                self.board [7][3].change_cell('black', 'rook')
                self.board [7][2].change_cell('black', 'king')
                self.board [7][0].change_cell('empty', 'empty')
            elif poss == [60, 63, 1]:
                self.board [7][4].change_cell('empty', 'empty')
                self.board [7][5].change_cell('black', 'rook')
                self.board [7][6].change_cell('black', 'king')
                self.board [7][7].change_cell('empty', 'empty')
            self.enpass_update()
            self.castling_update(poss)
            self.castling_rook_update(poss)
        
        elif poss[2] == 2:
            self.board [place_row][place_col].change_cell(player, self.board [piece_row][piece_col].piece)
            self.board [piece_row][piece_col].change_cell('empty', 'empty')
            self.board [c1d_2d(self.enpass) [0]][place_col].change_cell('empty', 'empty')
            self.enpass_update()
        
        elif poss [2] == 3:
            promote_piece == promote_piece.upper()
            if promote_piece == 'Q':
                self.board [place_row][place_col].change_cell(player, 'queen')
            elif promote_piece == 'R':
                self.board [place_row][place_col].change_cell(player, 'rook')
            elif promote_piece == 'B':
                self.board [place_row][place_col].change_cell(player, 'bishop')
            elif promote_piece == 'N':
                self.board [place_row][place_col].change_cell(player, 'knight')
            self.board [piece_row][piece_col].change_cell('empty', 'empty')
            self.enpass_update()
        
        elif poss [2] == 4:
            self.board [place_row][place_col].change_cell(player, self.board [piece_row][piece_col].piece)
            self.board [piece_row][piece_col].change_cell('empty', 'empty')
            self.enpass_update(poss [1])
        self.fifty_move += 1
    
    def check_valid_input(self: Self, selete_piece: int, moving_place: int, move_input: str) -> List[bool]:
        promote_miss = False
        flag_valid = False
        for i in self.player_possible:
            if [selete_piece, moving_place] == i [:-1]:
                if not self.check_checked_after_move(i):
                    if i [-1] == 3:
                        if len(move_input) == 6:
                            self.move([selete_piece, moving_place, i [-1]], move_input [-1])
                            flag_valid = True
                        else:
                            promote_miss = True
                    else:
                        self.move([selete_piece, moving_place, i [-1]])
                        flag_valid = True
                break
        return flag_valid, promote_miss
    
    
    def possible_update(self: Self) -> None:
        #Input type
        #0 -> non-special
        #1 -> castling
        #2 -> enpass (another function)
        #3 -> promote
        #4 -> allow enpass
        def player_possible_update(player: str) -> List[List[int]]:
            def list_piece_row(piece: List[int], place: List[int]) -> List[BoardCell]:
                if piece [1] < place [1]:
                    a, b = piece [1], place [1]
                else:
                    b, a = piece [1], place [1]
                return self.board [piece [0]][a:b+1]
            
            def list_piece_col(piece: List[int], place: List[int]) -> List[BoardCell]:
                if piece [0] < place [0]:
                    a, b = piece [0], place [0]
                else:
                    b, a = piece [0], place [0]
                temp = []
                for i in range(a, b + 1):
                    temp.append(self.board [i][piece [1]])
                return temp
            
            def list_piece_cross(piece: List[int], place: List[int]) -> List[BoardCell]:
                bishop = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
                for i in bishop:
                    temp = []
                    a = piece [0]
                    b = piece [1]
                    while 0 <= a <= 7 and 0 <= b <= 7:
                        temp.append(self.board [a][b])
                        if a == place [0] and b == place [1]:
                            return temp
                        a += i [0]
                        b += i [1]
            
            
            def king_move_valid(piece: List[int], place: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player != player:
                    if abs(piece [0] - place [0]) <= 1 and abs(piece [1] - place [1]) <= 1:
                        return True
                return False
            
            def queen_move_valid(piece: List[int], place: List[int], player: str) -> bool:
                if rook_move_valid(piece, place, player):
                    return True
                if bishop_move_valid(piece, place, player):
                    return True
                return False
            
            def rook_move_valid(piece: List[int], place: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player != player:
                    if check_on_row(piece, place):
                        return check_no_piece_between(list_piece_row(piece, place))
                    if check_on_col(piece, place):
                        return check_no_piece_between(list_piece_col(piece, place))
                return False
            
            def bishop_move_valid(piece: List[int], place: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player != player:
                    if check_on_cross(piece, place):
                        return check_no_piece_between(list_piece_cross(piece, place))
                return False
            
            def knight_move_valid(piece: List[int], place: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player != player:
                    if check_on_sun(piece, place):
                        return True
                return False
            
            def pawn_move_valid(piece: List[int], place: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player == 'empty':
                    if check_on_col(piece, place):
                        if check_no_piece_between(list_piece_col(piece, place)):
                            if player == 'white':
                                if place [0] - piece [0] == 1 and piece [0] != 6:
                                    return True
                            else:
                                if place [0] - piece [0] == -1 and piece [0] != 1:
                                    return True
                
                if player == 'white' and self.board [place [0]][place [1]].player == 'black':
                    if check_on_cross(piece, place):
                        if place [0] - piece [0] == 1 and piece [0] != 6:
                            return True
                elif player == 'black' and self.board [place [0]][place [1]].player == 'white':
                    if check_on_cross(piece, place):
                        if place [0] - piece [0] == -1 and piece [0] != 1:
                            return True
                return False
            
            
            def check_castling(piece: List[int], place: List[int], player: str) -> bool:
                temp = 0
                if player == 'white':
                    if not self.castling [0]:
                        if c2d_1d(piece) == 4 and c2d_1d(place) == 0:
                            for i in range(2, 5):
                                if not self.check_checked(c1d_2d(i), 'white'):
                                    temp += 1
                        elif c2d_1d(piece) == 4 and c2d_1d(place) == 7:
                            for i in range(4, 7):
                                if not self.check_checked(c1d_2d(i), 'white'):
                                    temp += 1
                else:
                    if not self.castling [1]:
                        if c2d_1d(piece) == 60 and c2d_1d(place) == 56:
                            for i in range(58, 61):
                                if not self.check_checked(c1d_2d(i), 'black'):
                                    temp += 1
                        elif c2d_1d(piece) == 60 and c2d_1d(place) == 63:
                            for i in range(60, 63):
                                if not self.check_checked(c1d_2d(i), 'black'):
                                    temp += 1
                if temp == 3:
                    return check_no_piece_between(list_piece_row(piece, place))
                return False
            
            def check_enpass(piece: List[int], place: List[int], player:str) -> bool:
                if self.enpass == 64:
                    return False
                row, col = c1d_2d(self.enpass)
                if player == 'white':
                    if self.board [row][col].player == 'black':
                        if piece [0] == row and abs(place [1] - piece [1]) == 1 and place [0] == row + 1 and place [1] == col:
                            return True
                else:
                    if self.board [row][col].player == 'white':
                        if piece [0] == row and abs(place [1] - piece [1]) == 1 and place [0] == row - 1 and place [1] == col:
                            return True
                return False
            
            def check_promote(piece: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player == 'empty':
                    if player == 'white':
                        if place [0] - piece [0] == 1 and piece [0] == 6:
                            return True
                    elif player == 'black':
                        if place [0] - piece [0] == -1 and piece [0] == 1:
                            return True
                
                if player == 'white' and self.board [place [0]][place [1]].player == 'black':
                    if check_on_cross(piece, place):
                        if place [0] - piece [0] == 1 and piece [0] == 6:
                            return True
                elif player == 'black' and self.board [place [0]][place [1]].player == 'white':
                    if check_on_cross(piece, place):
                        if place [0] - piece [0] == -1 and piece [0] == 1:
                            return True
                return False
            
            def check_allow_enpass(piece: List[int], place: List[int], player: str) -> bool:
                if self.board [place [0]][place [1]].player == 'empty':
                    if player == 'white':
                        if place [0] - piece [0] == 2 and piece [0] == 1:
                            return True
                    else:
                        if place [0] - piece [0] == -2 and piece [0] == 6:
                            return True
                return False
            
            
            poss: List[List[int]] = []
            for i in range(64):
                piece: List[int] = c1d_2d(i)
                if self.board [piece [0]][piece [1]].player == player:
                    for j in range(64):
                        place: List[int] = c1d_2d(j)
                        
                        #Check if it is vaild move
                        match self.board [piece [0]][piece [1]].piece:
                            case 'king':
                                if king_move_valid(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 0])
                                
                                elif check_castling(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 1])
                            
                            case 'queen':
                                if queen_move_valid(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 0])
                            
                            case 'rook':
                                if rook_move_valid(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 0])
                            
                            case 'bishop':
                                if bishop_move_valid(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 0])
                            
                            case 'knight':
                                if knight_move_valid(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 0])
                            
                            case 'pawn':
                                if pawn_move_valid(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 0])
                                
                                elif check_enpass(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 2])
                                
                                elif check_promote(piece, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 3])
                                
                                elif check_allow_enpass(piece, place, player):
                                    poss.append([c2d_1d(piece), c2d_1d(place), 4])
            return poss
        
        self.player_possible: List[List[int]] = player_possible_update(self.player)
        self.oppo_player_possible: List[List[int]] = player_possible_update(self.oppo_player)
    
    
    def find_king(self: Self, player: str) -> List[int]:
        for i in range(8):
            for j in range(8):
                if self.board [i][j].player == player and self.board [i][j].piece == 'king':
                    return [i, j]
    
    def check_checked(self: Self, king_corr: List[int], player: str) -> bool:
        temp = c2d_1d(king_corr)
        if self.player != player:
            for i in self.player_possible:
                if i [1] == temp:
                    return True
        else:
            for i in self.oppo_player_possible:
                if i [1] == temp:
                    return True
        return False
    
    def check_checked_after_move(self: Self, move: List[int]) -> bool:
        #move = [piece, place, type] (1D)
        temp = c1d_2d(move [0])
        player = self.board [temp [0]][temp [1]].player
        copy_game = deepcopy(self)
        copy_game.move(move)
        copy_game.possible_update()
        king_corr = copy_game.find_king(player)
        return copy_game.check_checked(king_corr, player)
    
    
    def check_win_draw(self: Self) -> None:
        
        def check_fifty() -> None:
            #Made change in move
            if self.fifty_move == 101:
                self.ended = True
                self.winner = 'empty'
                self.ended_type = 'fifty-move rule'
        
        def check_repetition() -> None:
            # trun board into List[List[List[player, piece]]]
            self.repet.append([deepcopy(self.return_board_str()), deepcopy(self.player), deepcopy(self.oppo_player), deepcopy(self.enpass), deepcopy(self.castling), deepcopy(self.castling_rook)])
            for i in self.repet:
                if self.repet.count(i) == 3:
                    self.ended = True
                    self.winner = 'empty'
                    self.ended_type = 'repetition'
                    return
        
        def check_insufficient() -> None:
            def remaining_piece(player) -> List[str]:
                temp = []
                for i in self.board:
                    for j in i:
                        if j.player == player:
                            temp.append(j.piece)
                return sorting_piece(temp)
            
            white_remaining = remaining_piece('white')
            black_remaining = remaining_piece('black')
            insufficient_list = [['king'], ['bishop', 'king'], ['knight', 'king']]
            
            if insufficient_list.count(white_remaining) == insufficient_list.count(black_remaining) == 1:
                self.ended = True
                self.winner = 'empty'
                self.ended_type = 'insufficient material'
                return
            
            insufficient_list = [['king'], ['knight', 'knight', 'king']]
            if insufficient_list.count(white_remaining) == insufficient_list.count(black_remaining) == 1:
                if white_remaining != black_remaining:
                    self.ended = True
                    self.winner = 'empty'
                    self.ended_type = 'insufficient material'
                    return
            
            insufficient_list = [['king'], ['bishop', 'bishop', 'king']]
            if insufficient_list.count(white_remaining) == insufficient_list.count(black_remaining) == 1:
                if white_remaining != black_remaining:
                    # dark light
                    temp = ''
                    for i in range(8):
                        for j in range(8):
                            if self.board [i][j].piece == 'bishop':
                                if temp == '':
                                    temp = dark_light(i, j)
                                else:
                                    if temp == dark_light(i, j):
                                        self.ended = True
                                        self.winner = 'empty'
                                        self.ended_type = 'insufficient material'
                                        return
        
        def check_checkmate_stalemate() -> None:
            self.switch_player()
            self.possible_update()
            for i in self.player_possible:
                if not self.check_checked_after_move(i):
                    self.switch_player()
                    return
            temp = self.find_king(self.player)
            self.switch_player()
            self.possible_update()
            if self.check_checked(temp, self.oppo_player):
                self.ended = True
                self.winner = self.player
                self.ended_type = 'checkmate'
                return
            self.ended = True
            self.winner = 'empty'
            self.ended_type = 'stalemate'
        
        
        check_fifty()
        check_repetition()
        check_insufficient()
        check_checkmate_stalemate()
    
    
    def display_board(self: Self, player: str | None = None) -> None:
        if player is None:
            player = self.player
            output_msg = player
        else:
            output_msg = 'white'
            if player == 'white':
                output_msg = 'black'
        #Convert all ASCII characters to the full-width counterpart.
        def fullen(string: str) -> str:
            half_to_full = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
            half_to_full [0x20] = 0x3000
            return string.translate(half_to_full)
        
        def captured_remaining_piece_update(player: str) -> None:
            captured_piece: List[str] = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'bishop', 'bishop', 'knight', 'knight', 'rook', 'rook', 'queen', 'king']
            remaining_piece: List[str] = []
            for i in self.board:
                for j in i:
                    if j.player == player:
                        if j.piece in captured_piece:
                            captured_piece.remove(j.piece)
                            remaining_piece.append(j.piece)
                        else:
                            captured_piece.remove('pawn')
                            remaining_piece.append(j.piece)
            remaining_piece.remove('king')
            return [captured_piece, sorting_piece(remaining_piece)]
        
        def total_point_cal(player: str) -> int:
            total_point = 0
            piece_point = [['pawn', 1], ['bishop', 3], ['knight', 3], ['rook', 5], ['queen', 9]]
            for i in white_remaining_piece:
                for j in range(5):
                    if piece_point [j][0] == i:
                        if player == 'white':
                            total_point -= piece_point [j][1]
                        else:
                            total_point += piece_point [j][1]
            
            for i in black_remaining_piece:
                for j in range(5):
                    if piece_point [j][0] == i:
                        if player == 'black':
                            total_point -= piece_point [j][1]
                        else:
                            total_point += piece_point [j][1]
            return total_point
        
        def print_captured_list(player: str) -> str:
            piece_point = [['pawn', 1], ['bishop', 3], ['knight', 3], ['rook', 5], ['queen', 9]]
            white_piece = [u'\u2659', u'\u2657', u'\u2658', u'\u2656', u'\u2655']
            black_piece = [u'\u265F', u'\u265D', u'\u265E', u'\u265C', u'\u265B']
            return_string: str = ''
            
            if player == 'white':
                for i in white_captured_piece:
                    for j in range(5):
                        if piece_point [j][0] == i:
                                return_string += white_piece [j] + ' '
            else:
                for i in black_captured_piece:
                    for j in range(5):
                        if piece_point [j][0] == i:
                            return_string += black_piece [j] + ' '
            
            total_point = total_point_cal(player)
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
        
        clear_screen(f'{output_msg.capitalize()}\'s turn' + Colour.Reset + '\n')
        white_captured_piece, white_remaining_piece = captured_remaining_piece_update('white')
        black_captured_piece, black_remaining_piece = captured_remaining_piece_update('black')
        
        if player == 'white':
            print('      ' + fullen('a') + '   ' + fullen('b') + '   ' + fullen('c') + '   ' + fullen('d') + '   ' + fullen('e') + '   ' + fullen('f') + '   ' + fullen('g') + '   ' + fullen('h') + f'        {Colour.Underline}Input Examples{Colour.Reset}')
            for i in range(8):
                list_print: List[str] = ['Moving from a1 to a2    ->  a1a2', 'Queenside castling      ->  0-0-0', 'Promote to a rook       ->  a7a8=R', 'Promote to a knight     ->  a7a8=N', 'Offer or accept a draw  ->  draw', 'Save the game           ->  save', '', f'{Colour.OnWhite}                                  {Colour.Reset}']#'' = print nothing
                print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      {list_print [i]}')
                
                print(' ' + fullen(f'{8 - i}') + ' ', end = f'{Colour.OnWhite}|')
                #print cell
                for j in range(8):
                    self.board [7 - i][j].print_cell()
                        
                list_print: List[str] = ['Kingside castling       ->  0-0', 'Promote to a queen      ->  a7a8=Q', 'Promote to a bishop     ->  a7a8=B', 'En passant              ->  a5b6', 'Resign                  ->  resign', 'Quit the game           ->  quit', Colour.OnWhite + print_captured_list('white') + Colour.Reset, f'{Colour.OnWhite}                                  {Colour.Reset}']#'' = print nothing
                print(f'{Colour.Reset} ' + fullen(f'{8 - i}') + f'   {list_print [i]}')
            
            print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ' + Colour.OnWhite + print_captured_list('black') + Colour.Reset)
            print('      ' + fullen('a') + '   ' + fullen('b') + '   ' + fullen('c') + '   ' + fullen('d') + '   ' + fullen('e') + '   ' + fullen('f') + '   ' + fullen('g') + '   ' + fullen('h') + '        \n')
        
        else:
            print('      ' + fullen('h') + '   ' + fullen('g') + '   ' + fullen('f') + '   ' + fullen('e') + '   ' + fullen('d') + '   ' + fullen('c') + '   ' + fullen('b') + '   ' + fullen('a') + f'        {Colour.Underline}Input Examples{Colour.Reset}')
            for i in range(8):
                list_print: List = ['Moving from a1 to a2    ->  a1a2', 'Queenside castling      ->  0-0-0', 'Promote to a rook       ->  a2a1=R', 'Promote to a knight     ->  a2a1=N', 'Offer or accept a draw  ->  draw', 'Save the game           ->  save', '', f'{Colour.OnWhite}                                  {Colour.Reset}']#'' = print nothing
                print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      {list_print[i]}')
                
                print(' ' + fullen(f'{i + 1}') + ' ', end = f'{Colour.OnWhite}|')
                #print cell
                for j in range(8):
                    self.board [i][7 - j].print_cell()
                
                list_print: List = ['Kingside castling       ->  0-0', 'Promote to a queen      ->  a2a1=Q', 'Promote to a bishop     ->  a2a1=B', 'En passant              ->  a4b3', 'Resign                  ->  resign', 'Quit the game           ->  quit', Colour.OnWhite + print_captured_list('black') + Colour.Reset, f'{Colour.OnWhite}                                  {Colour.Reset}']#'' = print nothing
                print(f'{Colour.Reset} ' + fullen(f'{i + 1}') + f'   {list_print [i]}')
            
            print(f'    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ' + Colour.OnWhite + print_captured_list('white') + Colour.Reset)
            print('      ' + fullen('h') + '   ' + fullen('g') + '   ' + fullen('f') + '   ' + fullen('e') + '   ' + fullen('d') + '   ' + fullen('c') + '   ' + fullen('b') + '   ' + fullen('a') + '   ' + '     \n')



class Computer:
    def random_move(list_poss) -> List[int]:
        return choice(list_poss)
    
    def evalution(game: Game, level: int) -> int:
        #2147483647 is limit
        ...
    
    def engine(game: Game, layer: int, orginal_layer:int, level: int) -> int | List[int]:
        #layer is even. e.g. 2 -> 1 -> 0, W -> B -> W, ran three layer
        temp = deepcopy(game)
        copy_game = deepcopy(temp)
        possible_and_point_list = []
        
        for i in copy_game.player_possible:
            str_input = ['A1A1=Q', 'A1A1=R', 'A1A1=B', 'A1A1=N']
            loop_time = 1
            if i [2]:
                loop_time = 4
            
            for j in range(loop_time):
                flag_valid = copy_game.check_valid_input(i [0], i [1], str_input [j]) [0]
                
                if not flag_valid:
                    point = 2147483647#limit
                else:
                    copy_game.check_win_draw()
                    if layer == 0:
                        return -Computer.evalution(copy_game, level)
                    else:
                        copy_game.switch_player()
                        copy_game.possible_update()
                        point = Computer.engine(copy_game, layer - 1, orginal_layer)
                
                possible_and_point_list.append([i [0], i [1], str_input [j], point])
                copy_game = deepcopy(temp)
        
        if layer < orginal_layer:
            lowest = possible_and_point_list [0][3]
            for i in possible_and_point_list [3]:
                if i < lowest:
                    lowest = i
            return -i
        else:
            return possible_and_point_list
    
    
    def level_1(game: Game) -> List[int]:
        return Computer.random_move(game.player_possible)
    
    def level_2(game: Game) -> List[int]:
        ...
        return



def init_setup(testBool: bool = False) -> list:
    ...
    #player can create own board
    board = [['' for i in range(8)] for i in range(8)]
    #upper case = white, lower case = black
    init_board = [
        'RNBQKBNR',
        'PPPPPPPP',
        '        ',
        '        ',
        '        ',
        '        ',
        'pppppppp',
        'rnbqkbnr'
        ]
    if testBool:
        init_board = [
        'RNBQKBNR',
        'PPPPPP  ',
        '        ',
        '        ',
        '        ',
        '        ',
        'pppppppP',
        'rnbqkbn '
        ]#IMPORTANT: The program can't run when there is invalid for example, 2 white king, 8 pawn + 2 queen. I think it is because there will be list out of range when counting remaining piece in Game.display_board().
        #Therefore, keep the board valid. (I haven't limited putting pawn on first row yet, but it won't casue error. I will make the limitation when I allow player to set their own board)
    for i in range(8):
        for j in range(8):
            match init_board [i][j]:
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



def sorting_piece(array: list[str]) -> list[str]:
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

def c1d_2d(c1d: int) -> List[int]:
    return [c1d // 8, c1d % 8]

def c2d_1d(c2d: List[int]) -> int:
    return c2d [0] * 8 + c2d [1]

def dark_light(row: int, col: int) -> Literal ['dark', 'light']:
    #dark or light
    # [0][0] is dark
    if row % 2 == col % 2:
        return 'dark'
    else:
        return 'light'



def check_on_row(piece: List[int], place: List[int]) -> bool:
    if piece [0] == place [0]:
        return True
    return False

def check_on_col(piece: List[int], place: List[int]) -> bool:
    if piece [1] == place [1]:
        return True
    return False

def check_on_cross(piece: List[int], place: List[int]) -> bool:
    if abs(piece [0] - place [0]) == abs(piece [1] - place [1]):
        return True
    return False

def check_on_sun(piece: List[int], place: List[int]) -> bool:
    if abs(piece [0] - place [0]) == 1 and abs(piece [1] - place [1]) == 2:
        return True
    if abs(piece [0] - place [0]) == 2 and abs(piece [1] - place [1]) == 1:
        return True
    return False

def check_no_piece_between(pieces: List[BoardCell]) -> bool:
    #pieces include head and tail
    #X only one piece in list X
    if len(pieces) <= 1:
        return False
    for i in pieces [1:-1]:
        if i.player != 'empty':
            return False
    return True



def save_game(game: Game, file_path: str, ended: bool = False) -> None:
    ...

def load_game(file_path: str) -> Game:
    ...



def loading_icon(text_msg: str, second) -> None:
    list_loading = ['\\', '|', '/', '-']
    for i in range(second, 0, -1):
        for j in list_loading:
            try:
                print(f'\r {j} {text_msg}', end = '')
                sleep(0.25)
            except:
                pass



def input_valid(player, str_input: str) -> List[int]:
    if len(str_input) == 3:
        str_input.replace('O', '0')
        if str_input == '0-0':
            if player == 'white':
                return [4, 7]
            return [60, 63]
    
    if len(str_input) == 4:
        if str_input [0].isalpha() and str_input [1].isdecimal() and str_input [2].isalpha() and str_input [3].isdecimal():
            column, row = ord(str_input [0]) - 65, int(str_input [1]) - 1
            column1, row1 = ord(str_input [2]) - 65, int(str_input [3]) - 1
            if 0 <= row < 8 and 0 <= column < 8 and 0 <= row1 < 8 and 0 <= column1 < 8:
                return [c2d_1d([row, column]), c2d_1d([row1, column1])]
    
    if len(str_input) == 5:
        str_input.replace('O', '0')
        if str_input == '0-0-0':
            if player == 'white':
                return [4, 0]
            return [60, 56]
    
    if len(str_input) == 6:
        if str_input [0].isalpha() and str_input [1].isdecimal() and str_input [2].isalpha() and str_input [3].isdecimal():
            if str_input [4] == '=' and (str_input [5] == 'Q' or str_input [5] == 'R' or str_input [5] == 'B' or str_input [5] == 'N'):
                column, row = ord(str_input [0]) - 65, int(str_input [1]) - 1
                column1, row1 = ord(str_input [2]) - 65, int(str_input [3]) - 1
                if 0 <= row < 8 and 0 <= column < 8 and 0 <= row1 < 8 and 0 <= column1 < 8:
                    return [c2d_1d([row, column]), c2d_1d([row1, column1])]
    
    if str_input == 'RESIGN':
        return [64, 64]
    
    if str_input == 'DRAW':
        return [65, 65]
    
    if str_input == 'SAVE':
        return [66, 66]
    
    if str_input == 'QUIT':
        return [67, 67]
    
    return [-1, -1]



#delete testBool = True
def chess_game(file_path: str, game_mode: int, player: str = 'white') -> None:
    #gamemode 0 -> two player
    #gamemode 1 -> computer (completely random)
    #gamemode 2 -> computer (6 layer random)
    
    
    main_game: Game = Game(init_setup(testBool = True))
    while not main_game.ended:
        main_game.switch_player()
        main_game.possible_update()
        while True:
            #output input for player
            if game_mode == 0 or main_game.player == player:
                try:
                    main_game.display_board()
                    
                    #input
                    if main_game.offer_draw:
                        print('Your opponent is offering a draw')
                        move_input = input('Input \'draw\' to accept or press Enter to reject: ')
                    else:
                        move_input = input('Input the move: ')
                    temp = move_input.upper()
                    for i in [' ', '#', '+', 'X', '!', '?']:
                        temp = temp.replace(i, '')
                    selete_piece, moving_place = input_valid(main_game.player, temp)
                except:
                    continue
            
            #output input for computer
            else:
                main_game.display_board(main_game.oppo_player)
                print(f'Input the move: {move_input}')
                print()
                # try multi processing
                """
                if game_mode != 0 and main_game.player != player:
                        loading_icon(main_game.player.capitalize() + 'is thinking.', 3)
                """
                ...
                if game_mode == 1:
                    selete_piece, moving_place = Computer.level_1(main_game)
                    move_input = 'a1a1=q'  #auto promote to a queen
                
                elif game_mode == 2:
                    selete_piece, moving_place = Computer.level_2(main_game)
                    #return move_input (for promotion)
            
            #agreement (only for two player)
            if main_game.offer_draw:
                if selete_piece == 65:
                    main_game.ended_type = 'agreement'
                    main_game.ended = True
                main_game.offer_draw = False
                break
            
            #resign
            if selete_piece == 64:
                main_game.winner = main_game.oppo_player
                main_game.ended_type = 'resignation'
                main_game.ended = True
                break
            
            #offer draw
            elif selete_piece == 65:
                #two player
                if game_mode == 0:
                    main_game.offer_draw = True
                #vs computer
                else:
                    main_game.ended = True
                    main_game.winner = 'empty'
                    main_game.ended_type = 'agreement'
                break
            
            #save
            elif selete_piece == 66:
                main_game.switch_player()
                save_game(main_game, file_path, ended=False)
                return
            
            #quit
            elif selete_piece == 67:
                ...
                quit()
            
            #incorrect input
            elif selete_piece == -1:
                try:
                    input(Colour.Red + 'INPUT INCORRECT' + Colour.Reset + '\n' + Colour.Yellow + 'ENTER TO RETRY' + Colour.Reset)
                finally:
                    continue
            
            #valid input
            else:
                flag_valid, promote_miss =  main_game.check_valid_input(selete_piece, moving_place, temp)
                
                #loading
                if flag_valid:
                    main_game.check_win_draw()
                    break
            
            #invalid move
            try:
                if game_mode == 0 or main_game.player == player:
                    if promote_miss:
                        input(Colour.Red + 'INVALID PROMOTION' + Colour.Reset + '\n' + Colour.Yellow + 'ENTER TO RETRY' + Colour.Reset)
                    else:
                        input(Colour.Red + 'INVALID MOVE' + Colour.Reset + '\n' + Colour.Yellow + 'ENTER TO RETRY' + Colour.Reset)
            finally:
                continue
    
    
    try:
        clear_screen()
        save_game(main_game, file_path, ended=True)
        main_game.switch_player()
        main_game.display_board()
        if main_game.winner == 'empty':
            input(f'Draw by {main_game.ended_type}\nEnter for next game')
        else:
            input(f'{main_game.winner.upper()} win by {main_game.ended_type}\nEnter for next game')
    except:
        return



def input_int_check(output: str, choose) -> int:
    str_input = input(output).replace(' ', '')
    if str_input.isdecimal() and 0 < int(str_input) <= choose:
        return int(str_input)
    else:
        input(Colour.Reset + Colour.Red + 'INCORRECT INPUT' + Colour.Reset + '\n' + Colour.Yellow + 'ENTER TO RETRY' + Colour.Reset)
        return 0

def menu_output(stage: int) -> int:
    if stage == 1:
        print('1 <-- PvP')
        print('2 <-- PvE')
        print()
        return 2


def main() -> None:
    while True:
        try:
            clear_screen('Menu')
            stage = 1
            int_input = 0
            while int_input == 0:
                choices = menu_output(stage)
                int_input = input_int_check('Input number: ', choices)
            chess_game('file_path', int_input - 1)
        except:
            pass
