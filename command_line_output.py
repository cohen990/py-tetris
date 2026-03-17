RESET = '\033[0m'

# ANSI colors matching standard Tetris piece colors
COLORS = {
    1: '\033[95m',        # T - bright magenta
    2: '\033[92m',        # S - bright green
    3: '\033[91m',        # Z - bright red
    4: '\033[94m',        # J - bright blue
    5: '\033[38;5;208m',  # L - orange
    6: '\033[96m',        # I - bright cyan
    7: '\033[93m',        # O - bright yellow
    8: '\033[90m',        # Wall - dark gray
}

BLOCK = '██'
EMPTY = '  '
BORDER_COLOR = '\033[37m'

cols = 10
top_border = BORDER_COLOR + '╔' + '══' * cols + '╗' + RESET
bottom_border = BORDER_COLOR + '╚' + '══' * cols + '╝' + RESET


def colored_cell(value):
    if value == 0:
        return EMPTY
    color = COLORS.get(value, '\033[97m')
    return color + BLOCK + RESET


def plain_cell(value):
    return EMPTY if value == 0 else '<>'


def render_row_colored(row):
    return BORDER_COLOR + '║' + RESET + ''.join(colored_cell(cell) for cell in row) + BORDER_COLOR + '║' + RESET


def render_row_plain(row):
    return '[' + ''.join(plain_cell(cell) for cell in row) + ']'


def print_game(name, game):
    rows = game[:-1]
    output = top_border + '\n'
    for row in rows:
        output += render_row_colored(row) + '\n'
    output += bottom_border
    print(name + ':\n' + output)


def game_to_plain_string(game):
    rows = game[:-1]
    line = '=' * (2 * len(rows[0]) + 2)
    output = line + '\n'
    for row in rows:
        output += render_row_plain(row) + '\n'
    output += line
    return output


def print_piece(piece):
    output = 'piece:\n'
    for row in piece:
        output += ''.join(colored_cell(cell) for cell in row) + '\n'
    print(output)
