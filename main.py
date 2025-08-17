import math
import rand


def main():
    print("Welcome to Bomb-Boinger!")





def game_over(board):
    render = board.board_render

    for mine_index in board.mine_field.mines:
        tile = board.tiles[mine_index]

        tile.reveal_tile(loss=True)
        render.update_tile_symbol(tile)

    print("\nBOOM! You exploded.\n")
    print('Please input "r" for restart, "m" for menu, or "q" for quit\n')

def first_open_tile(board):
    extra_safe_tiles = set()

    for i, tile in board.tiles.items():
        if tile.adjacent_mines == 0:
            extra_safe_tiles.add(i)

    if len(extra_safe_tiles) > 0: 
        start_tile_index = extra_safe_tiles[random.choice(len(extra_safe_tiles))]
        start_tile = board.tiles[start_tile_index]

        start_tile.reveal_tile()
        board.board_render.update_tile_symbol(start_tile)
        print(f'\nTile {start_tile.index} at {start_tile.coords} has been revealed!\n')
        return 

    else:
        kinda_safe_tiles = set()

        for i, tile in board.tiles.items():
            if tile.adjacent_mines <= 2:
                kinda_safe_tiles.add(i)
        
        three_or_less = min(3, len(kinda_safe_tiles))
        start_tiles_indices = random.sample(kinda_safe_tiles, three_or_less)

        for i in start_tiles_indices:
            start_tile = board.tiles[i]
            
            start_tile.reveal_tile()
            board.board_render.update_tile_symbol(start_tile)
            print(f'\nTile {start_tile.index} at {start_tile.coords} has been revealed!\n')


if __name__ == "__main__":
    main()