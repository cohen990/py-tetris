import command_line_output as clo
import random

def evaluate(board_state):
    clo.print_game("evaluating based on :", board_state)
    return random.random()

def train(final_score):
    print("training based on a final score of ", final_score)
    #no op
    return
