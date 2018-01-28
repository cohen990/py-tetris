import command_line_output as clo

import numpy as np
import random
import sys

class Evaluator(object):
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.input_to_hidden = initialize_weights(input_size, hidden_size)
        self.hidden_to_output = initialize_weights(hidden_size, 1)
        self.hidden_biases = initialize_biases(hidden_size)
        self.output_bias = initialize_biases(1)
        self.current_iteration_evaluations = []
        self.training_rate = 0.01

    def evaluate(self, board_state):
        inputs = get_inputs_from_board(board_state)
        hidden = self.forward(inputs, self.input_to_hidden, self.hidden_biases)
        output = self.forward(hidden, self.hidden_to_output, self.output_bias) 
        return output[0][0]

    def train(self, final_score):
        print("final score: ", final_score)
        unzipped = list(zip(*self.current_iteration_evaluations))
        inputs = get_inputs(unzipped[0])
        evaluations = unzipped[1]
        hidden_activations = self.forward(inputs[0], self.input_to_hidden, self.hidden_biases)
        error = self.error_function(evaluations, final_score)
        self.input_to_hidden = self.back_propagate(final_score, evaluations, inputs[0], self.input_to_hidden, self.hidden_biases)
        self.hidden_to_output = self.back_propagate(final_score, evaluations, hidden_activations, self.hidden_to_output, self.output_bias)
        print("error = ", error)
        return

    def forward(self, inputs, weights, biases):
        activate = np.vectorize(self.activation)
        activations = np.dot(inputs, weights)
        return(activate(activations, np.transpose(biases)))

    def activation(self, activatee, bias):
        if activatee + bias <= 0:
            return 0
        return activatee + bias

    def activation_derivative_with_respect_to_bias(self, inputs, weights, biases):
        activations = np.add(np.dot(inputs, weights),  np.transpose(biases))
        return np.maximum(np.divide(activations, np.absolute(activations)), 0)

    def activation_derivative_with_respect_to_weight(self, inputs, weights, biases):
        activations = np.add(np.dot(inputs, weights),  np.transpose(biases))
        return np.maximum(np.multiply(np.divide(activations, np.absolute(activations)), inputs), 0)

    def save_selected_evaluation(self, board, value):
        self.current_iteration_evaluations.append((board, value))

    def error_function(self, results, desired_result):
        print("results = ", results)
        print("desired results = ", desired_result)
        error = (1.0/(2*len(results)))*np.sum(np.subtract(results, desired_result)**2)
        return error

    def error_derivative_with_respect_to_output(self, computed_output, desired_output):
        return (1.0/len(computed_output)) * np.sum(np.subtract(computed_output, desired_output))

    def error_derivative_with_respect_to_weights(self, desired_result, computed_result, activations, weights, biases):
        dedy = self.error_derivative_with_respect_to_output(computed_result, desired_result) 
        print("dedy = ", dedy)
        dydw = self.activation_derivative_with_respect_to_weight(activations, weights, biases)
        print("dydw = ", dydw)
        return np.multiply(dedy, dydw)

    def error_derivative_with_respect_to_biases(self, activation, intended_result):
        dedy = self.error_derivative_with_respect_to_output(computed_result, desired_result) 
        dydb = self.activation_derivative_with_respect_to_bias(activations, weights, biases)
        return np.multiply(dedy, dydw)

    def back_propagate(self, desired_result, computed_result, activations, weights, biases):
        print("======back propping=======")
        print("activations: ", activations)
        print("original_weights: ", weights)
        dedw = self.error_derivative_with_respect_to_weights(desired_result, computed_result, activations, weights, biases)
        print("dedw = ", dedw)
        result = weights - np.multiply(self.training_rate, dedw) 
        print("new weights: ", result)
        #sys.exit()
        return result

def initialize_weights(dimension_1, dimension_2):
    return np.random.rand(dimension_1, dimension_2)

def initialize_biases(size):
    return np.random.rand(size,1)

def get_inputs_from_board(board_state):
    cleaned = board_state[:-1]
    inputs = np.array(cleaned).flatten()
    return inputs

def get_inputs(board_states):
    result = []
    for board_state in board_states:
        result.append(get_inputs_from_board(board_state))
    return result

def new_evaluator(input_size, hidden_size):
    return Evaluator(input_size, hidden_size)

def test():
    forward_test()
    activation_derivative_with_respect_to_bias_test()
    activation_derivative_with_respect_to_weight_test()

def forward_test():
    evaluator = new_evaluator(2, 2)
    inputs = [1, 2]
    input_to_hidden = [[3, 4], [5, 6]]
    hidden_biases = [7, 8]
    expected_output = [20, 24]
    result = evaluator.forward(inputs, input_to_hidden, hidden_biases)
    print("forward given known input, returns expected output:", np.array_equal(result, expected_output))

def activation_derivative_with_respect_to_bias_test():
    evaluator = new_evaluator(2, 2)
    inputs = [1, 2]
    weights = [[-3, 4], [5, -6]]
    biases = [7, -8]
    expected_output = [1, 0]
    result = evaluator.activation_derivative_with_respect_to_bias(inputs, weights, biases)
    print("dfdb returns expected output:", np.array_equal(result, expected_output))

def activation_derivative_with_respect_to_weight_test():
    evaluator = new_evaluator(2, 2)
    inputs = [1, 2]
    weights = [[-3, 4], [-5, 6]]
    biases = [-7, 8]
    expected_output = [0, 2]
    result = evaluator.activation_derivative_with_respect_to_weight(inputs, weights, biases)
    print("dfdw returns expected output:", np.array_equal(result, expected_output))

test()
