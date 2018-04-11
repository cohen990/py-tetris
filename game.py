import numpy as np


def get_inputs_from_board(board_state):
    cleaned = board_state[:-1]
    inputs = np.array(cleaned).reshape(20, 10, 1)
    return inputs