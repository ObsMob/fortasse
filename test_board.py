import unittest

from board import Board


class Test_Board_Creation(unittest.TestCase):
    def test_hex_board(self):
        board2 = Board(6, 2)
        board3 = Board(6, 3)
        
        self.assertEqual(board2.tiles,
            {
                1: {2, 3, 4},
                2: {1, 4, 5},
                3: {1, 4, 6},
                4: {1, 2, 3, 5, 6, 7},
                5: {2, 4, 7},
                6: {3, 4, 7},
                7: {6, 4, 5}
            }
        )
        self.assertEqual(board3.tiles,
            {
                1: {2, 4, 5},
                2: {1, 3, 5, 6},
                3: {2, 6, 7},
                4: {1, 5, 8, 9},
                5: {1, 2, 4, 6, 9, 10},
                6: {2, 3, 5, 7, 10, 11},
                7: {3, 6, 11, 12},
                8: {4, 9, 13},
                9: {4, 5, 8, 10, 13, 14},
                10: {5, 6, 9, 11, 14, 15},
                11: {6, 7, 10, 12, 15, 16},
                12: {7, 11, 16},
                13: {8, 9, 14, 17},
                14: {9, 10, 13, 15, 17, 18},
                15: {10, 11, 14, 16, 18, 19},
                16: {11, 12, 15, 19},
                17: {13, 14, 18},
                18: {14, 15, 17, 19},
                19: {15, 16, 18},
            }
        )

    def test_sq_board(self):
        board = Board(4, 2)

        self.assertEqual(
            board.tiles,
            {
                1: {2, 3},
                2: {1, 4},
                3: {1, 4},
                4: {2, 3}
            }
        )

    def test_tri_board(self):
        board2 = Board(3, 2)
        board3 = Board(3, 3)

        self.assertEqual(
            board2.tiles,
            {
                1: {3},
                2: {3},
                3: {1, 2, 4},
                4: {3}
            }
        )
        self.assertEqual(
            board3.tiles,
            {
                1: {3},
                2: {3, 6},
                3: {1, 2, 4},
                4: {3, 8},
                5: {6},
                6: {2, 5, 7},
                7: {6, 8},
                8: {4, 7, 9},
                9: {8}                
            }
        )

    def test_invalid_shape(self):
        board69 = Board(69)

if __name__ == "__main__":
    main()