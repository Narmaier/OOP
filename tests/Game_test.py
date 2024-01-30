import unittest
from Game import Game, WIN
from Pieces import *

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.test_game = Game()

    def test_castling(self):
        self.test_game.round((7, 6), (5, 5))
        self.test_game.round((6, 6), (4, 6))
        self.test_game.round((6, 6), (4, 6))
        self.test_game.round((7, 5), (6, 6))
        self.assertIsNotNone(self.test_game.castling_move((7, 4), (7, 7)))

    def test_promote(self):
        self.test_game.promote((6, 0), "q")
        self.assertIsInstance(self.test_game.board.pieceAt((6, 0)), Queen)

        self.test_game.promote((6, 1), "r")
        self.assertIsInstance(self.test_game.board.pieceAt((6, 1)), Rook)

        self.test_game.promote((6, 2), "b")
        self.assertIsInstance(self.test_game.board.pieceAt((6, 2)), Bishop)

        self.test_game.promote((6, 3), "n")
        self.assertIsInstance(self.test_game.board.pieceAt((6, 3)), Knight)

    def test_checkmate(self):
        self.test_game.round((6, 6), (4, 6))
        self.test_game.round((6, 5), (4, 5))
        self.test_game.round((1, 4), (3, 4))
        self.test_game.round((0, 3), (4, 7))

        self.assertEqual(self.test_game.check_game_status(), WIN)


if __name__ == '__main__':
    unittest.main()
