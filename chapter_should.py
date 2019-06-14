import unittest

import engine
import tetrominos
from game import Game
from training.chapter import Chapter


class ChapterShould(unittest.TestCase):

    def test_attenuate_fitness(self):
        game = Game()
        piece = engine.rotate(tetrominos.I, 1)
        game.apply_move(piece, (1, 17))
        chapter = Chapter(game, 2, 2)
        fitness = chapter.attenuate_fitness(204)
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
