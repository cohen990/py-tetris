import numpy as np


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
            flattened_chapters, effective_fitnesses = episode.unroll()
            x_batch.extend(flattened_chapters)
            y_batch.extend(effective_fitnesses)
        x_batch = np.array(x_batch)
        y_batch = np.array(y_batch)
        return x_batch, y_batch
