import engine
from enum import Enum
from copy import deepcopy

class Move(Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    ROTATE_COUNTERCLOCKWISE = 4
    ROTATE_CLOCKWISE = 5

valid_moves = [Move.LEFT, Move.RIGHT, Move.DOWN, Move.ROTATE_COUNTERCLOCKWISE, Move.ROTATE_CLOCKWISE]

def has_path(game_board, piece, position, target):
    has_path, _ = has_path_recursive(game_board, piece, position, target, None, [])
    return has_path

def has_path_recursive(game_board, piece, position, target, last_move, attempted_moves):
    move = get_move(piece, position)

    if move in attempted_moves:
        return False, attempted_moves
    attempted_moves.append(move)

    target_x, target_y, target_piece = target
    if piece == target_piece and position == (target_x, target_y):
        return True, attempted_moves
    
    has_found_path = False
    for move in valid_moves:
        if not move == get_opposite(last_move):
            new_position = deepcopy(position)
            new_piece = deepcopy(piece)
            if move == Move.LEFT:
                new_position = move_left(position)
            if move == Move.RIGHT:
                new_position = move_right(position)
            if move == Move.DOWN:
                new_position = move_down(position)
            if move == Move.ROTATE_COUNTERCLOCKWISE:
                new_piece = engine.rotate(piece, 3)
            if move == Move.ROTATE_CLOCKWISE:
                new_piece = engine.rotate(piece, 1)
            if not engine.piece_has_collided(game_board, new_piece, new_position):
                has_found_path, attempted_moves = has_path_recursive(game_board, new_piece, new_position, target, move, attempted_moves)
            if has_found_path:
                return True, attempted_moves
                
    return has_found_path, attempted_moves

def get_move(piece, position):
    x, y = position
    return (x, y, piece)

def get_opposite(move):
    if move == Move.LEFT:
        return Move.RIGHT
    if move == Move.RIGHT:
        return Move.LEFT
    if move == Move.ROTATE_COUNTERCLOCKWISE:
        return Move.ROTATE_CLOCKWISE
    if move == Move.ROTATE_CLOCKWISE:
        return Move.ROTATE_COUNTERCLOCKWISE
    return None

def move_left(position):
    x, y = position
    x -= 1
    return (x, y)

def move_right(position):
    x, y = position
    x += 1
    return (x, y)

def move_down(position):
    x, y = position
    y += 1
    return (x, y) 
