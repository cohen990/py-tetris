import command_line_output as clo

import numpy as np
import random

class Evaluator(object):
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.input_to_hidden = initialize_weights(input_size, hidden_size)
        self.hidden_to_output = initialize_weights(hidden_size, 1)
        self.hidden_biases = initialize_biases(hidden_size)
        self.output_bias = initialize_biases(1)

    def evaluate(self, board_state):
        cleaned = board_state[:-1]
        inputs = np.array(cleaned).flatten()
        hidden = self.forward(inputs, self.input_to_hidden, self.hidden_biases)
        output = self.forward(hidden, self.hidden_to_output, self.output_bias) 
        return output

    def train(self, final_score):
        #no op
        return

    def forward(self, inputs, weights, biases):
        activate = np.vectorize(self.activation)
        activations = np.dot(inputs, weights)
        return(activate(activations, np.transpose(biases)))

    def activation(self, activatee, bias):
        if activatee <= 0:
            return bias
        return activatee + bias

def initialize_weights(dimension_1, dimension_2):
    return np.random.rand(dimension_1, dimension_2)

def initialize_biases(size):
    return np.random.rand(size,1)

def new_evaluator(input_size, hidden_size):
    return Evaluator(input_size, hidden_size)
