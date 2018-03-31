import hybrid_output as log
import engine
import evaluator as ev

from copy import deepcopy
import random 
board_width = 10
board_height = 20

evaluator = ev.new_evaluator()

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
        value = evaluator.evaluate(resultant_board)[0]
        values.append(value)
    max_value = max(values)
    if len(values) > 0:
        if random.random() > 0.9:
            log.debug("Exploring a random option")
            max_value = random.choice(values)
    move_valuations = list(filter(lambda move_value: move_value[1] == max_value, list(zip(search_tree, values))))
    return random.choice(move_valuations)

def main():
    iteration = 1
    while(True):
        log.out("Iteration ", iteration)
        move_number = 0
        game, piece = engine.new_game(board_width, board_height)
        game_over = False
        points = 0
        while(not game_over):
            move_number += 1
            move, value = choose_move(game, piece)
            if(move == None):
                log.debug("game over") 
                game_over = True
                continue
            log.debug("MOVE NUMBER ", move_number)
            log.debug("Evaluated at " + str(value) + " fitness")
            game, piece = engine.play(move, game)
            log.debug(log.game_to_log_message("game", game))
            evaluator.save_selected_evaluation(deepcopy(game), deepcopy(value), deepcopy(move_number), deepcopy(points))
            rows_cleared, game = engine.remove_rows(game)
            points_gained = rows_cleared ** 2
            points += points_gained
            if points_gained > 0:
                log.debug("gained " + str(points_gained) + " point[s]!")
            log.debug("total points: ", points)
        evaluator.save_selected_evaluation(deepcopy(game), deepcopy(value), deepcopy(move_number), deepcopy(points))
        log.out("Total score: ", points)
        actual_fitness = evaluator.calculate_fitness(points, move_number)
        log.out("Actual fitness: ", actual_fitness)
        evaluator.train(deepcopy(actual_fitness))
        iteration += 1

main() 
