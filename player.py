import engine
from random import randint
# scaffold for what it should look like
board_width = 10
board_height = 20
line = "========================================"
def choose_move(game, piece):
    search_tree = []
    for x, row in enumerate(game):
        for y, item in enumerate(row):
            if(engine.move_is_legal(game, piece, (y, x))):
                search_tree.append((y, x))
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
    print("search_tree = ", search_tree)
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
            move, value = choose_move(game, piece)
            if(move == None):
                game_over = True
                continue
            # historical_evaluations.push((move, value))
            print("move = ", move)
            print("game = \n", game_to_string(game))
            print("piece = ", piece)
            game, piece = engine.play(move, game, piece)
            input("hit enter for next move...")
            move_number += 1
        # cnn.train(game.score, historical_evaluations)
        iteration += 1

def game_to_string(game):
    result = line + '\n'
    for row in game:
        result += str(row).replace('0', '  ').replace(',', ' ').replace('1', '<>') + '\n'
    result += line
    return result

main() 
