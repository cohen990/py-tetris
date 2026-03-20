import numpy as np


class Episodes:
    def __init__(self):
        self.episodes = []

    def add(self, episode):
        self.episodes.append(episode)
        if len(self.episodes) > 200:
            self.episodes.sort(key=lambda e: e.final_fitness)
            self.episodes = self.episodes[len(self.episodes) - 200:]

    def unroll(self):
        all_boards = []
        all_contexts = []
        all_fitnesses = []
        for episode in self.episodes:
            boards, contexts, fitnesses = episode.unroll()
            all_boards.extend(boards)
            all_contexts.extend(contexts)
            all_fitnesses.extend(fitnesses)
        return np.array(all_boards), np.array(all_contexts), np.array(all_fitnesses)
