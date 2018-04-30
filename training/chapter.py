class Chapter:
    def __init__(self, game, number_of_moves, score):
        self.game = game
        self.number_of_moves = number_of_moves
        self.score = score

    def calculate_fitness(self):
        return float(self.score * 100 + self.number_of_moves)/float(self.calculate_height())

    def flatten(self):
        return self.game.flatten()

    def calculate_height(self):
        for index, row in enumerate(self.game.board_without_bottom_row()):
            if all(column == 0 for column in row):
                continue
            return 20 - index
        return 1
