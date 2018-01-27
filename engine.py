#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from random import randrange as rand

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 1, 1],
     [1, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 0, 0],
     [1, 1, 1]],
    
    [[0, 0, 1],
     [1, 1, 1]],
    
    [[1, 1, 1, 1]],
    
    [[1, 1],
     [1, 1]]
]

def get_origin(piece, columns):
    x = int(columns / 2 - len(piece[0])/2)
    y = 0
    return x, y

def get_new_piece():
    return tetris_shapes[rand(len(tetris_shapes))]

def new_game(width, height):
    board = [ [ 0 for x in range(width) ]
            for y in range(height) ]
    board += [[ 1 for x in range(width)]]
    return board, get_new_piece()


def check_collision(board, shape, offset):
    position_x, position_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + position_y ][ cx + position_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    cols = len(board[0])
    del board[row]
    return [[0 for i in range(cols)]] + board


def join_matrices(game_board, piece, position): 
    position_x, position_y = position 
    for y, row in enumerate(piece): 
        for x, val in enumerate(row): 
            game_board[y+position_y-1][x+position_x] += val 
    return game_board

def remove_rows(board):
    cleared_rows = 0
    while True:
        for i, row in enumerate(board[:-1]):
            if 0 not in row:
                board = remove_row(
                  board, i)
                cleared_rows += 1
                break
        else:
            return cleared_rows, board

def play(move, board, piece):
    board = join_matrices(board, piece, move) 
    return board, get_new_piece()

def move_is_legal(game_board, piece, position):
    is_legal = not piece_has_collided(game_board, piece, position) and piece_is_resting(game_board, piece, position) and has_valid_path(game_board, piece, position, get_origin(piece))
    return is_legal

def piece_has_collided(game_board, piece, position):
    position_x, position_y = position 
    for y, row in enumerate(piece): 
        for x, val in enumerate(row): 
            combined_y = y + position_y - 1
            combined_x = x + position_x
            print("game_board.x = ", len(game_board[0]))
            print("combined_x = ", combined_x)
            print("game_board.y = ", len(game_board))
            print("combined_y = ", combined_y)
            if(len(game_board) - 1 <= combined_y):
                return True
            if(len(game_board[0]) - 1 < combined_x):
                return True
            if(game_board[combined_y][combined_x] + val > 1):
                return True
    return False

def piece_is_resting(game_board, piece, position):
    position_x, position_y = position 
    is_resting = False
    for y, row in enumerate(piece): 
        for x, val in enumerate(row): 
            combined_y = y + position_y - 1
            combined_x = x + position_x
            if(val == 1 and game_board[combined_y + 1][combined_x] == 1):
                is_resting = True
    return is_resting

def has_valid_path(game_board, piece, position, origin):
    return True
