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

    def train(self, final_fitness):
        original_input_to_hidden = deepcopy(self.input_to_hidden)
        original_hidden_to_output = deepcopy(self.hidden_to_output)
        original_hidden_biases = deepcopy(self.hidden_biases)
        original_output_bias = deepcopy(self.output_bias)
        for evaluation in self.current_iteration_evaluations:
            inputs = get_inputs_from_board(evaluation[0])
            log.write_game("Training against game", np.array(inputs).reshape((20, 10)))
            value = evaluation[1]
            score_so_far = evaluation[2]
            moves_so_far = evaluation[3]
            fitness_so_far = self.calculate_fitness(score_so_far, moves_so_far)
            log.write("Evaluation at the time: " + str(value))
            log.write("Actual value: " + str(final_fitness))
            effective_fitness = final_fitness - fitness_so_far
            hidden_activations = self.forward(inputs, self.input_to_hidden, self.hidden_biases)
            error = self.error_function(value, effective_fitness)
            self.input_to_hidden = self.back_propagate_weights(self.input_to_hidden, effective_fitness, value, inputs, original_input_to_hidden, original_hidden_biases)
            self.hidden_to_output = self.back_propagate_weights(self.hidden_to_output, final_fitness, value, hidden_activations, original_hidden_to_output, original_output_bias)
            self.hidden_biases = self.back_propagate_biases(self.hidden_biases, final_fitness, value, inputs, original_input_to_hidden, original_hidden_biases)
            self.output_bias = self.back_propagate_biases(self.output_bias, final_fitness, value, hidden_activations, original_hidden_to_output, original_output_bias)
        log.write("error = ", error)
        self.current_iteration_evaluations = []

    def forward(self, inputs, weights, biases):
        activate = np.vectorize(self.activation)
        activations = np.dot(inputs, weights)
        return(activate(activations, np.transpose(biases)))

    def activation(self, activatee, bias):
        raw_activation = activatee + bias
        if raw_activation <= 0:
            return -0.1 * raw_activation
        if raw_activation <= -1:
            return -1.0/raw_activation
        return raw_activation

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

    def save_selected_evaluation(self, board, value, moves_so_far, score_so_far):
        self.current_iteration_evaluations.append((board, value, moves_so_far, score_so_far))

    def error_function(self, results, desired_result):
        error = 0.5*np.sum(np.subtract(results, desired_result)**2)
        return error

    def error_derivative_with_respect_to_output(self, computed_output, desired_output):
        return np.subtract(computed_output, desired_output)

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

    def calculate_fitness(self, score, moves):
        return score * 1000 + moves

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
    expected_output = np.array([-3, -2])
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
    expected = np.array([[-91], [-8]])
    result = evaluator.back_propagate_weights(weights_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected)

@test
def back_propagate_weights_with_multiple_outputs_test():
    evaluator = new_evaluator(2, 2, 1)
    activations = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    weights_to_add_to = np.array([[-1, 14], [-7, 11]])
    biases = np.array([-7, 8])
    desired_result = np.array([1, 9])
    computed_result = np.array([2, 13])
    expected_result = np.array([[-1, 10], [-7, 3]])
    result = evaluator.back_propagate_weights(weights_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_equal(result, expected_result)

@test
def back_propagate_biases_test():
    evaluator = new_evaluator(2, 2, 0.1)
    activations = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    biases = np.array([-7, 8])
    biases_to_add_to = np.array([1, 1])
    desired_result = np.array([9, 11])
    computed_result = np.array([15, 20])
    expected_output = np.array([1, 0.1])
    result = evaluator.back_propagate_biases(biases_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_close(result, expected_output)

def train_test():
    evaluator = new_evaluator(2, 2, 0.1)
    evaluator.input_to_hidden = np.array([[-0.9, -1.1], [-0.7, 0.1]])
    evaluator.hidden_to_output = np.array([[-0.6], [0.8]])
    evaluator.hidden_biases = np.array([[0.8], [0.6]])
    evaluator.output_bias = np.array([[1.1]])
    first_inputs = [0, 1]
    first_evaluation = 1.6
    first_actual_fitness = 30
    second_inputs = [1, 0]
    second_evaluation = 5
    second_actual_fitness = 60
