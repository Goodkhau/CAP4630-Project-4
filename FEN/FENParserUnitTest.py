import unittest
import FENParser
board_one = [
    [-4, -2, -3, -5, -6, -3, -2, -4],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [4, 2, 3, 5, 6, 3, 2, 4]
]

class MyTestCase(unittest.TestCase):
    def test_board_one(self):
        f = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        fen = FENParser.FENParser(f)
        fen.Parse()
        fen = fen.ToTensor()
        self.assertEqual(board_one, fen)


if __name__ == '__main__':
    unittest.main()
    print(fen)
