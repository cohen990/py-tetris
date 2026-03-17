import engine


LEFT = 1
RIGHT = 2
DOWN = 3
ROTATE_CCW = 4
ROTATE_CW = 5

OPPOSITES = {LEFT: RIGHT, RIGHT: LEFT, ROTATE_CCW: ROTATE_CW, ROTATE_CW: ROTATE_CCW}


def _to_tuple(piece):
    return tuple(tuple(row) for row in piece)


def has_path(game_board, piece, position, target):
    target_x, target_y, target_piece = target
    target_key = (target_x, target_y, _to_tuple(target_piece))

    visited = set()
    stack = [(position, piece, _to_tuple(piece), None)]

    while stack:
        pos, pc, pc_key, last_move = stack.pop()

        state = (pos[0], pos[1], pc_key)
        if state in visited:
            continue
        visited.add(state)

        if state == target_key:
            return True

        for move in (LEFT, RIGHT, DOWN, ROTATE_CCW, ROTATE_CW):
            if move == OPPOSITES.get(last_move):
                continue

            if move == LEFT:
                new_pos = (pos[0] - 1, pos[1])
                new_pc, new_key = pc, pc_key
            elif move == RIGHT:
                new_pos = (pos[0] + 1, pos[1])
                new_pc, new_key = pc, pc_key
            elif move == DOWN:
                new_pos = (pos[0], pos[1] + 1)
                new_pc, new_key = pc, pc_key
            elif move == ROTATE_CCW:
                new_pc = engine.rotate(pc, 3)
                new_key = _to_tuple(new_pc)
                new_pos = pos
            else:
                new_pc = engine.rotate(pc, 1)
                new_key = _to_tuple(new_pc)
                new_pos = pos

            if (new_pos[0], new_pos[1], new_key) not in visited and \
               not engine.piece_has_collided(game_board, new_pc, new_pos):
                stack.append((new_pos, new_pc, new_key, move))

    return False
