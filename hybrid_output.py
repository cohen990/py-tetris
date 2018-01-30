import os
line = "========================================"
block = '<>'
if os.path.isfile("out.txt"):
    os.remove("out.txt")
def open_log():
    return open("out.txt", 'a')

def write_game(name, game):
    log = open_log()
    game_as_string = line + '\n'
    for row in game:
        game_as_string += convert_array_to_blocks(row) + '\n'
    game_as_string += line
    message = name + " = \n"
    log.write(message + game_as_string + "\n")
    print(message, game_as_string)
    log.close()

def write_piece(piece):
    log = open_log()
    piece_as_string = ""
    for row in piece:
        piece_as_string += remove_square_brackets(convert_array_to_blocks(row)) + '\n'
    piece_message = "piece = \n"
    log.write(piece_message + piece_as_string + "\n")
    print(piece_message + piece_as_string)
    log.close()

def write(message, target_object = ""):
    log = open_log()
    log.write(message + str(target_object) + "\n")
    print(message, target_object)
    log.close()

def convert_array_to_blocks(array):
    return str(array).replace('0', '  ').replace(',', ' ').replace('1', block)

def remove_square_brackets(input_string):
    return input_string.strip('[]')
