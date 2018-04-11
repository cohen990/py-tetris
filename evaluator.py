import hybrid_output as log
from game import get_inputs_from_board

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Activation, MaxPooling2D, Flatten

from training.episode import Episode
from training.episodes import Episodes


class Evaluator(object):
    def __init__(self):
        self.model = Sequential()
        self.prepare_network()
        self.current_episode = Episode()
        self.episodes = Episodes()

    def prepare_network(self):
        self.model.add(Conv2D(32, 3, input_shape=(20, 10, 1)))
        self.model.add(Activation('relu'))
        self.model.add(Conv2D(32, 3))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=2))
        self.model.add(Flatten())
        self.model.add(Dense(units=256, activation='relu'))
        self.model.add(Dense(units=64, activation='relu'))
        self.model.add(Dense(units=1, activation='linear'))
        self.model.compile(loss='mean_squared_logarithmic_error',
                           optimizer='RMSProp')

    def evaluate(self, board_state):
        activations = get_inputs_from_board(board_state)
        activations = np.expand_dims(activations, axis=0)
        prediction = self.model.predict(activations)
        return prediction

    def train(self, final_fitness):
        self.current_episode.set_final_fitness(final_fitness)
        self.episodes.add(self.current_episode)

        x_batch, y_batch = self.episodes.unroll()
        log.debug("Doing training against " + str(len(x_batch)) + " items.")

        x_train, y_train, x_test, y_test = self.prepare_training_sets(x_batch, y_batch)
        training_result = self.model.fit(x_train, y_train)
        log.out("error = ", training_result.history["loss"][0])
        network_evaluation = self.model.evaluate(x_test, y_test)
        log.out("evaluation error = ", network_evaluation)
        self.current_episode = Episode()

    def prepare_training_sets(self, x_batch, y_batch):
        x_batch, y_batch = self.unison_shuffled_copies(x_batch, y_batch)
        train_length = int(len(x_batch) * 0.8)
        x_train = x_batch[:train_length]
        y_train = y_batch[:train_length]
        x_test = x_batch[train_length:]
        y_test = y_batch[train_length:]
        return x_train, y_train, x_test, y_test

    def save_selected_evaluation(self, chapter):
        self.current_episode.add(chapter)

    @staticmethod
    def unison_shuffled_copies(a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]


def get_inputs(board_states):
    result = []
    for board_state in board_states:
        result.append(get_inputs_from_board(board_state))
    return result
