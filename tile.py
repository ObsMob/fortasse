class Tile():
    def __init__(self, index, board):
        self.board = board
        self.index = index
        self.neighbors = []
        self.is_mine = False
        self.adjacent_mines = 0
        self.is_revealed = False
        self.is_marked = False

    def update_adjacent_mines(self): 
        count = 0
        
        for neighbor in self.neighbors:
            if neighbor.is_mine:
                count += 1
        
        self.adjacent_mines = count

    def reveal_tile(self, loss=False):
        if loss == False:
            
            if self.is_revealed:
                print(f'Error: Tile {self.index} is already revealed.\n')
                return

            elif self.is_marked:
                print(f'Error: Tile {self.index} is marked. To reveal, first unmark Tile {self.index}.\n')
                return

            elif self.is_mine:
                #replace tile display with explosion
                return game_over(self.board)

            else:
                self.is_revealed = True

                for neighbor in self.neighbors:
                    if (
                        neighbor.is_revealed == False and 
                        neighbor.adjacent_mines == 0
                    ):
                        neighbor.reveal_tile()
        
        else: 
            if self.is_mine and self.is_marked:
                #replace mark with green check
            elif self.is_mine and not self.is_marked:
                #replace display with bomb
            elif not self.is_mine and self.is_marked:
                #replace with red x
        
    def mark_tile(self):
        if self.is_marked == True:
            self.is_marked = False
            self.board.mine_field.update_remaining_mines(+1)
            print(f'\nTile{self.index} has been unmarked.')
        else:
            self.is_marked = True
            self.board.mine_field.update_remaining_mines(-1)
            print(f'\nTile{self.index} has been marked.')
