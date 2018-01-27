line = "========================================"
block = '<>'

def print_game(name, game):
    game_as_string = line + '\n'
    for row in game:
        game_as_string += convert_array_to_blocks(row) + '\n'
    game_as_string += line
    message = name + " = \n"
    print(message, game_as_string)

def print_piece(piece):
    piece_as_string = ""
    for row in piece:
        piece_as_string += remove_square_brackets(convert_array_to_blocks(row)) + '\n'
    print("piece = \n", piece_as_string)

def convert_array_to_blocks(array):
    return str(array).replace('0', '  ').replace(',', ' ').replace('1', block)

def remove_square_brackets(input_string):
    return input_string.strip('[]')
