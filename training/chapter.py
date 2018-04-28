class Chapter:
    def __init__(self, game, number_of_moves, score):
        self.game = game
        self.number_of_moves = number_of_moves
        self.score = score

    def calculate_fitness(self):
        return self.score * 100 + self.number_of_moves

    def flatten(self):
        return self.game.flatten()
