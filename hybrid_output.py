import os
import numpy
import uuid
import command_line_output as clo

output_directory = "out"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

logging_id = str(uuid.uuid4())
os.makedirs(output_directory + "/" + logging_id)


def open_debug():
    return open(output_directory + "/" + logging_id + "/debug.txt", 'a')


def open_log():
    return open(output_directory + "/" + logging_id + "/out.txt", 'a')


def open_weights():
    return open(output_directory + "/" + logging_id + "/weights.txt", 'w')


output = open_log()
debug_output = open_debug()

quiet = False


def game_to_log_message(name, game):
    return name + " = \n" + clo.game_to_plain_string(game.board) + "\n"


def game_to_colored_message(name, game):
    rows = game.board[:-1]
    output = clo.top_border + '\n'
    for row in rows:
        output += clo.render_row_colored(row) + '\n'
    output += clo.bottom_border
    return name + ':\n' + output


def debug(message, target_object=""):
    _write(message, target_object, debug_output)
    if not quiet:
        print(message, target_object)


def debug_game(name, game):
    _write(game_to_log_message(name, game), "", debug_output)
    if not quiet:
        print(game_to_colored_message(name, game))


def out(message, target_object=""):
    _write(message, target_object, output)
    _write(message, target_object, debug_output)
    print(message, target_object)


def weights(weights):
    numpy.set_printoptions(threshold=numpy.nan)
    _write("", weights, open_weights())


def _write(message, target_object, log_file):
    log_message = message + str(target_object) + "\n"
    log_file.write(log_message)
    log_file.flush()
