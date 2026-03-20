import argparse
import time
import hybrid_output as log
import engine
from evaluator import Evaluator


import random
import numpy as np

from training.chapter import Chapter


parser = argparse.ArgumentParser()
parser.add_argument('--quiet', action='store_true', help='Suppress game output (keeps epoch/score output)')
args = parser.parse_args()
log.quiet = args.quiet

evaluator = Evaluator()


def choose_move(game, piece, score, move_number):
    rotations = [0, 1, 2, 3]
    search_tree = []
    for y_coordinate, row in enumerate(game.board):
        for x_coordinate, item in enumerate(row):
            for rotation in rotations:
                rotated_piece = engine.rotate(piece, rotation)
                candidate_move = x_coordinate, y_coordinate, rotated_piece
                if engine.move_is_legal(game, candidate_move):
                    search_tree.append(candidate_move)
    if len(search_tree) == 0:
        return None, None

    boards = []
    for move in search_tree:
        x, y, piece = move
        game_copy = game.copy()
        game_copy.apply_move(piece, (x, y))
        boards.append(game_copy.flatten())
    boards_batch = np.array(boards)
    contexts_batch = np.array([[score, move_number]] * len(boards))
    values = evaluator.target_network.model.predict(
        [boards_batch, contexts_batch], verbose=0).flatten().tolist()
    max_value = max(values)
    if len(values) > 0:
        if random.random() > 0.95:
            log.debug("Exploring a random option")
            max_value = random.choice(values)
    move_valuations = list(filter(lambda move_value: move_value[1] == max_value, list(zip(search_tree, values))))
    return random.choice(move_valuations)


def main():
    iteration = 1
    epoch_start = time.time()
    while True:
        log.out("Iteration ", iteration)
        move_number = 0
        game, piece = engine.new_game()
        game_over = False
        points = 0
        while not game_over:
            move_number += 1
            move, value = choose_move(game, piece, points, move_number)
            if move is None:
                log.debug("game over")
                game_over = True
                continue
            log.debug("MOVE NUMBER ", move_number)
            log.debug("Evaluated at " + str(value) + " fitness")
            game, piece = engine.play(move, game)
            log.debug_game("game", game)
            chapter = Chapter(game.copy(), move_number, points)
            evaluator.save_selected_evaluation(chapter)
            rows_cleared, game.board = engine.remove_rows(game.board)
            points_gained = rows_cleared ** 2
            points += points_gained
            if points_gained > 0:
                log.debug("gained " + str(points_gained) + " point[s]!")
            log.debug("total points: ", points)
        chapter = Chapter(game.copy(), move_number, points)
        evaluator.save_selected_evaluation(chapter)
        log.out("Total score: ", points)
        actual_fitness = chapter.calculate_fitness()
        log.out("Actual fitness: ", actual_fitness)
        evaluator.complete_episode(actual_fitness)
        if iteration % 50 == 0:
            epoch_elapsed = time.time() - epoch_start
            log.out("Epoch completed in {:.1f}s".format(epoch_elapsed))
            evaluator.train()
            epoch_start = time.time()
        iteration += 1


main()
