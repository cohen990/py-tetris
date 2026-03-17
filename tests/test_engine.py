from game import Game
import engine
import tetrominos


def test_rotate_zero_times_is_identity():
    piece = tetrominos.T
    assert engine.rotate(piece, 0) == piece


def test_rotate_four_times_is_identity():
    for piece in [tetrominos.T, tetrominos.S, tetrominos.Z, tetrominos.J, tetrominos.L, tetrominos.I]:
        assert engine.rotate(piece, 4) == piece


def test_rotate_clockwise_T():
    rotated = engine.rotate(tetrominos.T, 1)
    assert rotated == [[1, 0], [1, 1], [1, 0]]


def test_rotate_clockwise_I():
    rotated = engine.rotate(tetrominos.I, 1)
    assert rotated == [[6], [6], [6], [6]]


def test_rotate_O_is_always_same():
    for n in range(4):
        assert engine.rotate(tetrominos.O, n) == tetrominos.O


def test_get_origin():
    piece_3_wide = [[1, 1, 1], [0, 1, 0]]
    x, y = engine.get_origin(piece_3_wide, 10)
    assert y == 0
    assert x == int(10 / 2 - 3 / 2)


def test_piece_has_collided_with_floor():
    game = Game()
    piece = [[1]]
    # y=21 with the -1 offset puts piece on row 20 (the floor row), which has value 8
    assert engine.piece_has_collided(game.board, piece, (0, 21))


def test_piece_has_not_collided_on_empty_board():
    game = Game()
    piece = [[1]]
    assert not engine.piece_has_collided(game.board, piece, (0, 5))


def test_piece_has_collided_with_existing_block():
    game = Game()
    game.board[5][3] = 1
    piece = [[1]]
    assert engine.piece_has_collided(game.board, piece, (3, 6))


def test_piece_has_collided_left_wall():
    game = Game()
    piece = [[1, 1]]
    assert engine.piece_has_collided(game.board, piece, (-1, 5))


def test_piece_has_collided_right_wall():
    game = Game()
    piece = [[1, 1]]
    assert engine.piece_has_collided(game.board, piece, (9, 5))


def test_piece_is_resting_on_floor():
    game = Game()
    piece = [[1]]
    assert engine.piece_is_resting(game.board, piece, (0, 20))


def test_piece_is_resting_on_block():
    game = Game()
    game.board[10][5] = 1
    piece = [[1]]
    assert engine.piece_is_resting(game.board, piece, (5, 10))


def test_piece_is_not_resting_midair():
    game = Game()
    piece = [[1]]
    assert not engine.piece_is_resting(game.board, piece, (0, 5))


def test_remove_rows_clears_full_row():
    game = Game()
    game.board[19] = [1] * 10
    cleared, new_board = engine.remove_rows(game.board)
    assert cleared == 1
    assert all(cell == 0 for cell in new_board[0])


def test_remove_rows_clears_multiple():
    game = Game()
    game.board[18] = [1] * 10
    game.board[19] = [1] * 10
    cleared, new_board = engine.remove_rows(game.board)
    assert cleared == 2


def test_remove_rows_no_full_rows():
    game = Game()
    cleared, new_board = engine.remove_rows(game.board)
    assert cleared == 0


def test_remove_rows_preserves_floor():
    game = Game()
    game.board[19] = [1] * 10
    cleared, new_board = engine.remove_rows(game.board)
    assert all(cell == 8 for cell in new_board[-1])


def test_move_is_legal_on_floor():
    game = Game()
    piece = tetrominos.O
    candidate = (4, 19, piece)
    assert engine.move_is_legal(game, candidate)


def test_move_is_legal_rejects_collision():
    game = Game()
    game.board[18][4] = 1
    piece = tetrominos.O
    candidate = (4, 19, piece)
    assert not engine.move_is_legal(game, candidate)


def test_play_applies_move_and_returns_new_piece():
    game = Game()
    piece = tetrominos.O
    move = (4, 19, piece)
    returned_game, new_piece = engine.play(move, game)
    assert returned_game is game
    assert game.board[18][4] == 7
