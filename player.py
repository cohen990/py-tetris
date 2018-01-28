import command_line_output as clo
import engine
import evaluator as ev

from copy import deepcopy
from random import randint
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
    best_move = None
    best_value = 0
    for move in search_tree:
        x, y, piece = move
        resultant_board = engine.join_matrices(game, piece, (x, y))
        value = evaluator.evaluate(resultant_board)
        if best_value < value:
            best_value = value
            best_move = move

    return best_move, best_value

def main():
    iteration = 1
    while(True):
        print("Iteration ", iteration)
        move_number = 1
        game, piece = engine.new_game(board_width, board_height)
        game_over = False
        points = 0
        while(not game_over):
            points = 0
            print("MOVE NUMBER ", move_number)
            clo.print_game("game", game)
            move, value = choose_move(game, piece)
            if(move == None):
                game_over = True
                continue
            print("Evaluated at " + str(value) + " points!")
            rows_cleared, game, piece = engine.play(move, game)
            evaluator.save_selected_evaluation(game, value)
            points += rows_cleared ** 2
            if rows_cleared > 0:
                print("gained " + str(points_gained) + " point[s]!")
            #input("hit enter for next move...")
            move_number += 1
        print("Total score: ", points)
        evaluator.train(points)
        iteration += 1

main() 
