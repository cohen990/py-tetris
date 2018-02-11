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

def game_to_log_message(name, game):
    game_as_string = line + '\n'
    for row in game:
        game_as_string += convert_array_to_blocks(row) + '\n'
    game_as_string += line
    message = name + " = \n"
    return message + game_as_string + "\n"

def debug(message, target_object = ""):
    _write(message, target_object, debug_output)

def out(message, target_object = ""):
    _write(message, target_object, output)
    _write(message, target_object, debug_output)

def _write(message, target_object, log_file):
    log_message = message + str(target_object) + "\n"
    log_file.write(log_message)
    log_file.flush()
    print(message, target_object)

def convert_array_to_blocks(array):
    return str(array).replace('0', '  ').replace(',', ' ').replace('1', block)

def remove_square_brackets(input_string):
    return input_string.strip('[]')
