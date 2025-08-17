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
        start_tile = extra_safe_tiles[random.choice(len(extra_safe_tiles) - 1)]
        
        print(f'\nTile {start_tile.index} at {start_tile.coords} has been revealed!\n')
        board.tiles[start_tile].reveal_tile()
        return 

    else:
        kinda_safe_tiles = set()

        for i, tile in board.tiles.items():
            if tile.adjacent_mines <= 2:
                kinda_safe_tiles.add(i)
        
        three_or_less = min(3, len(kinda_safe_tiles))
        start_tiles = random.sample(kinda_safe_tiles, three_or_less)

        for tile in start_tiles:
            print(f'\nTile {tile.index} at {tile.coords} has been revealed!\n')
            board.tiles[tile].reveal_tile()


if __name__ == "__main__":
    main()