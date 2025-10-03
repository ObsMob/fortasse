import random
import math

from config import TileShape, RNGIndices
from tile import Tile
from mines import MineField
from holes import HoleField


class Board():
    def __init__(self, settings):
        self.depth = settings["BOARD_DEPTH"]
        self.tile_shape = settings["TILE_SHAPE"]
        self.corners = settings["CORNERS"]
        self.holes = settings["HOLES"]
        self.colours = settings["COLOURS"]
        self.tiles = {}
        self.tile_quantity = self.get_max_tiles()
        self.first_reveals = []
        self.saved_board_data = [] # [mines_list, holes_list, first_reveal_list]
        self.mine_field = MineField(self)
        self.hole_field = HoleField(self)
        self.board_render = None # RenderBoardCLI(board)
        
    def populate_tiles_data(self):
        tile_mapping = {}

        for i in range(1, self.tile_quantity + 1):
            self.tiles[i] = Tile(self)
            tile_mapping[i] = set()

        self.assign_state_coords()
        self.add_edges(tile_mapping)
        self.map_tile_neighbors(tile_mapping)
        self.mine_field.set_mine_attr()

        for tile in self.tiles.values():
            tile.update_adjacent_mines()

        if self.holes:
            self.hole_field.set_hole_attr()

            for tile in self.tiles.values():
                tile.neighbors = [n for n in tile.neighbors if not n.is_hole]

    def get_max_tiles(self):
        match self.tile_shape:
            
            case TileShape.TRI:
                return self.depth ** 2 
            case TileShape.SQ:
                return self.depth ** 2
            case TileShape.HEX:
                return 3 * self.depth * (self.depth - 1) + 1

    def add_edges(self, tile_mapping):
        # Adds to tile_mapping set of neighbor's indices
        match self.tile_shape:

            case TileShape.TRI:
                for i in range(1, self.tile_quantity + 1):              
                    row = math.ceil(i ** 0.5)
                    row_start = (row - 1) ** 2 + 1
                    row_end = row ** 2
                    
                    if i != row_start:
                        tile_mapping[i].add(i - 1)
                    if i != row_end:
                        tile_mapping[i].add(i + 1)
                        
                    if row % 2 == 1:
                        if i % 2 == 1 and row != self.depth:
                            tile_mapping[i].add(i + (row * 2))
                        elif i % 2 == 0:
                            tile_mapping[i].add(i - (row - 1) * 2)
                    else:
                        if i % 2 == 0 and row != self.depth:
                            tile_mapping[i].add(i + (row * 2))
                        elif i % 2 == 1:
                            tile_mapping[i].add(i - (row - 1) * 2)
            
            case TileShape.SQ:
                
                for i in range(1, self.tile_quantity + 1):  
                    row = (i - 1) // self.depth + 1
                    column = (i - 1) % self.depth + 1

                    # Cardinal
                    if row != 1:
                        tile_mapping[i].add(i - self.depth)
                    if row != self.depth:
                        tile_mapping[i].add(i + self.depth)
                    if column != 1:
                        tile_mapping[i].add(i - 1)
                    if column != self.depth:
                        tile_mapping[i].add(i + 1)

                    # Diagonal
                    if self.corners:
                        if row != 1:
                            if column != 1:
                                tile_mapping[i].add(i - self.depth - 1)
                            if column != self.depth:
                                tile_mapping[i].add(i - self.depth + 1)
                        if row != self.depth:
                            if column != 1:
                                tile_mapping[i].add(i + self.depth - 1)
                            if column != self.depth:
                                tile_mapping[i].add(i + self.depth + 1)

            case TileShape.HEX:
                # Create axial coordinates from center tile, map to index and vice versa
                def hex_axial_mapping():
                    index_to_axial = {}
                    axial_to_index = {}
                    
                    axial_depth = self.depth - 1
                    row = axial_depth
                    column = -axial_depth

                    for i in range(1, self.tile_quantity + 1):
                        
                        if row >= 0:
                            if row + column == axial_depth:
                                index_to_axial[i] = (row, column)
                                column = -axial_depth
                                row -= 1
                            
                            elif row + column < axial_depth:
                                index_to_axial[i] = (row, column)
                                column += 1
                        
                        else:
                            column += 1

                            if column == axial_depth:
                                index_to_axial[i] = (row, column)
                                column = -axial_depth - row
                                row -= 1

                            else:
                                index_to_axial[i] = (row, column)
                
                    for index, coords in index_to_axial.items():
                        axial_to_index[coords] = index
                    
                    return index_to_axial, axial_to_index

                def neighbors_get(coord):
                    d_neighbors = [
                        (0, -1),
                        (0, 1),
                        (1, -1),
                        (1, 0),
                        (-1, 0),
                        (-1, 1),
                    ]
                    row, column = coord

                    return [(row + dr, column + dc) for dr, dc in d_neighbors]

                index_to_coord, coord_to_index = hex_axial_mapping()

                for i in index_to_coord:
                    for coord in neighbors_get(index_to_coord[i]):
                        if coord in coord_to_index:
                            tile_mapping[i].add(coord_to_index[coord])
    
    def map_tile_neighbors(self, tile_mapping):
        for i, neighbors in tile_mapping.items():
            for neighbor in neighbors:
                self.tiles[i].neighbors.append(self.tiles[neighbor])

    def assign_state_coords(self):
        tile_index = 1
        for r in range(1, self.depth + 1):
            for c in range(1, self.depth + 1):
                self.tiles[tile_index].state_coords = (r, c)
                tile_index += 1

    def get_tile_from_coords(self, coords):
        row, col = coords

        for tile in self.tiles.values():
            if tile.state_coords == (row, col):
                return tile

    def rng_generate_indices(self, index_type):
        quant = self.tile_quantity
        free_indices = []

        match index_type:

            case RNGIndices.MINES:

                quant_of_mines = math.ceil(quant * random.uniform(.15, .40))
                mines = random.sample(range(1, quant + 1), quant_of_mines)
                return mines

            case RNGIndices.HOLES:
                
                for i in range (1, quant + 1):
                    free_indices.append(i)
                    
                for mine_index in self.mine_field.mines:
                    free_indices.remove(mine_index)
                
                quant_of_holes = math.ceil(quant * random.uniform(.08, .16))
                holes = random.sample(free_indices, quant_of_holes)
                return holes

            case RNGIndices.COLORS:
                return

    def populate_first_reveals(self):
        extra_safe_tiles = set()
        kinda_safe_tiles = set()

        for i, tile in self.tiles.items():
            if tile.adjacent_mines == 0 and not tile.is_mine and not tile.is_hole:
                extra_safe_tiles.add(i)

        if extra_safe_tiles: 
            start_tile_index = random.choice(list(extra_safe_tiles))
            start_tile = self.tiles[start_tile_index]

            self.first_reveals = [start_tile_index]

        else:
            for i, tile in self.tiles.items():
                if tile.adjacent_mines <= 2 and not tile.is_mine and not tile.is_hole:
                    kinda_safe_tiles.add(i)
            
            three_or_less = min(3, len(kinda_safe_tiles))
            start_tiles_indices = random.sample(list(kinda_safe_tiles), three_or_less)

            self.first_reveals = start_tiles_indices

    def populate_save_data(self):

        self.saved_board_data.append(self.mine_field.mines)
        self.saved_board_data.append(self.hole_field.holes)
        self.saved_board_data.append(self.first_reveals)
