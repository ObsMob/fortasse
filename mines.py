from board import Board


class MineField():
    def __init__(self, board):
        self.board = board
        self.mines = self.generate_mines(self.board.tile_quantity) # this is a list
        self.remaining_mines = len(self.mines)

    def generate_mines(self, tile_quantity):
            number_of_mines = math.ceil(self.board.tile_quantity * random.uniform(.15, .40))
            mines = random.sample(range(1, self.board.tile_quantity + 1), number_of_mines)

            return mines

    def place_mines(self):
        for index_of_mine in self.mines:
            self.board.tiles[index_of_mine].is_mine = True

    def update_remaining_mines(self, delta):
        self.remaining_mines += delta
