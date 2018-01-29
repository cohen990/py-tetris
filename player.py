import hybrid_output as log
import engine
import evaluator as ev

from copy import deepcopy
import random 
board_width = 10
board_height = 20

evaluator = ev.new_evaluator(board_width * board_height, 50)

def choose_move(game, piece):
    rotations = [0, 1, 2, 3]
    search_tree = []
    for y_coordinate, row in enumerate(game):
        for x_coordinate, item in enumerate(row):
            for rotation in rotations:
                rotated_piece = engine.rotate(piece, rotation)
                candidate = x_coordinate, y_coordinate, rotated_piece
                if(engine.move_is_legal(game, candidate)):
                    search_tree.append(candidate)
    if len(search_tree) == 0:
        return None, None

    values = []
    for move in search_tree:
        x, y, piece = move
        resultant_board = engine.join_matrices(game, piece, (x, y))
        value = evaluator.evaluate(resultant_board)
        values.append(value)
    max_value = max(values)
    move_valuations = list(filter(lambda move_value: move_value[1] == max_value, list(zip(search_tree, values))))
    return random.choice(move_valuations)

def main():
    iteration = 1
    while(True):
        log.write("Iteration ", iteration)
        move_number = 1
        game, piece = engine.new_game(board_width, board_height)
        game_over = False
        points = 0
        while(not game_over):
            points = 0
            log.write("MOVE NUMBER ", move_number)
            log.write_game("game", game)
            move, value = choose_move(game, piece)
            if(move == None):
                log.write("game over")
                game_over = True
                continue
            log.write("Evaluated at " + str(value) + " points!")
            rows_cleared, game, piece = engine.play(move, game)
            evaluator.save_selected_evaluation(game, value)
            points_gained = rows_cleared ** 2
            points += points_gained
            if rows_cleared > 0:
                log.write("gained " + str(points_gained) + " point[s]!")
            #input("hit enter for next move...")
            move_number += 1
        log.write("Total score: ", points)
        evaluator.train(points)
        iteration += 1

main() 
