#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from random import randrange as rand
import sys
import engine
import ui
from ui import Ui

# The configuration
cell_size =    18
cols =        10
rows =        22
maxfps =     30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

class TetrisApp(object):
    def __init__(self):
        Ui.initialise(self)
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(cols)] for y in range(rows)]
        self.screen = Ui.get_screen(self.width, self.height)
        self.next_stone = engine.get_new_piece()
        self.init_game()
    
    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = engine.get_new_piece()
        x, y = engine.get_origin(self.stone, cols)
        self.stone_x = x
        self.stone_y = y
        
        if engine.check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True
    
    def init_game(self):
        self.board, _ = engine.new_game(cols, rows)
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        Ui.set_timer(1000)
    
    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14
    
    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))
        
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
        
            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))
    
    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    Ui.draw(self.screen, colors[val], off_x + x, off_y + y, cell_size)
    
    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            Ui.set_timer(newdelay)
    
    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not engine.check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x
    def quit(self):
        self.center_msg("Exiting...")
        Ui.update()
        sys.exit()
    
    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if engine.check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = engine.join_matrices(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows, self.board = engine.remove_rows(self.board)
                self.add_cl_lines(cleared_rows)
                return True
        return False
    
    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass
    
    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not engine.check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False
    
    def run(self):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        lambda:self.drop(True),
            'UP':        self.rotate_stone,
            'p':        self.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':    self.insta_drop
        }
        
        self.gameover = False
        self.paused = False
        
        dont_burn_my_cpu = Ui.get_clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:
                self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.score)
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    Ui.draw_line(self.screen, self.rlim+1, self.height-1)
                    self.disp_msg("Next:", (
                        self.rlim+cell_size,
                        2))
                    self.disp_msg("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.stone,
                        (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone,
                        (cols+1,2))
            Ui.update() 

            for event in Ui.get_events():
                if Ui.is_user_event(event):
                    self.drop(False)
                elif Ui.is_quit_event(event):
                    self.quit()
                elif Ui.is_keydown_event(event):
                    for key in key_actions:
                        if Ui.is_correct_key(event, key):
                            key_actions[key]()
                    
            dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
    App = TetrisApp()
    App.run()
