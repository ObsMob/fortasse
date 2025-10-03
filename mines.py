from config import RNGIndices


class MineField():
    def __init__(self, board):
        self.board = board
        self.mines = []
        self.remaining_mines = 0

    def generate_mine_indices(self):  
        self.mines = self.board.rng_generate_indices(RNGIndices.MINES)

    def set_mine_attr(self):
        for index_of_mine in self.mines:
            self.board.tiles[index_of_mine].is_mine = True

    def update_remaining_mines(self, delta):
        self.remaining_mines += delta

    def set_remaining_mines(self):
        self.remaining_mines = len(self.mines)

