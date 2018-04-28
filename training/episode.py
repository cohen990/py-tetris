class Episode:
    def __init__(self):
        self.chapters = []
        self.final_fitness = 0

    def add(self, chapter):
        self.chapters.append(chapter)

    def set_final_fitness(self, final_fitness):
        self.final_fitness = final_fitness

    def unroll(self):
        flattened_chapters = []
        effective_fitnesses = []
        for chapter in self.chapters:
            effective_fitness = self.final_fitness - chapter.calculate_fitness()
            flattened_chapter = chapter.flatten()
            flattened_chapters.append(flattened_chapter)
            effective_fitnesses.append(effective_fitness)
        return flattened_chapters, effective_fitnesses
