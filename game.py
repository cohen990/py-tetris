import numpy as np


class Game:
    # noinspection PyUnusedLocal
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]
        self.board += [[1 for x in range(self.width)]]

    def flatten(self):
        cleaned = self.board[:-1]
        inputs = np.array(cleaned).reshape(self.height, self.width, 1)
        return inputs

    def apply_move(self, piece, position):
        position_x, position_y = position
        for y, row in enumerate(piece):
            for x, val in enumerate(row):
                self.board[y + position_y - 1][x + position_x] += val
