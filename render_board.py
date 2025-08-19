import sys

from board import Board
from config import Symbol_Icon, Text_Color


class RenderBoardCLI():
    def __init__(self, board):
        self.board = board
        self.total_cli_depth = board.depth * 2 + 1
        self.total_state_depth = board.depth
        self.cli_grid = []

        self.populate_cli_grid()
        for tile in board.tiles.values():
            self.update_tile_symbol(tile)

    def update_tile_symbol(self, tile):
        cli_row, cli_column = self.state_to_cli_index(tile.state_coords) 
        
        self.cli_grid[cli_row][cli_column] = self.get_tile_symbol(tile)
        self.render_tile(tile.state_coords)

    def state_to_cli_index(self, coords):
        r, c  = coords
        return (r * 2, c * 2)

    def get_tile_symbol(self, tile):        
        if tile.game_loss_symbol == "CORRECT":
            return Symbol_Icon.CORRECT.value
        elif tile.game_loss_symbol == "MISSED":
            return Symbol_Icon.BOMB.value
        elif tile.game_loss_symbol == "INCORRECT":
            return Symbol_Icon.INCORRECT.value
        
        if not tile.is_revealed:
            if tile.is_flagged:
                return Symbol_Icon.FLAG.value
            else:
                return Symbol_Icon.UNKNOWN.value

        if tile.is_mine:
            return Symbol_Icon.EXPLODE.value

        digit = self.compose_fullwidth_digit(tile.adjacent_mines)
        color = self.get_digit_color(tile)
        reset_color = Text_Color.RESET.value
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
                return Text_Color.GREY.value
            else:
                return Text_Color.GREEN.value
        
        else:
            return Text_Color.RED.value

    def compose_fullwidth_digit(self, digit):
        if digit <= 9:
            return Symbol_Icon.DIGITS.value[digit]
        else:
            return "".join(Symbol_Icon.DIGITS.value[int(d)] for d in str(digit)) # Parses the digits of a number and combines separate fullwidth versions??

    def populate_cli_grid(self):
        for r in range(self.total_cli_depth + 1):
            row = [] 
            
            for c in range(self.total_cli_depth + 1):
                row.append(self.cli_outline_get_symbol(r, c))
            
            self.cli_grid.append(row)

    def cli_outline_get_symbol(self, r, c):
        if r == 0 or c == 0:
            return self.cli_outline_tile_index(r, c)

        if r == 1:
            if c == 1: 
                return Symbol_Icon.TOPLEFT
            elif c == self.total_cli_depth: 
                return Symbol_Icon.TOPRIGHT
            elif c % 2 == 0: 
                return Symbol_Icon.HORIZ
            else:
                return Symbol_Icon.TOPTEE
        
        elif r == self.total_cli_depth:
            if c == 1:
                return Symbol_Icon.BOTLEFT
            elif c == self.total_cli_depth:
                return Symbol_Icon.BOTRIGHT              
            elif c % 2 == 0:
                return Symbol_Icon.HORIZ
            else:
                return Symbol_Icon.BOTTEE

        elif r % 2 == 0:
            if c % 2 == 1:
                return Symbol_Icon.VERT
            else:
                return Symbol_Icon.EMPTY

        else:
            if c == 1:
                return Symbol_Icon.LEFTTEE
            elif c == self.total_cli_depth:
                return Symbol_Icon.RIGHTTEE
            elif c % 2 == 0:
                return Symbol_Icon.HORIZ
            else:
                return Symbol_Icon.TEE                   

    def render_tile(self, coords):
        cli_row, cli_column = state_to_cli_index(coords)
        symbol = self.cli_grid[cli_row][cli_column]
        ANSI_row = coords[0] * 3 + 1
        ANSI_column = coords[1] * 2 + 1 

        print(f'\033[{ANSI_row};{ANSI_column}H{symbol}', end="", flush=True)

    def cli_outline_tile_index(self, r, c):
        if r == 0:
            if c == 0:
                return Symbol_Icon.EMPTY
            elif c % 2 == 1:
                return " "
            else:
                return self.compose_fullwidth_digit(c / 2)
        
        else:
            if r % 2 == 1:
                return Symbol_Icon.EMPTY
            else:
                return self.compose_fullwidth_digit(r / 2)

    def update_print_remaining_mines(self):

