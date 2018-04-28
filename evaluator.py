from training.episode import Episode
from training.episodes import Episodes
from training.neural_network import NeuralNetwork


class Evaluator:
    def __init__(self):
        self.network = NeuralNetwork()
        self.current_episode = Episode()
        self.episodes = Episodes()

    def evaluate(self, game):
        return self.network.evaluate(game)

    def complete_episode(self, final_fitness):
        self.current_episode.set_final_fitness(final_fitness)
        self.episodes.add(self.current_episode)
        self.current_episode = Episode()

    def train(self):
        self.network.train(self.episodes)

    def save_selected_evaluation(self, chapter):
        self.current_episode.add(chapter)
