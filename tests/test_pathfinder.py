from game import Game
import engine
import pathfinder
import tetrominos


def test_has_path_straight_down():
    game = Game()
    piece = tetrominos.O
    origin = engine.get_origin(piece, 10)
    target = (origin[0], 19, piece)
    assert pathfinder.has_path(game.board, piece, origin, target)


def test_has_path_to_left():
    game = Game()
    piece = tetrominos.O
    origin = engine.get_origin(piece, 10)
    target = (0, 19, piece)
    assert pathfinder.has_path(game.board, piece, origin, target)


def test_has_path_to_right():
    game = Game()
    piece = tetrominos.O
    origin = engine.get_origin(piece, 10)
    target = (8, 19, piece)
    assert pathfinder.has_path(game.board, piece, origin, target)


def test_has_path_with_rotation():
    game = Game()
    piece = tetrominos.T
    rotated = engine.rotate(piece, 1)
    origin = engine.get_origin(piece, 10)
    target = (4, 18, rotated)
    assert pathfinder.has_path(game.board, piece, origin, target)


def test_no_path_blocked():
    game = Game()
    # Build a wall across row 10
    game.board[10] = [1] * 10
    piece = tetrominos.O
    origin = engine.get_origin(piece, 10)
    # Target is below the wall
    target = (4, 20, piece)
    assert not pathfinder.has_path(game.board, piece, origin, target)


def test_path_through_gap():
    game = Game()
    # Wall with a gap wide enough for the I piece vertical
    game.board[10] = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
    piece_horizontal = tetrominos.I
    piece_vertical = engine.rotate(tetrominos.I, 1)
    origin = engine.get_origin(piece_horizontal, 10)
    target = (3, 15, piece_vertical)
    assert pathfinder.has_path(game.board, piece_horizontal, origin, target)


def test_no_path_gap_too_small():
    game = Game()
    # Wall with a gap only 1 wide - O piece is 2 wide
    game.board[10] = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
    piece = tetrominos.O
    origin = engine.get_origin(piece, 10)
    target = (3, 20, piece)
    assert not pathfinder.has_path(game.board, piece, origin, target)


def test_has_path_target_is_origin():
    game = Game()
    piece = tetrominos.O
    origin = engine.get_origin(piece, 10)
    target = (origin[0], origin[1], piece)
    assert pathfinder.has_path(game.board, piece, origin, target)
