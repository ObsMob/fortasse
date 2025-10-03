from config import RNGIndices


class HoleField():
    def __init__(self, board):
        self.board = board
        self.holes = []

    def generate_hole_indices(self):  
        self.holes = self.board.rng_generate_indices(RNGIndices.HOLES)

    def set_hole_attr(self):
        for index_of_hole in self.holes:
            self.board.tiles[index_of_hole].is_hole = True
