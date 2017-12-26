#!/usr/bin/env python2
#-*- coding: utf-8 -*-

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
	del board[row]
	return [[0 for i in range(cols)]] + board


def join_matrixes(mat1, mat2, mat2_off): 
	off_x, off_y = mat2_off 
	for cy, row in enumerate(mat2): 
		for cx, val in enumerate(row): 
			mat1[cy+off_y-1	][cx+off_x] += val 
	return mat1
