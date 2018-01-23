import engine
# scaffold for what it should look like
board_width = 10
board_height = 20

def choose_move(game):
    search_tree = []
    print(game)
    for x, row in enumerate(game):
        for y, item in enumerate(row):
            search_tree.append((x, y))
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
    best_move = search_tree[5]
    value = 15
    return (best_move, value)

# def evaluate(board):
#   cnn_input = board.flatten
#   cnn.evaluate(cnn_input)

def main():
    while(True):
       game, piece = engine.new_game(board_width, board_height)
       game_over = False
       while(not game_over):
           move, value = choose_move(game)
    #       historical_evaluations.push((move, value))
           game, piece = engine.play(move, game)
    #   cnn.train(game.score, historical_evaluations)

main() 
