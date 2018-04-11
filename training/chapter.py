import numpy as np


class Chapter:
    def __init__(self, board, number_of_moves, score):
        if np.array(board).shape != (21, 10):
            raise Exception("Attempted to create a board with shape " + str(np.array(board).shape))
        self.board = board
        self.number_of_moves = number_of_moves
        self.score = score

    def calculate_fitness(self):
        return self.score * 100 + self.number_of_moves
