from config import RevealType


class Tile():
    def __init__(self, index, board):
        self.board = board
        self.index = index
        self.neighbors = []
        self.is_mine = False
        self.adjacent_mines = 0
        self.adjacent_flags = 0
        self.is_revealed = False
        self.is_flagged = False
        self.state_coords = None
        self.game_loss_symbol = None

    def update_adjacent_mines(self): 
        count = 0
        
        for neighbor in self.neighbors:
            if neighbor.is_mine:
                count += 1
        
        self.adjacent_mines = count

    def update_adjacent_flags(self):
        count = 0
        
        for neighbor in self.neighbors:
            if neighbor.is_flagged:
                count += 1
        
        self.adjacent_flags = count

    def reveal_tile(self, loss=False):
        if loss == False:
            
            if self.is_revealed:
                return RevealType.ISREVEALED
            elif self.is_flagged:
                return RevealType.ISFLAGGED
            elif self.is_mine:
                self.is_revealed = True
                return RevealType.ISMINE
            else:
                self.is_revealed = True

        else: 
            if not self.is_revealed:
                if self.is_mine and self.is_flagged:
                    self.game_loss_symbol = "CORRECT"
                elif self.is_mine and not self.is_flagged:
                    self.game_loss_symbol = "MISSED"
                elif not self.is_mine and self.is_flagged:
                    self.game_loss_symbol = "INCORRECT"

    def flag_tile(self):
        mine_field = self.board.mine_field
        if self.is_revealed:
            return RevealType.ISREVEALED

        elif self.is_flagged == True:    
            
            self.is_flagged = False
            mine_field.update_remaining_mines(+1)

            for neighbor in self.neighbors:
                neighbor.update_adjacent_flags()
            
            return RevealType.UNFLAG

        else:
            self.is_flagged = True
            mine_field.update_remaining_mines(-1)
            
            for neighbor in self.neighbors:
                neighbor.update_adjacent_flags()
            
            return RevealType.ISFLAGGED
