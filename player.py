import engine
import command_line_output
import sys
from random import randint
# scaffold for what it should look like
board_width = 10
board_height = 20
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
    # for position on board:
    #    if engine.is_legal_move(board, piece, position):
    #        search_tree.add(position)
    # best_move = null
    # best_value = 0
    # for move in search_tree:
    #   resultant_board = board.apply(move)
    #   value = evaluate(resultant_board)
    #   if best_value < value:
    #       best_value = value
    #       best_move = move
    print("search_tree size = ", len(search_tree))
    if(len(search_tree) == 0):
        return None, None
    best_move = search_tree[randint(0, len(search_tree) - 1)]
    value = 15
    return best_move, value

# def evaluate(board):
#   cnn_input = board.flatten
#   cnn.evaluate(cnn_input)

def main():
    iteration = 1
    while(True):
        print("Iteration ", iteration)
        move_number = 1
        game, piece = engine.new_game(board_width, board_height)
        game_over = False
        while(not game_over):
            print("MOVE NUMBER ", move_number)
            command_line_output.print_piece(piece)
            command_line_output.print_game("game", game)
            move, value = choose_move(game, piece)
            if(move == None):
                game_over = True
                continue
            # historical_evaluations.push((move, value))
            print("move = ", move)
            game, piece = engine.play(move, game)
      #      sys.exit()
            input("hit enter for next move...")
      #      sys.exit()
            move_number += 1
        # cnn.train(game.score, historical_evaluations)
        iteration += 1

main() 
