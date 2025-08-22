import random

from board import Board
from config import SymbolIcon, TextColor
from cursor import print_wo_newline, print_w_flush, reset_line


class RenderBoardCLI():
    def __init__(self, board):
        self.board = board
        self.total_cli_depth = board.depth * 2 + 1
        self.cli_grid = []

        self.populate_cli_grid()
        for tile in board.tiles.values():
            self.update_tile_symbol(tile)

    def update_tile_symbol(self, tile):
        cli_row, cli_column = self.state_to_cli_index(tile.state_coords) 
      
        self.cli_grid[cli_row][cli_column] = self.get_tile_symbol(tile)

    def state_to_cli_index(self, coords):
        r, c  = coords
        return (r * 2, c * 2)
    
    def get_tile_symbol(self, tile):        
        if tile.game_loss_symbol == "CORRECT":
            return SymbolIcon.CORRECT.value
        elif tile.game_loss_symbol == "MISSED":
            return SymbolIcon.BOMB.value
        elif tile.game_loss_symbol == "INCORRECT":
            return SymbolIcon.INCORRECT.value
        
        if not tile.is_revealed:
            if tile.is_flagged:
                return SymbolIcon.FLAG.value
            else:
                return SymbolIcon.UNKNOWN.value

        if tile.is_mine:
            return SymbolIcon.EXPLODE.value

        digit = SymbolIcon.DIGITS.value[tile.adjacent_mines]
        color = self.get_digit_color(tile)
        reset_color = TextColor.RESET.value
        return f'{color}{digit}{reset_color}'

    def get_digit_color(self, tile):
        if tile.adjacent_mines == tile.adjacent_flags:
            neighbor_pass = 0

            for neighbor in tile.neighbors:
                if (
                    neighbor.is_mine and neighbor.is_flagged or
                    not neighbor.is_mine and neighbor.is_revealed
                ):
                    neighbor_pass += 1
            
            if neighbor_pass == len(tile.neighbors):
                return TextColor.GREY.value
            else:
                return TextColor.GREEN.value
        
        else:
            return TextColor.RED.value

    def populate_cli_grid(self):
        for r in range(self.total_cli_depth + 1):
            row = [] 
            
            for c in range(self.total_cli_depth + 1):
                row.append(self.cli_outline_get_symbol(r, c))
            
            self.cli_grid.append(row)

    def cli_outline_get_symbol(self, r, c):
        if r == 0 or c == 0:
            return self.cli_outline_indices(r, c)

        if r == 1:
            if c == 1: 
                return SymbolIcon.TOPLEFT.value
            elif c == self.total_cli_depth: 
                return SymbolIcon.TOPRIGHT.value
            elif c % 2 == 0: 
                return SymbolIcon.HORIZ.value * 2
            else:
                return SymbolIcon.TOPTEE.value
        
        elif r == self.total_cli_depth:
            if c == 1:
                return SymbolIcon.BOTLEFT.value
            elif c == self.total_cli_depth:
                return SymbolIcon.BOTRIGHT.value
            elif c % 2 == 0:
                return SymbolIcon.HORIZ.value * 2
            else:
                return SymbolIcon.BOTTEE.value

        elif r % 2 == 0:
            if c % 2 == 1:
                return SymbolIcon.VERT.value
            else:
                return SymbolIcon.EMPTY.value

        else:
            if c == 1:
                return SymbolIcon.LEFTTEE.value
            elif c == self.total_cli_depth:
                return SymbolIcon.RIGHTTEE.value
            elif c % 2 == 0:
                return SymbolIcon.HORIZ.value * 2
            else:
                return SymbolIcon.TEE.value            

    def cli_outline_indices(self, r, c):
        if c == 0:
            if r == 0 or r % 2 == 1:
                return SymbolIcon.EMPTY.value
            else:
                return f'{r // 2:>2}'
        else:
            if c % 2 == 1:
                return " "
            else:
                return f'{c // 2:>2}'

    def draw_board(self):

        for tile in self.board.tiles.values():
            self.update_tile_symbol(tile)

        for r in range(len(self.cli_grid)):
            for c in range(len(self.cli_grid[r])):

                if c == len(self.cli_grid[r]) - 1:
                    print_w_flush(self.cli_grid[r][c])
                else:
                    print_wo_newline(self.cli_grid[r][c])

        reset_line()
        self.draw_remaining_mines()
        reset_line()

    def draw_remaining_mines(self):
        remaining_mines = self.board.mine_field.remaining_mines
        board_width = self.board.depth * 3 + 1

        return print_w_flush(f'\033[3G{"Remaining Mines: " + str(remaining_mines):^{board_width}}')

    def first_tile_reveal(self):
        extra_safe_tiles = set()
        kinda_safe_tiles = set()

        for i, tile in self.board.tiles.items():
            if tile.adjacent_mines == 0 and not tile.is_mine:
                extra_safe_tiles.add(i)

        if extra_safe_tiles: 
            start_tile_index = random.choice(list(extra_safe_tiles))
            start_tile = self.board.tiles[start_tile_index]

            start_tile.reveal_tile()
            self.update_tile_symbol(start_tile)
            return 

        else:
            for i, tile in self.board.tiles.items():
                if tile.adjacent_mines <= 2 and not tile.is_mine:
                    kinda_safe_tiles.add(i)
            
            three_or_less = min(3, len(kinda_safe_tiles))
            start_tiles_indices = random.sample(list(kinda_safe_tiles), three_or_less)

            for i in start_tiles_indices:
                start_tile = self.board.tiles[i]
                
                start_tile.reveal_tile()
                self.update_tile_symbol(start_tile)
