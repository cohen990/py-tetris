#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from random import randrange as rand

tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]

def get_new_piece():
    return tetris_shapes[rand(len(tetris_shapes))]

def new_game(width, height):
	board = [ [ 0 for x in range(width) ]
			for y in range(height) ]
	board += [[ 1 for x in range(width)]]
	return board, get_new_piece()


def check_collision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[ cy + off_y ][ cx + off_x ]:
					return True
			except IndexError:
				return True
	return False

def remove_row(board, row):
	cols = len(board[0])
	del board[row]
	return [[0 for i in range(cols)]] + board


def join_matrices(mat1, mat2, mat2_off): 
	off_x, off_y = mat2_off 
	for cy, row in enumerate(mat2): 
		for cx, val in enumerate(row): 
			mat1[cy+off_y-1	][cx+off_x] += val 
	return mat1

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
def play(move, board):
    return board, get_new_piece()

