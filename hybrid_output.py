import os
line = "========================================"
block = '<>'

if os.path.isfile("debug.txt"):
    os.remove("debug.txt")
def open_debug():
    return open("debug.txt", 'a')
if os.path.isfile("out.txt"):
    os.remove("out.txt")
def open_log():
    return open("out.txt", 'a')
output = open_log()
debug_output = open_debug()

def write_game(name, game, debug = True):
    game_as_string = line + '\n'
    for row in game:
        game_as_string += convert_array_to_blocks(row) + '\n'
    game_as_string += line
    message = name + " = \n"
    log_message = message + game_as_string + "\n"
    debug_output.write(log_message)
    if not debug:
        output.write(log_message)
    print(message, game_as_string)
    output.flush()

def write_piece(piece, debug = True):
    piece_as_string = ""
    for row in piece:
        piece_as_string += remove_square_brackets(convert_array_to_blocks(row)) + '\n'
    piece_message = "piece = \n"
    log_message = piece_message + piece_as_string + "\n"
    debug_output.write(log_message)
    if not debug:
        output.write(log_message)
    print(piece_message + piece_as_string)
    output.flush()

def write(message, target_object = "", debug = True):
    log_message = message + str(target_object) + "\n"
    debug_output.write(log_message)
    if not debug:
        output.write(log_message)
    print(message, target_object)
    output.flush()

def convert_array_to_blocks(array):
    return str(array).replace('0', '  ').replace(',', ' ').replace('1', block)

def remove_square_brackets(input_string):
    return input_string.strip('[]')
