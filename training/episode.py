class Episode:
    def __init__(self):
        self.chapters = []
        self.final_fitness = 0

    def add(self, chapter):
        self.chapters.append(chapter)

    def set_final_fitness(self, final_fitness):
        self.final_fitness = final_fitness

    def unroll(self, discount=0.95):
        flattened_chapters = []
        effective_fitnesses = []
        total_chapters = len(self.chapters)
        for index, chapter in enumerate(self.chapters):
            steps_from_end = total_chapters - 1 - index
            effective_fitness = self.final_fitness - chapter.calculate_fitness()
            effective_fitness = chapter.attenuate_fitness(effective_fitness)
            effective_fitness *= discount ** steps_from_end
            flattened_chapter = chapter.flatten()
            flattened_chapters.append(flattened_chapter)
            effective_fitnesses.append(effective_fitness)
        return flattened_chapters, effective_fitnesses
