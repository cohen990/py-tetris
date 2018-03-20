import hybrid_output as log
from test_framework import *

import numpy as np
import random
import sys
from copy import deepcopy
from keras.models import Sequential
from keras.layers import Dense

class Evaluator(object):
    def __init__(self, network_shape, training_rate):
        log.out("Generating a network with shape: ", network_shape)
        self.model = Sequential()
        self.model.add(Dense(units=64, activation='selu', input_dim=200))
        self.model.add(Dense(units=1, activation='selu'))
        self.model.compile(loss='mean_squared_error',
              optimizer='sgd')
        self.current_iteration_evaluations = []

    def evaluate(self, board_state):
        activations = get_inputs_from_board(board_state)
        activations = np.expand_dims(activations, axis=0)
        prediction = self.model.predict(activations)
        return(prediction)

    def train(self, final_fitness):
        x_batch = []
        y_batch = []
        for evaluation in self.current_iteration_evaluations:
            value = evaluation[1]
            score_so_far = evaluation[2]
            moves_so_far = evaluation[3]
            fitness_so_far = self.calculate_fitness(score_so_far, moves_so_far)
            effective_fitness = final_fitness - fitness_so_far
            activations = get_inputs_from_board(evaluation[0])
            x_batch.append(activations)
            y_batch.append(effective_fitness)
        self.model.train_on_batch(np.array(x_batch), np.array(y_batch))
        self.current_iteration_evaluations = []

    def calculate_fitness(self, score, moves):
        return score * 10 + moves

    def save_selected_evaluation(self, board, value, moves_so_far, score_so_far):
        self.current_iteration_evaluations.append((board, value, moves_so_far, score_so_far))

def get_inputs_from_board(board_state):
    cleaned = board_state[:-1]
    inputs = np.array(cleaned).flatten()
    return inputs

def get_inputs(board_states):
    result = []
    for board_state in board_states:
        result.append(get_inputs_from_board(board_state))
    return result

def new_evaluator(network_shape, learning_rate = 0.0001):
    return Evaluator(network_shape, learning_rate)