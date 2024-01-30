import unittest

from Board import Board
from Pieces import Pawn
from Player import Player
from Square import BLACK, WHITE


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_board = Board()

    def put_piece(self, position, piece):
        self.test_board.board[position[0]][position[1]].piece = piece
        piece.set_available_move(self.test_board.board)

    # def test_pawn_moves(self):
    #     test_pawn = Pawn((4, 4), BLACK)
    #     subTest_pawn = Pawn((1, 4), WHITE)
    #     self.put_piece((4, 4), test_pawn)
    #     self.put_piece((5, 3), subTest_pawn)
    #     test_pawn.set_available_move(self.test_board.board)
    #     self.assertTrue(len(test_pawn.attack) == 3)
    #     self.test_board.move_piece((4, 4), (6, 4), Player())
    #     self.assertTrue(len(test_pawn.attack) == 1)



if __name__ == '__main__':
    unittest.main()
