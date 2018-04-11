class Episode:
    def __init__(self):
        self.chapters = []
        self.final_fitness = 0

    def add(self, chapter):
        self.chapters.append(chapter)

    def set_final_fitness(self, final_fitness):
        self.final_fitness = final_fitness
