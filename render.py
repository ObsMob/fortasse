
from config import Symbol_Icon, Text_Color
from board import Board

class RenderCLI():
    def __init__(self, board):
        self.board = board
        self.total_cli_depth = board.depth * 2 + 1
        self.total_state_depth = board.depth
        self.cli_grid = []

        self.populate_cli_grid()
        for tile in board.tiles.values():
            self.update_tile_symbol(tile)

    def update_tile_symbol(self, tile):
        cli_row, cli_column = self.state_to_cli(tile.state_coords)
        #mutate symbol in cli_grid on call
        #call helpers for symbols

    def state_to_cli_index(self, coords):
        r, c  = coords
        return (r * 2 - 1, c * 2 - 1)

    def get_tile_symbol(self, tile):
        if not tile.is_revealed:
            if tile.is_flagged:
                return Symbol_Icon.FLAG.value
            else:
                return Symbol_Icon.UNKNOWN.value
        
        if tile.game_loss_symbol == "CORRECT":
            return Symbol_Icon.CORRECT.value
        elif tile.game_loss_symbol == "MISSED":
            return Symbol_Icon.BOMB.value
        elif tile.game_loss_symbol == "INCORRECT":
            return Symbol_Icon.INCORRECT.value

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

    def compose_fullwidth_digit(self, mine_count):
        if mine_count <= 9:
            return Symbol_Icon.DIGITS.value[mine_count]
        else:
            return "".join(Symbol_Icon.DIGITS.value[int(d)] for d in str(mine_count)) # Parses the digits of a number and combines separate fullwidth versions??

    def populate_cli_grid(self):
        for r in range(1, self.total_cli_depth + 1):
            row = [] 
            
            for c in range(1, self.total_cli_depth + 1):
                row.append(self.cli_outline_render(r, c))
            
            self.cli_grid.append(row)

    def cli_outline_render(self, r, c):
        if r == 1:
            if c == 1: 
                return "╔"
            elif c == self.total_cli_depth: 
                return "╗"
            elif c % 2 == 0: 
                return "═"
            else:
                return "╦"
        
        elif r == self.total_cli_depth:
            if c == 1:
                return "╚"
            elif c == self.total_cli_depth:
                return "╝"              
            elif c % 2 == 0:
                return "═"
            else:
                return "╩"

        elif r % 2 == 0:
            if c % 2 == 1:
                return "║"
            else:
                return "  "

        else:
            if c == 1:
                return "╠"
            elif c == self.total_cli_depth:
                return "╣"
            elif c % 2 == 0:
                return "═"
            else:
                return "╬"                   



