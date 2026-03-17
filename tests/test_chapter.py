from game import Game
from training.chapter import Chapter


def test_calculate_fitness():
    game = Game()
    chapter = Chapter(game, number_of_moves=10, score=3)
    assert chapter.calculate_fitness() == 310


def test_calculate_fitness_zero_score():
    game = Game()
    chapter = Chapter(game, number_of_moves=5, score=0)
    assert chapter.calculate_fitness() == 5


def test_calculate_height_empty_board():
    game = Game()
    chapter = Chapter(game, number_of_moves=1, score=0)
    assert chapter.calculate_height() == 1


def test_calculate_height_with_blocks():
    game = Game()
    game.board[15][0] = 1
    chapter = Chapter(game, number_of_moves=1, score=0)
    assert chapter.calculate_height() == 5


def test_calculate_height_top_row():
    game = Game()
    game.board[0][0] = 1
    chapter = Chapter(game, number_of_moves=1, score=0)
    assert chapter.calculate_height() == 20


def test_attenuate_fitness():
    game = Game()
    game.board[15][0] = 1
    chapter = Chapter(game, number_of_moves=1, score=0)
    height = chapter.calculate_height()
    assert height == 5
    assert chapter.attenuate_fitness(100) == 20.0


def test_flatten_shape():
    game = Game()
    chapter = Chapter(game, number_of_moves=1, score=0)
    flat = chapter.flatten()
    assert flat.shape == (20, 10, 1)
