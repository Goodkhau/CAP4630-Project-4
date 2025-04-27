import chess
from tabulate import tabulate
from fenConversion import*
import tensorflow as tf
from tensorflow import keras
import time
import ChessMLM


def print_board():
    start = "\033[1;93m"
    end = "\033[0m"
    header = [' ', start + 'a' + end, start + 'b' + end, start + 'c' + end, start + 'd' + end, start + 'e' + end, start + 'f' + end, start + 'g' + end, start + 'h' + end]

    rows_info = []
    for row in range(8, 0, -1):
        row_info = [start + str(row) + end]
        for col in range(8):
            square = chess.square(col, row - 1)
            piece = ML.board.piece_at(square)
            row_info.append(piece.symbol() if piece else ' ')
        rows_info.append(row_info)

    table = tabulate(rows_info, header, tablefmt="heavy_grid")
    print(table)

def valid_coordinate(location):

    location = location.strip()
    if len(location) != 2:
        #print(len(location))
        return False
    
    letter = location[0]
    number = location[1]

    if not letter.isalpha():
        #print('not alpha')
        return False
    
    if not number.isdigit():
        #print('not digit')
        return False
    
    number = int(number)

    if not letter in 'abcdefgh':
        #print('not in letter')
        return False
    
    if not 1 <= number <= 8:
        #print('not in range number')
        return False
    
    return True

def select_piece():

    while True:
        piece = input('Choose Piece to move: ')

        if not valid_coordinate(piece):
            print('Please Put Valid Coordinate')
            continue

        square = chess.parse_square(piece)
        piece_moves = [move for move in ML.board.legal_moves if move.from_square == square]

        if piece_moves:
            break
        else:
            print('Choose a LEGAL Piece')

    return piece


def make_move(from_move):
    while True:

        move_to = input('Position to Move to: ')

        if not valid_coordinate(move_to):
            print('Please Put Valid Coordinate')
            continue

        promoted_piece = ''
        rank = int(move_to[1])
        if rank == 1 or rank == 8:
            square = chess.parse_square(from_move)
            piece = ML.board.piece_at(square)
            if chess.PAWN == piece.piece_type:
                print('Type "q" for Queen, "r" for Rook, "b" for Bishop, "n" for Knight')
                promoted_piece = input('Promotion Piece: ')

        if ML.move(from_move, move_to, promoted_piece):
            break
        else:
            print('Choose a LEGAL Position')


## Commandline program, **only for debugging and testing
def Optional_Engine_Cycle():
    while True:
        print()
        print_board()
        if ML.board.turn == chess.WHITE:
            print("White Turn to Move")
            start = select_piece()
            make_move(start)
            time.sleep(0.5)
            print()
        else:
            time.sleep(1.5)  # time delay so you can actually see what you moved
            print("Black Has Moved")
            ML.ai_select_move()
        result = ML.board.result()
        if result != "*":
            print_board()
            print(result)
            break

## Only runs if you start file directly
if __name__ == '__main__':
    ML = ChessMLM.ChessML()
    Optional_Engine_Cycle()
