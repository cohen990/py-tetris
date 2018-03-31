import hybrid_output as log
from test_framework import *

import numpy as np
import random
import sys
from copy import deepcopy
from keras.models import Sequential
from keras.layers import Dense

class Evaluator(object):
    def __init__(self, training_rate):
        self.model = Sequential()
        self.model.add(Dense(units=64, activation='relu', input_dim=200))
        self.model.add(Dense(units=64, activation='relu'))
        self.model.add(Dense(units=1, activation='linear'))
        self.model.compile(loss='mean_squared_error',
              optimizer='RMSProp')
        self.current_episode = []
        self.episodes = []

    def evaluate(self, board_state):
        activations = get_inputs_from_board(board_state)
        activations = np.expand_dims(activations, axis=0)
        prediction = self.model.predict(activations)
        return(prediction)

    def train(self, final_fitness):
        self.episodes.append(self.current_episode)
        while len(self.episodes) > 100:
            self.episodes = self.episodes[1:]

        x_batch = []
        y_batch = []
        for episode in self.episodes:
            for evaluation in episode:
                value = evaluation[1]
                score_so_far = evaluation[2]
                moves_so_far = evaluation[3]
                fitness_so_far = self.calculate_fitness(score_so_far, moves_so_far)
                effective_fitness = final_fitness - fitness_so_far
                activations = get_inputs_from_board(evaluation[0])
                x_batch.append(activations)
                y_batch.append(effective_fitness)
        log.debug("Doing training against " + str(len(x_batch)) + " items.")
        x_batch = np.array(x_batch)
        y_batch = np.array(y_batch)
        x_batch, y_batch = self.unison_shuffled_copies(x_batch, y_batch)
        train_length = int(len(x_batch) * 0.8)
        x_train = x_batch[:train_length]
        y_train = y_batch[:train_length]
        x_test = x_batch[train_length:]
        y_test = y_batch[train_length:]
        epoch_size = int(train_length * 0.35)
        history = self.model.fit(x_train, y_train, steps_per_epoch=epoch_size, epochs=2)
        log.out("initial error = ", history.history["loss"][0])
        log.out("final error = ", history.history["loss"][-1])
        network_evaluation = self.model.evaluate(x_test, y_test)
        log.out("evaluation error = ", network_evaluation)
        weights = self.model.get_weights()
        log.weights(weights)
        self.current_episode = []

    def calculate_fitness(self, score, moves):
        return score * 100 + moves

    def save_selected_evaluation(self, board, value, moves_so_far, score_so_far):
        self.current_episode.append((board, value, moves_so_far, score_so_far))

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

def get_inputs_from_board(board_state):
    cleaned = board_state[:-1]
    inputs = np.array(cleaned).flatten()
    return inputs

def get_inputs(board_states):
    result = []
    for board_state in board_states:
        result.append(get_inputs_from_board(board_state))
    return result

def new_evaluator(learning_rate = 0.0001):
    return Evaluator(learning_rate)
