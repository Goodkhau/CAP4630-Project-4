import chess
from tabulate import tabulate
from fenConversion import*
import tensorflow as tf
from tensorflow import keras
import time


class ChessML:
    def __init__(self):
        self.board = chess.Board()
        self.checkmate_model = keras.models.load_model("models/mate_model.keras")
        self.evaluation_model = keras.models.load_model("models/eval_big_model_v2.keras")


    def move(self, selected_piece, selection, promoted_piece):
        move = chess.Move.from_uci(selected_piece + selection + promoted_piece)
        if self.board.is_legal(move):
            self.board.push(move)
            return True
        return False

    ## This method will select a move by our ML model from a list of possible moves
    ## The move is retained in the chess.Board() object.
    def ai_select_move(self, black=True):
        possible_moves = list(self.board.legal_moves)
        temp_board = self.board

        input_list = []
        for move in possible_moves:
            temp_board.push(move)
            fen = self.board.fen()
            input = FENParser(fen)
            input_list.append(input.parse())
            temp_board.pop()

        X = np.array(input_list)

        ## Integer of number of moves worth evaluation
        moves_index_eval = self.run_checkmate_model(X)
        if len(moves_index_eval) > 1:

            eval_positions = []  # will contain inputs that are worth evalating
            for index in moves_index_eval:
                move = possible_moves[index]  # move worth evaluating
                temp_board.push(move)
                fen = self.board.fen()
                input = FENParser(fen)
                eval_positions.append(input.parse())
                temp_board.pop()

            index_of_eval_positions = self.run_eval_model(np.array(
                eval_positions))  # returns index of eval_positions which is the same index for a position as moves_index_eval
            best_move_index = moves_index_eval[index_of_eval_positions]  # gets index of move using moves_index_eval
            best_move = possible_moves[best_move_index]

        else:
            best_move = possible_moves[moves_index_eval[0]]

        self.board.push(best_move)

    ## Returns a list of "good" moves
    def run_checkmate_model(self, X, black=True):
        Y = self.checkmate_model.predict_on_batch(X)
        indexes = np.argmax(Y, axis=1)  # 1 if forced mate for black, 2 if forced mate for white, 0 no forced mate

        i = 0
        selected_position_indexes = []
        alternatives = []
        if black:
            for index in indexes:
                if index == 1:  # forced mate for black preferred
                    selected_position_indexes = [i]
                    break
                elif index == 0:  # append if its not forced mate
                    selected_position_indexes.append(i)
                elif index == 2:
                    alternatives.append(i)
                i += 1
        else:
            print('functionality for white hasnt been implemented yet')
        if len(selected_position_indexes) == 0:  # edge case if there are no good moves for black we have to still give it a index to move
            selected_position_indexes.append(alternatives[0])  # so we just choose the first alternative
        return selected_position_indexes

    def run_eval_model(self, X):
        ## Returns tensor array (3, 1)
        Y = self.evaluation_model.predict_on_batch(X)

        i = 0
        centipawn = Y[0]
        pos_index = 0
        for pred_value in Y:
            if pred_value[0] < centipawn:
                centipawn = pred_value[0]
                pos_index = i
            i += 1
        return pos_index