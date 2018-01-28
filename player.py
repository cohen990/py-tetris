import command_line_output
import engine
import evaluator

from copy import deepcopy
from random import randint
board_width = 10
board_height = 20

def choose_move(game, piece):
    command_line_output.print_game("choosing move for:", game)
    command_line_output.print_piece(piece)
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

    print("search_tree size = ", len(search_tree))
    if(len(search_tree) == 0):
        return None, None
    best_move = search_tree[randint(0, len(search_tree) - 1)]
    value = 15
    return best_move, value

def main():
    iteration = 1
    while(True):
        print("Iteration ", iteration)
        move_number = 1
        game, piece = engine.new_game(board_width, board_height)
        game_over = False
        while(not game_over):
            points = 0
            print("MOVE NUMBER ", move_number)
            command_line_output.print_piece(piece)
            command_line_output.print_game("game", game)
            move, value = choose_move(game, piece)
            if(move == None):
                game_over = True
                continue
            print("move = ", move)
            points_gained, game, piece = engine.play(move, game)
            points += points_gained
            if points_gained > 0:
                print("gained " + str(points_gained) + " point[s]!")
            input("hit enter for next move...")
            move_number += 1
        evaluator.train(game.score)
        iteration += 1

main() 
