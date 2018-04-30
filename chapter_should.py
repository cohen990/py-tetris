import unittest

import engine
import tetrominos
from game import Game
from training.chapter import Chapter


class ChapterShould(unittest.TestCase):
    def test_have_zero_fitness_when_new(self):
        game = Game()
        chapter = Chapter(game, 0, 0)

        fitness = chapter.calculate_fitness()
        self.assertEqual(0, fitness)

    def test_have_1_fitness_after_1_move(self):
        game = Game()
        chapter = Chapter(game, 1, 0)
        fitness = chapter.calculate_fitness()
        self.assertEqual(1, fitness)

    def test_have_2_fitness_after_2_moves(self):
        game = Game()
        chapter = Chapter(game, 2, 0)
        fitness = chapter.calculate_fitness()
        self.assertEqual(2, fitness)

    def test_have_202_fitness_after_2_moves_with_2_points(self):
        game = Game()
        chapter = Chapter(game, 2, 2)
        fitness = chapter.calculate_fitness()
        self.assertEqual(202, fitness)

    def test_have_41_fitness_after_4_moves_with_2_points_and_line_height_4(self):
        game = Game()
        piece = engine.rotate(tetrominos.I, 1)
        game.apply_move(piece, (1, 17))
        chapter = Chapter(game, 4, 2)
        fitness = chapter.calculate_fitness()
        self.assertEqual(51, fitness)

    def test_calculate_line_height_to_be_four_when_theres_a_standing_I_on_the_bottom(self):
        game = Game()
        piece = engine.rotate(tetrominos.I, 1)
        game.apply_move(piece, (1, 17))
        chapter = Chapter(game, 4, 2)
        height = chapter.calculate_height()
        self.assertEqual(4, height)


if __name__ == '__main__':
    unittest.main()
