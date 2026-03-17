import os

import keras
import numpy
from keras import Sequential
from keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense

import hybrid_output as log
from training.data import prepare_training_sets



class NeuralNetwork:
    def __init__(self):
        self.model = Sequential()
        self.prepare_network()

    def load_weights_if_they_exist(self):
        if os.path.exists("weights.keras"):
            self.model = keras.models.load_model("weights.keras")

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
        self.model.compile(loss='mse',
                           optimizer='RMSProp')
        self.load_weights_if_they_exist()

    def train(self, episodes):
        x_batch, y_batch = episodes.unroll()
        log.debug("Doing training against " + str(len(x_batch)) + " items.")
        x_train, y_train, x_test, y_test = prepare_training_sets(x_batch, y_batch)
        training_result = self.model.fit(x_train, y_train, epochs=5)
        log.out("error = ", training_result.history["loss"][0])
        network_evaluation = self.model.evaluate(x_test, y_test)
        log.out("evaluation error = ", network_evaluation)
        self.model.save("weights.keras")

    def evaluate(self, game):
        activations = game.flatten()
        activations = numpy.expand_dims(activations, axis=0)
        prediction = self.model.predict(activations, verbose=0)
        return prediction
