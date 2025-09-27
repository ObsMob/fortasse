import random
import math

from board import Board


class MineField():
    def __init__(self, board):
        self.board = board
        self.mines = None # This is a list
        self.remaining_mines = 0

    def generate_mine_indices(self, tile_quantity):
            quantity_of_mines = math.ceil(self.board.tile_quantity * random.uniform(.15, .40))
            mines = random.sample(range(1, self.board.tile_quantity + 1), quantity_of_mines)

            return mines

    def set_tile_mine_attr(self):
        for index_of_mine in self.mines:
            self.board.tiles[index_of_mine].is_mine = True

    def update_remaining_mines(self, delta):
        self.remaining_mines += delta

    def set_remaining_mines(self):
        self.remaining_mines = len(self.mines)
