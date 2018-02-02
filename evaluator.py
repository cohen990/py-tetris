import hybrid_output as log
from test_framework import *

import numpy as np
import random
import sys
from copy import deepcopy

class Evaluator(object):
    def __init__(self, input_size, hidden_size, training_rate):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.input_to_hidden = initialize_weights(input_size, hidden_size)
        self.hidden_to_output = initialize_weights(hidden_size, 1)
        self.hidden_biases = initialize_biases(hidden_size)
        self.output_bias = initialize_biases(1)
        self.current_iteration_evaluations = []
        self.training_rate = training_rate

    def evaluate(self, board_state):
        inputs = get_inputs_from_board(board_state)
        hidden = self.forward(inputs, self.input_to_hidden, self.hidden_biases)
        output = self.forward(hidden, self.hidden_to_output, self.output_bias) 
        return output[0][0]

    def train(self, final_score):
        original_input_to_hidden = deepcopy(self.input_to_hidden)
        original_hidden_to_output = deepcopy(self.hidden_to_output)
        original_hidden_biases = deepcopy(self.hidden_biases)
        original_output_bias = deepcopy(self.output_bias)
        for evaluation in self.current_iteration_evaluations:
            inputs = get_inputs_from_board(evaluation[0])
            value = evaluation[1]
            hidden_activations = self.forward(inputs, self.input_to_hidden, self.hidden_biases)
            error = self.error_function(value, final_score)
            self.input_to_hidden = self.back_propagate_weights(self.input_to_hidden, final_score, value, inputs, original_input_to_hidden, self.hidden_biases)
            self.hidden_to_output = self.back_propagate_weights(self.hidden_to_output, final_score, value, hidden_activations, original_hidden_to_output, self.output_bias)
            self.hidden_biases = self.back_propagate_biases(self.hidden_biases, final_score, value, inputs, self.input_to_hidden, original_hidden_biases)
            self.output_bias = self.back_propagate_biases(self.output_bias, final_score, value, hidden_activations, self.hidden_to_output, original_output_bias)
        log.write("error = ", error)

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
        normalised = np.clip(activations, 0, 1)
        return np.maximum(normalised, 0)

    def activation_derivative_with_respect_to_weight(self, inputs, weights, biases):
        weighted_inputs = np.transpose(np.dot(inputs, weights))
        activations = np.add(weighted_inputs,  np.transpose(biases))
        rectified = np.clip(activations, 0, 1)
        result = np.outer(inputs, rectified)
        return result

    def save_selected_evaluation(self, board, value):
        self.current_iteration_evaluations.append((board, value))

    def error_function(self, results, desired_result):
        error = 0.5*np.sum(np.subtract(results, desired_result)**2)
        return error

    def error_derivative_with_respect_to_output(self, computed_output, desired_output):
        if not isinstance(computed_output, list):
            computed_output = [computed_output]
            desired_output = [desired_output]
        return (1/len(computed_output)) * np.sum(np.subtract(computed_output, desired_output))

    def error_derivative_with_respect_to_weights(self, desired_result, computed_result, activations, weights, biases):
        dedy = self.error_derivative_with_respect_to_output(computed_result, desired_result) 
        dydw = self.activation_derivative_with_respect_to_weight(activations, weights, biases)
        return np.multiply(dedy, dydw)

    def error_derivative_with_respect_to_biases(self, desired_result, computed_result, activations, weights, biases):
        dedy = self.error_derivative_with_respect_to_output(computed_result, desired_result) 
        dydb = self.activation_derivative_with_respect_to_bias(activations, weights, biases)
        return np.multiply(dedy, dydb)

    def back_propagate_weights(self, weights_to_modify, desired_result, computed_result, activations, weights, biases):
        dedw = self.error_derivative_with_respect_to_weights(desired_result, computed_result, activations, weights, biases)
        result = weights_to_modify - np.transpose(np.multiply(self.training_rate, np.transpose(dedw)))
        return result

    def back_propagate_biases(self, biases_to_modify, desired_result, computed_result, activations, weights, biases):
        dedb = self.error_derivative_with_respect_to_biases(desired_result, computed_result, activations, weights, biases)
        result = biases_to_modify - np.transpose(np.multiply(self.training_rate, dedb))
        return result

def initialize_weights(dimension_1, dimension_2):
    return np.random.randn(dimension_1, dimension_2)

def initialize_biases(size):
    return np.random.randn(size,1)

def get_inputs_from_board(board_state):
    cleaned = board_state[:-1]
    inputs = np.array(cleaned).flatten()
    return inputs

def get_inputs(board_states):
    result = []
    for board_state in board_states:
        result.append(get_inputs_from_board(board_state))
    return result

def new_evaluator(input_size, hidden_size, learning_rate = 0.0001):
    return Evaluator(input_size, hidden_size, learning_rate)

@test
def forward_test():
    evaluator = new_evaluator(2, 2)
    inputs = np.array([1, 2])
    input_to_hidden = np.array([[3, 4], [5, 6]])
    hidden_biases = np.array([7, 8])
    expected_output = np.array([20, 24])
    result = evaluator.forward(inputs, input_to_hidden, hidden_biases)
    assert_arrays_equal(result, expected_output)

@test
def activation_derivative_with_respect_to_bias_test():
    evaluator = new_evaluator(2, 2)
    inputs = np.array([1, 2])
    weights = np.array([[-3, 4], [5, -6]])
    biases = np.array([7, -8])
    expected_output = np.array([1, 0])
    result = evaluator.activation_derivative_with_respect_to_bias(inputs, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def activation_derivative_with_respect_to_weight_with_2x1_weights_test():
    evaluator = new_evaluator(2, 2)
    inputs = np.array([7, 2])
    weights = np.array([[3], [-6]])
    biases = np.array([8])
    expected_output = np.array([[7], [2]])
    result = evaluator.activation_derivative_with_respect_to_weight(inputs, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def activation_derivative_with_respect_to_weight_with_2x2_weights_test():
    evaluator = new_evaluator(2, 2)
    inputs = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    biases = np.array([-7, 8])
    expected_output = np.array([[0, 1], [0, 2]])
    result = evaluator.activation_derivative_with_respect_to_weight(inputs, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_output_test():
    evaluator = new_evaluator(2, 2)
    computed_results = 1
    desired_results = 4
    expected_output = -3
    result = evaluator.error_derivative_with_respect_to_output(computed_results, desired_results)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_output_with_multiple_outputs_test():
    evaluator = new_evaluator(2, 2)
    computed_results = np.array([1, 5])
    desired_results = np.array([4, 7])
    expected_output = -2.5
    result = evaluator.error_derivative_with_respect_to_output(computed_results, desired_results)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_weights_test():
    evaluator = new_evaluator(2, 2)
    activations = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    biases = np.array([-7, 8])
    desired_result = 9
    computed_result = 15
    expected_output = np.array([[0, 6], [0, 12]])
    result = evaluator.error_derivative_with_respect_to_weights(desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_biases_test():
    evaluator = new_evaluator(2, 2)
    activations = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    biases = np.array([-7, 8])
    desired_result = 9
    computed_result = 15
    expected_output = np.array([0, 6])
    result = evaluator.error_derivative_with_respect_to_biases(desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def back_propagate_weights_test():
    evaluator = new_evaluator(2, 2, 1)
    activations = np.array([7, 2])
    weights = np.array([[3],[-6]])
    weights_to_add_to = np.array([[-7], [16]])
    biases = np.array([8])
    desired_result = np.array([1])
    computed_result = np.array([13])
    expected_result = np.array([[-91], [16]])
    result = evaluator.back_propagate_weights(weights_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected_result)

@test
def back_propagate_weights_with_multiple_outputs_test():
    evaluator = new_evaluator(2, 2, 1)
    activations = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    weights_to_add_to = np.array([[-1, 14], [-7, 11]])
    biases = np.array([-7, 8])
    desired_result = np.array([1, 9])
    computed_result = np.array([2, 13])
    expected_result = np.array([[-1, 11.5], [-7, 6]])
    result = evaluator.back_propagate_weights(weights_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected_result)

@test
def back_propagate_biases_test():
    evaluator = new_evaluator(2, 2)
    activations = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    biases = np.array([-7, 8])
    biases_to_add_to = np.array([1, 1])
    desired_result = np.array([9, 11])
    computed_result = np.array([15, 20])
    expected_output = np.array([1, 0.99925])
    result = evaluator.back_propagate_biases(biases_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected_output)
