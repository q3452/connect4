import unittest
from c4lib.board import Board
from c4lib.randomBot import RandomBot
from c4lib.humanPlayer import HumanPlayer


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    # test horizontal line win condition at either side of the board
    def test_horizontalWinCondition1(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,0)
        self.board.makeMove(1,1)
        self.board.makeMove(1,2)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,3)
        self.assertTrue(self.board.winState == 1)
    def test_horizontalWinCondition2(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,3)
        self.board.makeMove(1,4)
        self.board.makeMove(1,5)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,6)
        self.assertTrue(self.board.winState == 1)

    # test vertical lines at top and bottom of column
    def test_verticalWinCondition1(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,0)
        self.board.makeMove(1,0)
        self.board.makeMove(1,0)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,0)
        self.assertTrue(self.board.winState == 1)
    def test_verticalWinCondition2(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,6)
        self.board.makeMove(1,6)
        self.board.makeMove(2,6)
        self.board.makeMove(2,6)
        self.board.makeMove(2,6)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(2,6)
        self.assertTrue(self.board.winState == 2)

    # test ascending lines in bottom-left and top-right corners
    def test_ascendingWinCondition1(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,0)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,2)
        self.board.makeMove(2,2)
        self.board.makeMove(1,2)
        self.board.makeMove(2,3)
        self.board.makeMove(2,3)
        self.board.makeMove(2,3)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,3)
        self.assertTrue(self.board.winState == 1)
    def test_ascendingWinCondition2(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,3)
        self.board.makeMove(2,4)
        self.board.makeMove(1,5)
        self.board.makeMove(2,6)
        self.board.makeMove(1,3)
        self.board.makeMove(2,4)
        self.board.makeMove(1,5)
        self.board.makeMove(2,6)      
        self.board.makeMove(1,3)
        self.board.makeMove(2,4)
        self.board.makeMove(1,4)
        self.board.makeMove(2,5)
        self.board.makeMove(2,5)
        self.board.makeMove(1,5)
        self.board.makeMove(2,6)
        self.board.makeMove(1,6)
        self.board.makeMove(2,6)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,6)
        self.assertTrue(self.board.winState == 1)

    # test descending lines in top-left and bottom-right corners
    def test_descendingWinCondition1(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,0)
        self.board.makeMove(1,0)
        self.board.makeMove(1,0)
        self.board.makeMove(2,0)
        self.board.makeMove(1,0)
        self.board.makeMove(2,0)
        self.board.makeMove(2,1)
        self.board.makeMove(2,1)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,1)
        self.board.makeMove(2,2)
        self.board.makeMove(2,2)
        self.board.makeMove(1,2)
        self.board.makeMove(2,2)
        self.board.makeMove(1,3)
        self.board.makeMove(2,3)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(2,3)
        self.assertTrue(self.board.winState == 2)
    def test_descendingWinCondition2(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,3)
        self.board.makeMove(1,3)
        self.board.makeMove(1,3)
        self.board.makeMove(2,3)
        self.board.makeMove(1,4)
        self.board.makeMove(1,4)
        self.board.makeMove(2,4)
        self.board.makeMove(2,5)
        self.board.makeMove(2,5)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(2,6)
        self.assertTrue(self.board.winState == 2)

    def test_illegalMoveFull(self):
        self.board.makeMove(1,1)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,1)
        # check that an illegal move will raise an exception
        with self.assertRaises(Exception):
            self.board.makeMove(1,1)

    def test_illegalMoveWon(self):
        self.board.makeMove(1,1)
        self.board.makeMove(1,1)
        self.board.makeMove(1,1)
        self.board.makeMove(1,1)
        self.assertTrue(self.board.winState == 1)
        # check that a move will raise an exception after the game is won
        with self.assertRaises(Exception):
            self.board.makeMove(2,2)

    def test_illegalPlayer(self):
        # check that a move will raise an exception after the game is won
        with self.assertRaises(Exception):
            self.board.makeMove(3,2)
    def test_illegalColumn(self):
        # check that a move will raise an exception after the game is won
        with self.assertRaises(Exception):
            self.board.makeMove(1,9)
    def test_illegalColumnType(self):
        # check that a move will raise an exception after the game is won
        with self.assertRaises(Exception):
            self.board.makeMove(1,'9')
            
    def test_tieCondition(self):
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(2,0)
        self.board.makeMove(1,0)
        self.board.makeMove(2,0)
        self.board.makeMove(1,0)
        self.board.makeMove(2,0)
        self.board.makeMove(1,0)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,1)
        self.board.makeMove(1,1)
        self.board.makeMove(2,2)
        self.board.makeMove(1,2)
        self.board.makeMove(2,2)
        self.board.makeMove(1,2)
        self.board.makeMove(2,2)
        self.board.makeMove(1,2)
        self.board.makeMove(1,3)
        self.board.makeMove(2,3)
        self.board.makeMove(1,3)
        self.board.makeMove(2,3)
        self.board.makeMove(1,3)
        self.board.makeMove(2,3)
        self.board.makeMove(2,4)
        self.board.makeMove(1,4)
        self.board.makeMove(2,4)
        self.board.makeMove(1,4)
        self.board.makeMove(2,4)
        self.board.makeMove(1,4)
        self.board.makeMove(2,5)
        self.board.makeMove(1,5)
        self.board.makeMove(2,5)
        self.board.makeMove(1,5)
        self.board.makeMove(2,5)
        self.board.makeMove(1,5)
        self.board.makeMove(2,6)
        self.board.makeMove(1,6)
        self.board.makeMove(2,6)
        self.board.makeMove(1,6)
        self.board.makeMove(2,6)
        self.assertTrue(self.board.winState == 0)
        self.board.makeMove(1,6)
        self.assertTrue(self.board.winState == -1)

if __name__ == '__main__':
    unittest.main()
