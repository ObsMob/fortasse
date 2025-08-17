

def render_cli(board):
    self.board = board
    self.total_cli_rows = board.depth * 2 + 1
    self.total_cli_columns = board.depth * 2 + 1
    self.total_state_rows = board.depth
    self.total_state_columns = board.depth

    def get_render_symbol(self, r, c):
        if r == 1:
            if c == 1: 
                return "╔"
            elif c == self.total_cli_columns: 
                return "╗"
            elif c % 2 == 0: 
                return "═"
            else:
                return "╦"
        
        elif r == self.total_cli_rows:
            if c == 1:
                return "╚"
            elif c == self.total_cli_columns:
                return "╝"              
            elif c % 2 == 0:
                return "═"
            else:
                return "╩"

        elif r % 2 == 0:
            elif c % 2 == 1:
                return "║"
            else:
                return "⬜"

        else:
            if c == 1:
                return "╠"
            elif c == self.total_cli_columns:
                return "╣"
            elif c % 2 == 0:
                return "═"
            else:
                return "╬"                   
                    

    def board_render(self):
        board_strings = []
        
        for r in range(1, self.total_cli_rows + 1):
            row = ""
            
            for c in range(1, self.total_cli_columns + 1):
                row += self.get_render_symbol(r, c)

            board_strings.append(row)