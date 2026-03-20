import os

import keras
import numpy
from keras.layers import Input, Conv2D, Activation, MaxPooling2D, Flatten, Dense, Concatenate

import hybrid_output as log
from training.data import prepare_training_sets



class NeuralNetwork:
    def __init__(self):
        self.model = self.build_network()
        self.load_weights_if_they_exist()

    def load_weights_if_they_exist(self):
        if os.path.exists("weights.keras"):
            self.model = keras.models.load_model("weights.keras")

    def build_network(self):
        board_input = Input(shape=(20, 10, 1), name='board')
        context_input = Input(shape=(2,), name='context')

        x = Conv2D(32, 3)(board_input)
        x = Activation('relu')(x)
        x = Conv2D(32, 3)(x)
        x = Activation('relu')(x)
        x = MaxPooling2D(pool_size=2)(x)
        x = Flatten()(x)

        x = Concatenate()([x, context_input])
        x = Dense(units=256, activation='relu')(x)
        x = Dense(units=64, activation='relu')(x)
        output = Dense(units=1, activation='softplus')(x)

        model = keras.Model(inputs=[board_input, context_input], outputs=output)
        model.compile(loss='mean_squared_logarithmic_error', optimizer='RMSProp')
        return model

    def train(self, episodes):
        boards, contexts, y_batch = episodes.unroll()
        log.debug("Doing training against " + str(len(boards)) + " items.")
        x_train_boards, x_train_contexts, y_train, x_test_boards, x_test_contexts, y_test = prepare_training_sets(boards, contexts, y_batch)
        training_result = self.model.fit(
            [x_train_boards, x_train_contexts], y_train, epochs=5)
        log.out("error = ", training_result.history["loss"][0])
        network_evaluation = self.model.evaluate(
            [x_test_boards, x_test_contexts], y_test)
        log.out("evaluation error = ", network_evaluation)
        self.model.save("weights.keras")

    def evaluate(self, game):
        activations = game.flatten()
        activations = numpy.expand_dims(activations, axis=0)
        prediction = self.model.predict(activations, verbose=0)
        return prediction
