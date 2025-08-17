import math

from config import Tile_Shape, BOARD_DEPTH
from mines import MineField
from tile import Tile

class Board():
    def __init__(self, tile_shape_value, board_depth=BOARD_DEPTH):
        self.tiles = {}
        self.depth = board_depth
        self.mine_field = MineField(self)
        self.tile_quantity = self.get_max_tiles()
        try:
            self.tile_shape = Tile_Shape(tile_shape_value)
        except ValueError:
            print(f'{tile_shape_value} is not a supported tile shape.\nExpected Shapes: "3, 4, or 6"')

        for i in range(1, self.tile_quantity + 1):
            self.tiles[i] = Tile(i, self)

        self.mine_field.place_mines()

        tile_mapping = {i: set() for i in range(1, self.tile_quantity + 1)}
        self.add_edges()
        
        for i, neighbors in tile_mapping.items():
            for neighbor in neighbors:
                self.tiles[i].neighbors.append(self.tiles[neighbor])
        
        for tile in self.tiles.values():
            tile.update_adjacent_mines()
            
    def get_max_tiles(self):
        match self.tile_shape:
            
            case Tile_Shape.TRI:
                return self.depth ** 2
            
            case Tile_Shape.SQ:
                return self.depth ** 2

            case Tile_Shape.HEX:
                return 3 * self.depth * (self.depth - 1) + 1

    def add_edges(self):

        match self.tile_shape:

            case Tile_Shape.TRI:
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
            
            case Tile_Shape.SQ:
                for i in range(1, self.tile_quantity + 1):  
                    row = (i - 1) // self.depth + 1
                    column = (i - 1) % self.depth + 1

                    if row != 1:
                        tile_mapping[i].add(i - self.depth)
                    if row != self.depth:
                        tile_mapping[i].add(i + self.depth)
                    if column != 1:
                        tile_mapping[i].add(i - 1)
                    if column != self.depth:
                        tile_mapping[i].add(i + 1)

            case Tile_Shape.HEX:

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
