# scaffold for what it should look like

# fn choose_move:
    # engine.get_board
    # engine.get_current_piece

    # search_tree = new search_tree()
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
    # return (best_move, value)

# def evaluate(board):
#   cnn_input = board.flatten
#   cnn.evaluate(cnn_input)

# def main():
#   while(true):
    #   game = engine.start_game()
    #   while(game.not_over):
    #       move, value = choose_move()
    #       historical_evaluations.push((move, value))
    #       game = engine.play(move)
    #   cnn.train(game.score, historical_evaluations)

