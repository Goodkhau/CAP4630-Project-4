import chess
from tabulate import tabulate
from fenConversion import*
import tensorflow as tf
from tensorflow import keras
import time
import ChessMLM


class ChessML:
    def __init__(self):
        self.board = chess.Board()
        self.checkmate_model = keras.models.load_model("models/mate_model.keras")
        self.evaluation_model = keras.models.load_model("models/eval_big_model_v2.keras")