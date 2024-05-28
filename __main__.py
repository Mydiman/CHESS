"""CHESS"""



from copy import deepcopy



def clear_screen() -> None:
    from os import system
    from platform import system as platform_system
    if platform_system() == "Windows":
        system('cls')
    else:
        system('clear')



class Colour:
	Reset: str = '\033[0m\033[K'
	Red: str = '\033[31m'
	Green: str = '\033[32m'
	Yellow: str = '\033[33m'
	OnWhite: str = '\033[30;47m'
	Underline: str = '\033[4m'



class BoardCell:
    def __init__(self, player, piece):
        self.player = player
        self.piece = piece

    #check if the seleted piece valid
    def check_selete_valid(self, player):
        if player == self.player:
            return True
        return False



def main() -> None: 
    #check if the piece can move to
    #-1 = invalided move
    #0  = move
    #1  = capture
    #2  = enpassant is able for the next player
    #3  = promotion
    #4  = castling (king to rook same player)
    #5  = enpassant
    def check_moving_valid(row_selete, column_selete, row_moving, column_moving) -> int:
        match board [row_selete][column_selete].piece:
            case "pawn":
                if board [row_selete][column_selete].player == "white":
                    if column_selete == column_moving:
                        if row_selete == 1 and row_moving == 3:
                            if board [2][column_moving].piece == "empty" and board [3][column_moving].piece == "empty":
                                if column_moving + 1 <= 7 and board [row_moving][column_moving + 1].piece == "pawn" and board [row_moving][column_moving + 1].player == "black":
                                    return 2
                                elif column_moving - 1 >= 0 and board [row_moving][column_moving - 1].piece == "pawn" and board [row_moving][column_moving - 1].player == "black":
                                    return 2
                                else:
                                    return 0
                        elif row_selete + 1 == row_moving:
                            if row_moving == 7:
                                if board [row_moving][column_moving].piece == "empty":
                                    return 3
                            else:
                                if board [row_moving][column_moving].piece == "empty":
                                    return 0
                    elif column_selete == column_moving + 1 or column_selete == column_moving - 1:
                        if row_selete + 1 == row_moving:
                            if board [row_moving][column_moving].player == "black":
                                if row_moving == 7:
                                    return 3
                                return 1
                            elif (row_moving - 1) * 8 + column_moving == enpassant:
                                return 5

                else:
                    if column_selete == column_moving:
                        if row_selete == 6 and row_moving == 4:
                            if board [5][column_moving].piece == "empty" and board [4][column_moving].piece == "empty":
                                if column_moving + 1 <= 7 and board [row_moving][column_moving + 1].piece == "pawn" and board [row_moving][column_moving + 1].player == "white":
                                    return 2
                                elif  column_moving - 1 >= 0 and board [row_moving][column_moving - 1].piece == "pawn" and board [row_moving][column_moving - 1].player == "white":
                                    return 2
                                else:
                                    return 0
                        elif row_selete - 1 == row_moving:
                            if row_moving == 0:
                                if board [row_moving][column_moving].piece == "empty":
                                    return 3
                            else:
                                if board [row_moving][column_moving].piece == "empty":
                                    return 0
                    elif column_selete == column_moving + 1 or column_selete == column_moving - 1:
                        if row_selete - 1 == row_moving:
                            if board [row_moving][column_moving].player == "white":
                                if row_moving == 0:
                                    return 3
                                return 1
                            elif (row_moving + 1) * 8 + column_moving == enpassant:
                                return 5

            case "knight":
                if ((abs(row_moving - row_selete) == 1) and (abs(column_moving - column_selete) == 2)) or ((abs(row_moving - row_selete) == 2) and (abs(column_moving - column_selete) == 1)):
                    if board [row_moving][column_moving].player == "empty":
                        return 0
                    return 1

            case "bishop":
                if abs(row_moving - row_selete) == abs(column_moving - column_selete):
                    row = row_selete
                    column = column_selete
                    if row_moving > row_selete:
                        if column_moving > column_selete:
                            for i in range(row_moving - row_selete - 1):
                                row += 1
                                column += 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1
                        else:
                            for i in range(row_moving - row_selete - 1):
                                row += 1
                                column -= 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1
                    else:
                        if column_moving > column_selete:
                            for i in range(row_selete - row_moving - 1):
                                row -= 1
                                column += 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1
                        else:
                            for i in range(row_selete - row_moving - 1):
                                row -= 1
                                column -= 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1

            case "rook":
                column = column_selete
                row = row_selete
                if row_selete == row_moving:
                    if column_moving > column_selete:
                        for i in range(column_moving - column_selete - 1):
                            column += 1
                            if board [row_selete][column].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                    else:
                        for i in range(column_selete - column_moving - 1):
                            column -= 1
                            if board [row_selete][column].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                elif column_selete == column_moving:
                    if row_moving > row_selete:
                        for i in range(row_moving - row_selete - 1):
                            row += 1
                            if board [row][column_selete].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                    else:
                        for i in range(row_selete - row_moving - 1):
                            row -= 1
                            if board [row][column_selete].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1

            case "queen":
                if row_selete == row_moving:
                    column = column_selete
                    if column_moving > column_selete:
                        for i in range(column_moving - column_selete - 1):
                            column += 1
                            if board [row_selete][column].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                    else:
                        for i in range(column_selete - column_moving - 1):
                            column -= 1
                            if board [row_selete][column].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                elif column_selete == column_moving:
                    row = row_selete
                    if row_moving > row_selete:
                        for i in range(row_moving - row_selete - 1):
                            row += 1
                            if board [row][column_selete].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                    else:
                        for i in range(row_selete - row_moving - 1):
                            row -= 1
                            if board [row][column_selete].player != "empty":
                                return -1
                        if board [row_moving][column_moving].player == "empty":
                            return 0
                        return 1
                elif abs(row_moving - row_selete) == abs(column_moving - column_selete):
                    row = row_selete
                    column = column_selete
                    if row_moving > row_selete:
                        if column_moving > column_selete:
                            for i in range(row_moving - row_selete - 1):
                                row += 1
                                column += 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1
                        else:
                            for i in range(row_moving - row_selete - 1):
                                row += 1
                                column -= 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1
                    else:
                        if column_moving > column_selete:
                            for i in range(row_selete - row_moving - 1):
                                row -= 1
                                column += 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1
                        else:
                            for i in range(row_selete - row_moving - 1):
                                row -= 1
                                column -= 1
                                if board [row][column].player != "empty":
                                    return -1
                            if board [row_moving][column_moving].player == "empty":
                                return 0
                            return 1

            case "king":
                if board [row_moving][column_moving].player == board [row_selete][column_selete].player == "white":
                    if column_moving == 0 and castling [0]:
                        return 4
                    elif column_moving == 7 and castling [1]:
                        return 4
                elif board [row_moving][column_moving].player == board [row_selete][column_selete].player == "black":
                    if column_moving == 0 and castling [2]:
                        return 4
                    elif column_moving == 7 and castling [3]:
                        return 4
                elif abs(row_moving - row_selete) <= 1 and abs(column_moving - column_selete) <= 1:
                    if board [row_moving][column_moving].player == "empty":
                        return 0
                    return 1
        
        return -1
        


    def display_board(board, player) -> None:
        clear_screen()

        half_to_full = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
        half_to_full[0x20] = 0x3000
            
        def fullen(s):
            '''
            Convert all ASCII characters to the full-width counterpart.
            '''
            return str(s).translate(half_to_full)

        piece_list = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        white_piece = [u"\u2659", u"\u2658", u"\u2657", u"\u2656", u"\u2655", u"\u2654"]
        black_piece = [u"\u265F", u"\u265E", u"\u265D", u"\u265C", u"\u265B", u"\u265A"]
        
        if player == "white":
            print(Colour.Underline + "White's turn" + Colour.Reset)
            print()
            print("      " + fullen("a") + "   " + fullen("b") + "   " + fullen("c") + "   " + fullen("d") + "   " + fullen("e") + "   " + fullen("f") + "   " + fullen("g") + "   " + fullen("h") + f"        {Colour.Underline}Input Examples{Colour.Reset}")
            for i in range(8):
                if i == 0:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Moving from a1 to a2    -> a1a2")
                elif i == 1:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Queenside castling      -> 0-0-0")
                elif i == 2:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Promote to a rook       -> a7a8=R")
                elif i == 3:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Promote to a knight     -> a7a8=N")
                elif i == 4:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Offer or accept a draw  -> draw")
                else:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ")
                print(" " + fullen(f"{8 - i}") + " ", end = f"{Colour.OnWhite}|")
                for j in range(8):
                    if board [7 - i][j].player == "white":
                        for k in range(6):
                            if board [7 - i][j].piece == piece_list [k]:
                                print(" " + white_piece [k], end = "  |")
                    elif board [7 - i][j].player == "black":
                        for k in range(6):
                            if board [7 - i][j].piece == piece_list [k]:
                                print(" " + black_piece [k], end = "  |")
                    else:
                        print("    ", end = "|")
                if i == 0:
                    print(f"{Colour.Reset} " + fullen(f"{8 - i}") + "   Kingside castling       -> 0-0")
                elif i == 1:
                    print(f"{Colour.Reset} " + fullen(f"{8 - i}") + "   Promote to a queen      -> a7a8=Q")
                elif i == 2:
                    print(f"{Colour.Reset} " + fullen(f"{8 - i}") + "   Promote to a bishop     -> a7a8=B")
                elif i == 3:
                    print(f"{Colour.Reset} " + fullen(f"{8 - i}") + "   En passant              -> a5b6")
                elif i == 4:
                    print(f"{Colour.Reset} " + fullen(f"{8 - i}") + "   Resign                  -> resign")
                else:
                    print(f"{Colour.Reset} " + fullen(f"{8 - i}") + "   ")
            print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ")
            print("      " + fullen("a") + "   " + fullen("b") + "   " + fullen("c") + "   " + fullen("d") + "   " + fullen("e") + "   " + fullen("f") + "   " + fullen("g") + "   " + fullen("h") + "        ")
            print("")

        else:
            print(Colour.Underline + "Black's turn" + Colour.Reset)
            print()
            print("      " + fullen("h") + "   " + fullen("g") + "   " + fullen("f") + "   " + fullen("e") + "   " + fullen("d") + "   " + fullen("c") + "   " + fullen("b") + "   " + fullen("a") + f"        {Colour.Underline}Input Examples{Colour.Reset}")
            for i in range(8):
                if i == 0:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Moving from a1 to a2    -> a1a2")
                elif i == 1:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Queenside castling      -> 0-0-0")
                elif i == 2:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Promote to a rook       -> a2a1=R")
                elif i == 3:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Promote to a knight     -> a2a1=N")
                elif i == 4:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      Offer or accept a draw  -> draw")
                else:
                    print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ")
                print(" " + fullen(f"{i + 1}") + " ", end = f"{Colour.OnWhite}|")
                for j in range(8):
                    if board [i][7 - j].player == "white":
                        for k in range(6):
                            if board [i][7 - j].piece == piece_list [k]:
                                print(" " + white_piece [k], end = "  |")
                    elif board [i][7 - j].player == "black":
                        for k in range(6):
                            if board [i][7 - j].piece == piece_list [k]:
                                print(" " + black_piece [k], end = "  |")
                    else:
                        print("    ", end = "|")
                if i == 0:
                    print(f"{Colour.Reset} " + fullen(f"{i + 1}") + "   Kingside castling       -> 0-0")
                elif i == 1:
                    print(f"{Colour.Reset} " + fullen(f"{i + 1}") + "   Promote to a queen      -> a2a1=Q")
                elif i == 2:
                    print(f"{Colour.Reset} " + fullen(f"{i + 1}") + "   Promote to a bishop     -> a2a1=B")
                elif i == 3:
                    print(f"{Colour.Reset} " + fullen(f"{i + 1}") + "   En passant              -> a4b3")
                elif i == 4:
                    print(f"{Colour.Reset} " + fullen(f"{i + 1}") + "   Resign                  -> resign")
                else:
                    print(f"{Colour.Reset} " + fullen(f"{i + 1}") + "   ")
            print(f"    {Colour.OnWhite}-----------------------------------------{Colour.Reset}      ")
            print("      " + fullen("h") + "   " + fullen("g") + "   " + fullen("f") + "   " + fullen("e") + "   " + fullen("d") + "   " + fullen("c") + "   " + fullen("b") + "   " + fullen("a") + "        ")
            print("")



    def check_moving_piece(player, str_input) -> list:
        if len(str_input) == 3:
            if str_input [0] == "0" and str_input [1] == "-" and str_input [2] == "0":
                if player == "white":
                    return [4, 7]
                return [60, 63]
        
        if len(str_input) == 4:
            if (str_input [0].isalpha() and str_input [1].isdecimal()):
                column = ord(str_input [0]) - 65
                row = int(str_input [1]) - 1
                if 0 <= row < 8 and 0 <= column < 8:
                    if board [row][column].check_selete_valid(player):

                        if (str_input [2].isalpha() and str_input [3].isdecimal()):
                            column1 = ord(str_input [2]) - 65
                            row1 = int(str_input [3]) - 1
                            if 0 <= row1 < 8 and 0 <= column1 < 8:
                                if not board [row1][column1].check_selete_valid(player):
                                    return [row * 8 + column, row1 * 8 + column1]
            
            if str_input == "DRAW":
                return [65, 65]

        if len(str_input) == 5:
            if str_input [0] == "0" and str_input [1] == "-" and str_input [2] == "0" and str_input [3] == "-" and str_input [4] == "0":
                if player == "white":
                    return [4, 0]
                return [60, 56]
        
        if len(str_input) == 6:
            if (str_input [0].isalpha() and str_input [1].isdecimal()):
                column = ord(str_input [0]) - 65
                row = int(str_input [1]) - 1
                if 0 <= row < 8 and 0 <= column < 8:
                    if board [row][column].check_selete_valid(player):

                        if (str_input [2].isalpha() and str_input [3].isdecimal()):
                            column1 = ord(str_input [2]) - 65
                            row1 = int(str_input [3]) - 1
                            if 0 <= row1 < 8 and 0 <= column1 < 8:
                                if not board [row1][column1].check_selete_valid(player):
                                    if str_input [4] == "=" and (str_input [5] == "Q" or str_input [5] == "R" or str_input [5] == "B" or str_input [5] == "N"):
                                        return [row * 8 + column, row1 * 8 + column1]
            
            if str_input == "RESIGN":
                return [64, 64]
        return [-1, -1]
    


    def change_board(row_selete, column_selete, row_moving, column_moving, str_input, moving_type) -> list:
        copy_board = deepcopy(board)
        if moving_type <= 2:
            copy_board [row_moving][column_moving].piece, copy_board [row_moving][column_moving].player = copy_board [row_selete][column_selete].piece, copy_board [row_selete][column_selete].player
            copy_board [row_selete][column_selete].piece, copy_board [row_selete][column_selete].player = "empty", "empty"
        
        elif moving_type == 3:
            if str_input [5].upper() == "Q":
                copy_board [row_moving][column_moving].piece = "queen"
            elif str_input [5].upper() == "R":
                copy_board [row_moving][column_moving].piece = "rook"
            elif str_input [5].upper() == "B":
                copy_board [row_moving][column_moving].piece = "bishop"
            elif str_input [5].upper() == "N":
                copy_board [row_moving][column_moving].piece = "knight"
            copy_board [row_moving][column_moving].player = copy_board [row_selete][column_selete].player
            copy_board [row_selete][column_selete].piece, copy_board [row_selete][column_selete].player = "empty", "empty"
        
        elif moving_type == 4:
            if row_selete == 0:
                if column_moving == 0:
                    copy_board [0][0].piece, copy_board [0][0].player = "empty", "empty"
                    copy_board [0][1].piece, copy_board [0][1].player = "empty", "empty"
                    copy_board [0][2].piece, copy_board [0][2].player = "king", "white"
                    copy_board [0][3].piece, copy_board [0][3].player = "rook", "white"
                    copy_board [0][4].piece, copy_board [0][4].player = "empty", "empty"
                else:
                    copy_board [0][4].piece, copy_board [0][4].player = "empty", "empty"
                    copy_board [0][5].piece, copy_board [0][5].player = "rook", "white"
                    copy_board [0][6].piece, copy_board [0][6].player = "king", "white"
                    copy_board [0][7].piece, copy_board [0][7].player = "empty", "empty"
            else:
                if column_moving == 0:
                    copy_board [7][0].piece, copy_board [7][0].player = "empty", "empty"
                    copy_board [7][1].piece, copy_board [7][1].player = "empty", "empty"
                    copy_board [7][2].piece, copy_board [7][2].player = "king", "black"
                    copy_board [7][3].piece, copy_board [7][3].player = "rook", "black"
                    copy_board [7][4].piece, copy_board [7][4].player = "empty", "empty"
                else:
                    copy_board [7][4].piece, copy_board [7][4].player = "empty", "empty"
                    copy_board [7][5].piece, copy_board [7][5].player = "rook", "black"
                    copy_board [7][6].piece, copy_board [7][6].player = "king", "black"
                    copy_board [7][7].piece, copy_board [7][7].player = "empty", "empty"
        else:
            if copy_board [row_selete][column_selete].player == "white":
                copy_board [row_moving][column_moving].piece, copy_board [row_moving][column_moving].player = "pawn", "white"
                copy_board [row_selete][column_selete].piece, copy_board [row_selete][column_selete].player = "empty", "empty"
                copy_board [row_moving - 1][column_moving].piece, copy_board [row_moving - 1][column_moving].player = "empty", "empty"
            else:
                copy_board [row_moving][column_moving].piece, copy_board [row_moving][column_moving].player = "pawn", "black"
                copy_board [row_selete][column_selete].piece, copy_board [row_selete][column_selete].player = "empty", "empty"
                copy_board [row_moving + 1][column_moving].piece, copy_board [row_moving + 1][column_moving].player = "empty", "empty"
        return copy_board



    def update_castling(board, castling, castling_already) -> list:
        castling = [False, False, False, False]
        if not castling_already [0]:
            if board [0][1].player == board [0][2].player == board [0][3].player == "empty":
                if (not undercheck("white", 0, 2)) and (not undercheck("white", 0, 3)) and (not undercheck("white", 0, 4)):
                    castling [0] = True
        
        if not castling_already [1]:
            if board [0][5].player == board [0][6].player == "empty":
                if (not undercheck("white", 0, 4)) and (not undercheck("white", 0, 5)) and (not undercheck("white", 0, 6)):
                    castling [1] = True
        
        if not castling_already [2]:
            if board [7][1].player == board [7][2].player == board [7][3].player == "empty":
                if (not undercheck("black", 7, 2)) and (not undercheck("black", 7, 3)) and (not undercheck("white", 7, 4)):
                    castling [2] = True
        
        if not castling_already [3]:
            if board [7][5].player == board [7][6].player == "empty":
                if (not undercheck("white", 7, 4)) and (not undercheck("black", 7, 5)) and (not undercheck("black", 7, 6)):
                    castling [3] = True
        return castling



    def update_castling_already() -> list:
        copy_castling_already = deepcopy(castling_already)
        if board [row_selete][column_selete].piece == "rook":
            if selete_place == 0:
                copy_castling_already [0] = True
            elif selete_place == 7:
                copy_castling_already [1] = True
            elif selete_place == 56:
                copy_castling_already [2] = True
            elif selete_place == 63:
                copy_castling_already [3] = True
        elif board [row_selete][column_selete].piece == "king":
            if board [row_selete][column_selete].player == "white":
                copy_castling_already [0] = True
                copy_castling_already [1] = True
            else:
                copy_castling_already [2] = True
                copy_castling_already [3] = True
        return copy_castling_already



    def search_king(board, player) -> list:
        for i in range(8):
            for j in range(8):
                if board [i][j].piece == "king" and board [i][j].player == player:
                    return [i, j]



    def undercheck(player, row_king, column_king) -> bool:
        copy_board = deepcopy(board)
        if player == "white":
            oppo_player = "black"
            pawn_row = 1
        else:
            oppo_player = "white"
            pawn_row = -1
        
        #pawn
        if copy_board [row_king + pawn_row][column_king + 1].player == oppo_player and copy_board [row_king + pawn_row][column_king + 1].piece == "pawn":
            return True
        if copy_board [row_king + pawn_row][column_king - 1].player == oppo_player and copy_board [row_king + pawn_row][column_king - 1].piece == "pawn":
            return True
        
        #king
        corr_oppo_king = search_king(copy_board, oppo_player)
        if abs(row_king - corr_oppo_king [0]) <= 1 and abs(column_king - corr_oppo_king [1]):
            return False
        
        #knight
        knight_move = [[[2, -2], [1, -1]], [[1, -1], [2, -2]]]
        for i in knight_move:
            for j in i [0]:
                for k in i [1]:
                    if 0 <= row_king + j <= 7 and 0 <= column_king + k <= 7:
                        if copy_board [row_king + j][column_king + k].player == oppo_player and copy_board [row_king + j][column_king + k].piece == "knight":
                            return True
        
        #queen, rook
        for i in range(row_king + 1, 8):
            if copy_board [i][column_king].player == oppo_player and (copy_board [i][column_king].piece == "rook" or copy_board [i][column_king].piece == "queen"):
                return True
            if copy_board [i][column_king].player != "empty":
                break
        for i in range(row_king):
            if copy_board [row_king - i - 1][column_king].player == oppo_player and (copy_board [row_king - i - 1][column_king].piece == "rook" or copy_board [row_king - i - 1][column_king].piece == "queen"):
                return True
            if copy_board [row_king - i - 1][column_king].player != "empty":
                break
        for i in range(column_king + 1, 8):
            if copy_board [row_king][i].player == oppo_player and (copy_board [row_king][i].piece == "rook" or copy_board [row_king][i].piece == "queen"):
                return True
            if copy_board [row_king][i].player != "empty":
                break
        for i in range(column_king):
            if copy_board [row_king][column_king - i - 1].player == oppo_player and (copy_board [row_king][column_king - i - 1].piece == "rook" or copy_board [row_king][column_king - i - 1].piece == "queen"):
                return True
            if copy_board [row_king][column_king - i - 1].player != "empty":
                break
        
        #queen, bishop
        bishop_move = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for i in bishop_move:
            row_bishop = row_king + i [0]
            column_bishop = column_king + i [1]
            while 0 <= row_bishop <= 7 and 0 <= column_bishop <= 7:
                if copy_board [row_bishop][column_bishop].player == oppo_player and (copy_board [row_bishop][column_bishop].piece == "bishop" or copy_board [row_bishop][column_bishop].piece == "queen"):
                    return True
                if  copy_board [row_bishop][column_bishop].player != "empty":
                    break
                row_bishop += i [0]
                column_bishop += i [0]
        return False



    def undercheck_after_moving(row_selete, column_selete, row_moving, column_moving, str_input, moving_type, player) -> bool:
        board_after_move = change_board(row_selete, column_selete, row_moving, column_moving, str_input, moving_type)
        corr_king = search_king(board_after_move, player)
        return undercheck(player, corr_king [0], corr_king [1])
    


    def all_possible_move(board, player) -> list:
        all_possible = []
        all_possible_type = []
        for i in range(8):
            for j in range(8):
                if board [i][j].player == player:
                    for k in range(8):
                        for l in range(8):
                            if board [k][l].player != player:
                                moving_type = check_moving_valid(i, j, k, l)
                                if moving_type == 3:
                                    all_possible_type.append(moving_type)
                                    all_possible.append(chr(65 + j) + chr(49 + i) + chr(65 + l) + chr(49 + k) + "=Q")
                                elif moving_type != -1:
                                    all_possible_type.append(moving_type)
                                    all_possible.append(chr(65 + j) + chr(49 + i) + chr(65 + l) + chr(49 + k))

                    if board [i][j].piece == "king" and board [i][j].player == player:
                        if castling [0] and player == "white":
                            moving_type = check_moving_valid(i, j, 0, 0)
                            if moving_type == 4:
                                all_possible_type.append(moving_type)
                                all_possible.append("0-0-0")
                        if castling [1] and player == "white":
                            moving_type = check_moving_valid(i, j, 0, 7)
                            if moving_type == 4:
                                all_possible_type.append(moving_type)
                                all_possible.append("0-0")
                        if castling [2] and player == "black":
                            moving_type = check_moving_valid(i, j, 7, 0)
                            if moving_type == 4:
                                all_possible_type.append(moving_type)
                                all_possible.append("0-0-0")
                        if castling [3] and player == "black":
                            moving_type = check_moving_valid(i, j, 7, 7)
                            if moving_type == 4:
                                all_possible_type.append(moving_type)
                                all_possible.append("0-0")
        
        for i in range(len(all_possible)):
            selete_place, moving_place = check_moving_piece(player, all_possible [len(all_possible) - i - 1])
            row_selete, column_selete = selete_place // 8, selete_place % 8
            row_moving, column_moving = moving_place // 8, moving_place % 8
            new_board = change_board(row_selete, column_selete, row_moving, column_moving, all_possible [len(all_possible) - i - 1], all_possible_type [len(all_possible) - i - 1])
            corr_king = search_king(new_board, player)
            if undercheck(player, corr_king [0], corr_king [1]):
                del all_possible [len(all_possible) - i - 1]
        return all_possible
    


    def stalemate_checkmate(board, oppo_player) -> bool:
        move_list = all_possible_move(board, oppo_player)
        if len(move_list) == 0:
            return True
        return False
    


    def insufficient_material_draw_check(board) -> bool:
        white_piece = []
        black_piece = []
        for i in range(8):
            for j in range(8):
                if board [i][j].player == "white":
                    if board [i][j].piece == "bishop":
                        if (i + j) % 2 == 0:
                            white_piece.append("bishop dark")
                        else:
                            white_piece.append("bishop light")
                    elif board [i][j].piece != "king":
                        white_piece.append(board [i][j].piece)
                if board [i][j].player == "black":
                    if board [i][j].piece == "bishop":
                        if (i + j) % 2 == 0:
                            black_piece.append("bishop dark")
                        else:
                            black_piece.append("bishop light")
                    elif board [i][j].piece != "king":
                        black_piece.append(board [i][j].piece)
        
        if white_piece == [] and black_piece == []:
            return True
        elif (white_piece == ["knight"] and black_piece == []) or (white_piece == [] and black_piece == ["knight"]):
            return True
        else:
            temp = ""
            for i in white_piece:
                if (temp == "" or temp == i) and (i == "bishop light" or i == "bishop dark"):
                    temp = i
                else:
                    return False
            for j in black_piece:
                if (temp == "" or temp == i) and (i == "bishop light" or i == "bishop dark"):
                    temp = i
                else:
                    return False
            return True



    def initial_setup() -> list:
        #initial setup
        board = []
        
        enpassant = 64

        #W Q, W K, B Q, B K
        castling = [False, False, False, False]
        castling_already = [False, False, False, False]
        
        # big -> white, small -> black, 0 -> empty
        testing_board = [
            'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
            'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
            'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'
            ]  #for testing
        if testing_board != []:
            for i in range(8):
                temp = []
                for j in range(8):
                    match testing_board [i * 8 + j]:
                        case "K":
                            temp.append(BoardCell("white", "king"))
                        case "Q":
                            temp.append(BoardCell("white", "queen"))
                        case "R":
                            temp.append(BoardCell("white", "rook"))
                        case "N":
                            temp.append(BoardCell("white", "knight"))
                        case "B":
                            temp.append(BoardCell("white", "bishop"))
                        case "P":
                            temp.append(BoardCell("white", "pawn"))
                        case "k":
                            temp.append(BoardCell("black", "king"))
                        case "q":
                            temp.append(BoardCell("black", "queen"))
                        case "r":
                            temp.append(BoardCell("black", "rook"))
                        case "n":
                            temp.append(BoardCell("black", "knight"))
                        case "b":
                            temp.append(BoardCell("black", "bishop"))
                        case "p":
                            temp.append(BoardCell("black", "pawn"))
                        case 0:
                            temp.append(BoardCell("empty", "empty"))
                board.append(temp)
        else:
            for i in range(8):
                temp = []
                for j in range(8):
                    if i == 0:
                        temp.append(BoardCell("white", ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"] [j]))
                    elif i == 1:
                        temp.append(BoardCell("white", "pawn"))
                    elif i == 7:
                        temp.append(BoardCell("black", ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"] [j]))
                    elif i == 6:
                        temp.append(BoardCell("black", "pawn"))
                    else:
                        temp.append(BoardCell("empty", "empty"))
                board.append(temp)
        return board, enpassant, castling, castling_already
        


    board, enpassant, castling, castling_already = initial_setup()
    
    game_end = False

    winner = "empty"

    end_type = ""  # insufficient material, stalemate, threefold repetition, fifty move rule, checkmate, agreement or resignation

    #three the same -> draw
    save_board = [board, 0, 0, 0, 0, 0, 0, 0]
    save_castling = [castling, 0, 0, 0, 0, 0, 0, 0]
    save_enpassant = [enpassant, 0, 0, 0, 0, 0, 0, 0]

    #fifty move rule when fifty_move_draw = 101
    fifty_move_draw = 0

    offer_draw = False

    count = -1
    while not game_end:
        count = (count + 1) % 2
        player = ["white", "black"][count]
        oppo_player = ["white", "black"][(count + 1) % 2]
        while True:
            display_board(board, player)
            if offer_draw:
                print("Your opponent is offering a draw")
                str_input = input("Input \"draw\" for accepting: ")
            else:
                str_input = input("Input the move: ")
            str_input = str_input.replace(' ', '')
            str_input = str_input.upper()
            selete_place, moving_place = check_moving_piece(player, str_input)
            if offer_draw:
                if selete_place == moving_place == 65:
                    end_type = "agreement"
                    game_end = True
                offer_draw = False
                break
            
            if selete_place == moving_place == 64:
                winner = oppo_player
                end_type = "resignation"
                game_end = True
                break
            
            elif selete_place == moving_place == 65:
                offer_draw = True
                break
            
            elif selete_place != -1 and moving_place != -1:
                row_selete, column_selete = selete_place // 8, selete_place % 8
                row_moving, column_moving = moving_place // 8, moving_place % 8
                moving_type = check_moving_valid(row_selete, column_selete, row_moving, column_moving)
                
                if undercheck_after_moving(row_selete, column_selete, row_moving, column_moving, str_input, moving_type, player):
                    moving_type == -1
                
                if moving_type != -1:
                    if moving_type == 0:
                        enpassant = 64
                        if board [row_selete][column_selete].piece == "pawn":
                            fifty_move_draw = 0
                        castling_already = update_castling_already()
                    
                    elif moving_type == 1:
                        enpassant = 64
                        fifty_move_draw = 0
                        castling_already = update_castling_already()
                    
                    elif moving_type == 2:
                        enpassant = moving_place
                        fifty_move_draw = 0
                    
                    elif moving_type == 3:
                        enpassant = 64
                        fifty_move_draw = 0
                    
                    elif moving_type == 4:
                        enpassant = 64
                        update_castling_already()
                    
                    elif moving_type == 5:
                        enpassant = 64
                        fifty_move_draw = 0
                    
                    board = change_board(row_selete, column_selete, row_moving, column_moving, str_input, moving_type)
                    castling = update_castling(board, castling, castling_already)
                    
                    if stalemate_checkmate(board, oppo_player):
                        row_king, column_king = search_king(board, oppo_player)
                        if undercheck(oppo_player, row_king, column_king):
                            winner = player
                            end_type = "checkmate"
                        else:
                            end_type = "stalemate"
                        game_end = True
                    
                    if not game_end:
                        if insufficient_material_draw_check(board):
                            end_type = "insufficient material"
                            game_end = True
                    
                    if not game_end:
                        if save_board[0] == board and save_board[4] == board:
                            if save_castling[0] == castling and save_castling[4] == castling:
                                if save_enpassant[0] == enpassant and save_enpassant[4] == enpassant:
                                    end_type = "threefold repetition"
                                    game_end = True
                        save_board.append(board)
                        save_castling.append(castling)
                        save_enpassant.append(enpassant)
                        if save_board [8] != 0:
                            del save_board [0], save_castling [0], save_enpassant [0]
                    
                    if fifty_move_draw == 101 and not game_end:
                        end_type = "fifty move rule"
                        game_end = True
                    else:
                        fifty_move_draw += 1
                    
                    break
                
                else:
                    print(Colour.Red + "INPUT INCORRECT" + Colour.Reset)
                    input(Colour.Yellow + "ENTER TO RETRY" + Colour.Reset)
            else:
                print(Colour.Red + "INPUT INCORRECT" + Colour.Reset)
                input(Colour.Yellow + "ENTER TO RETRY" + Colour.Reset)
    
    display_board(board, player)
    if winner == "empty":
        print(f"Draw by {end_type}")
        input("Enter for next game")
    else:
        print(f"{winner.upper()} win by {end_type}")
        input("Enter for next game")

while True:
    clear_screen()
    main()