from training.episode import Episode
from training.episodes import Episodes
from training.neural_network import NeuralNetwork


TARGET_UPDATE_INTERVAL = 5


class Evaluator:
    def __init__(self):
        self.network = NeuralNetwork()
        self.target_network = NeuralNetwork()
        self.current_episode = Episode()
        self.episodes = Episodes()
        self.training_rounds = 0

    def evaluate(self, game):
        return self.target_network.evaluate(game)

    def complete_episode(self, final_fitness):
        self.current_episode.set_final_fitness(final_fitness)
        self.episodes.add(self.current_episode)
        self.current_episode = Episode()

    def train(self):
        self.network.train(self.episodes)
        self.training_rounds += 1
        if self.training_rounds % TARGET_UPDATE_INTERVAL == 0:
            self.target_network.model.set_weights(self.network.model.get_weights())

    def save_selected_evaluation(self, chapter):
        self.current_episode.add(chapter)
