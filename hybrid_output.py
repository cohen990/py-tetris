import os
import uuid

line = "========================================"
block = '<>'

output_directory = "out"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

logging_id = str(uuid.uuid4())
os.makedirs(output_directory + "/" + logging_id)
def open_debug():
    return open(output_directory + "/" + logging_id + "/debug.txt", 'a')
def open_log():
    return open(output_directory + "/" + logging_id + "/out.txt", 'a')

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
    print(message, target_object)

def out(message, target_object = ""):
    _write(message, target_object, output)
    _write(message, target_object, debug_output)
    print(message, target_object)

def _write(message, target_object, log_file):
    log_message = message + str(target_object) + "\n"
    log_file.write(log_message)
    log_file.flush()

def convert_array_to_blocks(array):
    return str(array).replace('0', '  ').replace(',', ' ').replace('1', block)

def remove_square_brackets(input_string):
    return input_string.strip('[]')
