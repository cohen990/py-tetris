import numpy as np
from game import Game


def test_new_game_dimensions():
    game = Game()
    assert len(game.board) == 21
    assert all(len(row) == 10 for row in game.board)


def test_new_game_empty_except_floor():
    game = Game()
    for row in game.board[:-1]:
        assert all(cell == 0 for cell in row)
    assert all(cell == 8 for cell in game.board[-1])


def test_apply_move():
    game = Game()
    piece = [[1, 1], [1, 1]]
    game.apply_move(piece, (0, 1))
    assert game.board[0][0] == 1
    assert game.board[0][1] == 1
    assert game.board[1][0] == 1
    assert game.board[1][1] == 1
    assert game.board[0][2] == 0


def test_apply_move_does_not_overwrite():
    game = Game()
    game.board[5][3] = 2
    piece = [[1, 1]]
    game.apply_move(piece, (3, 6))
    assert game.board[5][3] == 3


def test_flatten_shape():
    game = Game()
    flat = game.flatten()
    assert flat.shape == (20, 10, 1)


def test_flatten_binary():
    game = Game()
    game.board[0][0] = 5
    game.board[0][1] = 3
    flat = game.flatten()
    assert flat[0][0][0] == 1
    assert flat[0][1][0] == 1
    assert flat[0][2][0] == 0


def test_copy_is_independent():
    game = Game()
    game.board[0][0] = 1
    clone = game.copy()
    clone.board[0][0] = 9
    assert game.board[0][0] == 1
    assert clone.board[0][0] == 9


def test_copy_preserves_board():
    game = Game()
    game.board[3][5] = 7
    clone = game.copy()
    assert clone.board[3][5] == 7
    assert clone.width == game.width
    assert clone.height == game.height


def test_board_without_bottom_row():
    game = Game()
    board = game.board_without_bottom_row()
    assert len(board) == 20
    assert all(cell == 0 for row in board for cell in row)
