import unittest
import Board
from Pieces import Piece
from Player import Player


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.test_board = Board.Board()

    def test_filling(self):
        self.test_board.fill_board()
        for i in [0, 1, 6, 7]:
            for j in range(8):
                self.assertIsInstance(self.test_board.pieceAt((i, j)), Piece)
        for i in range(2, 6):
            for j in range(8):
                self.assertIsNone(self.test_board.pieceAt((i, j)))

    def test_setup_stats(self):
        self.test_board.fill_board()
        self.test_board.per_update_stats()
        for i in [1, 6]:
            for j in range(8):
                self.assertTrue(len(self.test_board.pieceAt((i, j)).attack) > 0)
        for move in [(0, 1), (0, 6), (7, 1), (7, 6)]:
            self.assertTrue(len(self.test_board.pieceAt(move).attack) > 0)

    def test_move(self):
        self.test_board.fill_board()
        self.test_board.per_update_stats()
        self.assertTrue(len(self.test_board.pieceAt((0, 4)).attack) == 0)
        self.assertIsNotNone(self.test_board.move_piece((1, 4), (3, 4), Player()))
        self.assertIsNotNone(self.test_board.move_piece((0, 4), (1, 4), Player()))
        self.assertIsNotNone(self.test_board.move_piece((0, 3), (0, 4), Player()))

    def test_adding_stats(self):
        self.test_board.fill_board()
        self.test_board.per_update_stats()
        self.test_board.move_piece((6, 0), (4, 0), Player())

        for move in self.test_board.pieceAt((7, 0)).attack.keys():
            self.assertTrue(len(self.test_board.board[move[0]][move[1]].attack) > 0)

        self.test_board.move_piece((7, 0), (5, 0), Player())

        for move in self.test_board.pieceAt((5, 0)).attack.keys():
            self.assertTrue(len(self.test_board.board[move[0]][move[1]].attack) > 0)

    def test_deleting_stats(self):
        self.test_board.fill_board()
        self.test_board.per_update_stats()
        self.assertTrue(len(self.test_board.board[5][1].attack) == 2)
        self.test_board.move_piece((6, 0), (4, 0), Player())
        self.assertTrue(len(self.test_board.board[5][1].attack) == 1)



if __name__ == '__main__':
    unittest.main()
