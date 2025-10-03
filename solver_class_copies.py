

class SolverTile:
    def __init__(self, is_mine, is_revealed):
        self.neighbors = []
        self.is_revealed = is_revealed
        self.is_mine = is_mine
        self.is_flagged = False
        self.adjacent_mines = 0
        self.adjacent_flags = 0

    def reveal_tile(self):

        if not self.is_revealed and not self.is_flagged:
            self.is_revealed = True

    def flag_tile(self):

        if not self.is_flagged and not self.is_revealed:
            self.is_flagged = True
            for n in self.neighbors:
                n.adjacent_flags += 1

class SolverBoard:
    def __init__(self, board):
        self.tiles = {}
        self.tile_quantity = board.tile_quantity
        self.mines_quant = len(board.saved_board_data[0])
        self.holes = board.holes
        self.holes_quant = len(board.saved_board_data[1]) if self.holes else 0

        self.populate_tiles_data(board)

    def populate_tiles_data(self, board):
        tile_to_index = {}
        
        for i, tile in board.tiles.items():
            tile_to_index[tile] = i
            solver_tile = SolverTile(tile.is_mine, tile.is_revealed)
            self.tiles[i] = solver_tile

        for i, tile in board.tiles.items():
            solver_tile = self.tiles[i]

            for neighbor in tile.neighbors:
                neighbor_i = tile_to_index[neighbor]
                solver_tile.neighbors.append(self.tiles[neighbor_i])
        
        for tile in self.tiles.values():
            for neighbor in tile.neighbors:
                if neighbor.is_mine:
                    tile.adjacent_mines +=1
