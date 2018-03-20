import hybrid_output as log
from test_framework import *

import numpy as np
import random
import sys
from copy import deepcopy

class Evaluator(object):
    def __init__(self, network_shape, training_rate):
        log.out("Generating a network with shape: ", network_shape)
        self.network_shape = network_shape
        self.weights = []
        for index, _ in enumerate(network_shape[:-1]):
            weights = initialize_weights(network_shape[index], network_shape[index+1])
            self.weights.append(weights)
        self.biases = []
        for index, _ in enumerate(network_shape[:-1]):
            biases = initialize_biases(network_shape[index + 1])[:,0]
            self.biases.append(biases)
        self.current_iteration_evaluations = []
        self.training_rate = training_rate

    def evaluate(self, board_state):
        activations = get_inputs_from_board(board_state)
        for index, _ in enumerate(self.network_shape[:-1]):
            activations = self.forward(activations, self.weights[index], self.biases[index])
        return activations

    def train(self, final_fitness):
        original_weights = deepcopy(self.weights)
        original_biases = deepcopy(self.biases)
        for evaluation in self.current_iteration_evaluations:
            value = evaluation[1]
            score_so_far = evaluation[2]
            moves_so_far = evaluation[3]
            fitness_so_far = self.calculate_fitness(score_so_far, moves_so_far)
            log.debug("Evaluation at the time: " + str(value))
            log.debug("Actual value: " + str(final_fitness))
            effective_fitness = final_fitness - fitness_so_far
            activations = get_inputs_from_board(evaluation[0])
            log.debug(log.game_to_log_message("Training against game", np.array(activations).reshape((20, 10))))
            error = self.back_propagate(effective_fitness, value, activations, original_weights, original_biases)
        log.out("Trained against " + str(len(self.current_iteration_evaluations)) + " evaluations")
        log.out("error = ", error)
        log.debug("Original weights", original_weights)
        log.debug("New weights", self.weights)
        log.debug("Original biases", original_biases)
        log.debug("New biases", self.biases)
        self.current_iteration_evaluations = []

    def back_propagate(self, actual_result, computed_result, activations, original_weights, original_biases):
        for index, _ in enumerate(self.weights):
            log.debug("Training weights with shape " + str(self.weights[index].shape))
            self.weights[index] = self.back_propagate_weights(self.weights[index], actual_result, computed_result, activations, original_weights[index], original_biases[index])
            log.debug("Training biases with size " + str(self.biases[index].shape))
            self.biases[index] = self.back_propagate_biases(self.biases[index], actual_result, computed_result, activations, original_weights[index], original_biases[index])
            activations = self.forward(activations, original_weights[index], original_biases[index])
        error = self.error_function(computed_result, actual_result)
        return error

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
    log.out("Initializing weights with dimensions: " + str(dimension_1) + ", " + str(dimension_2))
    return np.random.randn(dimension_1, dimension_2)

def initialize_biases(size):
    log.out("Initializing biases with size: ", size)
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

def new_evaluator(network_shape, learning_rate = 0.0001):
    return Evaluator(network_shape, learning_rate)

@test
def forward_test():
    evaluator = new_evaluator([2, 2])
    inputs = np.array([1, 2])
    input_to_hidden = np.array([[3, 4], [5, 6]])
    hidden_biases = np.array([7, 8])
    expected_output = np.array([20, 24])
    result = evaluator.forward(inputs, input_to_hidden, hidden_biases)
    assert_arrays_equal(result, expected_output)

@test
def activation_derivative_with_respect_to_bias_test():
    evaluator = new_evaluator([2, 2])
    inputs = np.array([1, 2])
    weights = np.array([[-3, 4], [5, -6]])
    biases = np.array([7, -8])
    expected_output = np.array([1, 0])
    result = evaluator.activation_derivative_with_respect_to_bias(inputs, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def activation_derivative_with_respect_to_weight_with_2x1_weights_test():
    evaluator = new_evaluator([2, 2])
    inputs = np.array([7, 2])
    weights = np.array([[3], [-6]])
    biases = np.array([8])
    expected_output = np.array([[7], [2]])
    result = evaluator.activation_derivative_with_respect_to_weight(inputs, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def activation_derivative_with_respect_to_weight_with_2x2_weights_test():
    evaluator = new_evaluator([2, 2])
    inputs = np.array([1, 2])
    weights = np.array([[-3, 4], [-5, 6]])
    biases = np.array([-7, 8])
    expected_output = np.array([[0, 1], [0, 2]])
    result = evaluator.activation_derivative_with_respect_to_weight(inputs, weights, biases)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_output_test():
    evaluator = new_evaluator([2, 2])
    computed_results = 1
    desired_results = 4
    expected_output = -3
    result = evaluator.error_derivative_with_respect_to_output(computed_results, desired_results)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_output_with_multiple_outputs_test():
    evaluator = new_evaluator([2, 2])
    computed_results = np.array([1, 5])
    desired_results = np.array([4, 7])
    expected_output = np.array([-3, -2])
    result = evaluator.error_derivative_with_respect_to_output(computed_results, desired_results)
    assert_arrays_equal(result, expected_output)

@test
def error_derivative_with_respect_to_weights_test():
    evaluator = new_evaluator([2, 2])
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
    evaluator = new_evaluator([2, 2])
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
    evaluator = new_evaluator([2, 2], 1)
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
    evaluator = new_evaluator([2, 2], 1)
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
    evaluator = new_evaluator([1, 3], 0.1)
    activations = np.array([1])
    weights = np.array([[-3, 4, -5]])
    biases = np.array([6, -7, 8])
    biases_to_add_to = np.array([1, 1, 2])
    desired_result = np.array([9, 10, 11])
    computed_result = np.array([15, 20, 25])
    expected_output = np.array([1, 0.1, 0.4])
    result = evaluator.back_propagate_biases(biases_to_add_to, desired_result, computed_result, activations, weights, biases)
    assert_arrays_close(result, expected_output)

@test
def back_propagate_test():
    evaluator = new_evaluator([1, 1, 1, 1], 0.1)
    activations = np.array([7])
    actual_result = 8
    computed_result = 217
    original_weights = [np.array([[2]]), np.array([[3]]), np.array([[4]])]
    evaluator.weights = [np.array([[1]]), np.array([[1]]), np.array([[1]])]
    original_biases = [np.array([3]), np.array([2]), np.array([5])]
    evaluator.biases = [np.array([1]), np.array([1]), np.array([1])]
    result = evaluator.back_propagate(actual_result, computed_result, activations, original_weights, original_biases)
    print(result)
    print(evaluator.weights)
    print(evaluator.biases)
