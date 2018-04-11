import numpy as np

from game import get_inputs_from_board


class Episodes:
    def __init__(self):
        self.episodes = []

    def add(self, episode):
        self.episodes.append(episode)
        while len(self.episodes) > 1000:
            self.episodes = self.episodes[1:]

    def unroll(self):
        x_batch = []
        y_batch = []
        for episode in self.episodes:
            for chapter in episode.chapters:
                effective_fitness = episode.final_fitness - chapter.calculate_fitness()
                activations = get_inputs_from_board(chapter.board)
                x_batch.append(activations)
                y_batch.append(effective_fitness)
        x_batch = np.array(x_batch)
        y_batch = np.array(y_batch)
        return x_batch, y_batch
