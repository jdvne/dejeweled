import random, copy

WIDTH = 8
HEIGHT = 8
GEMS = ['!', '@', '#', '$', '%', '&', '*']

def main():
    # setup board with random values
    BOARD = [[random.choice(GEMS) for c in range(WIDTH)] for r in range(HEIGHT)]
    SCORE = 0

    # clear matches
    while get_matches(BOARD) != []:
        for match in get_matches(BOARD):
            for gem in match:
                BOARD[gem[1]][gem[0]] = random.choice(GEMS)

    # game loop
    while(True):
        print("\nscore: ", SCORE)
        print_board(BOARD)

        print("enter pairs to swap: x1 y1 x2 y2")
        coords = [int(val) for val in input().split(" ")]

        # make swap on prospective next board
        next_board = copy.deepcopy(BOARD)
        swap_gems(next_board,coords[0], coords[1], coords[2], coords[3])
        
        # check that match is valid
        matches = get_matches(next_board)
        if matches == []: continue
        BOARD = next_board

        # clear matches and increment score
        while get_matches(BOARD) != []:
            for match in get_matches(BOARD):
                for gem in match:
                    SCORE += (10 + (len(match) - 3) * 10)
                    BOARD[gem[1]][gem[0]] = " "

            drop_and_fill(BOARD)

def get_gem(board, x, y):
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT): return " "
    else return board[y][x]

def swap_gems(board,x1,y1,x2,y2):
    '''
    Swap two gems on a board given their coordinates
    '''
    # Swap the gems
    board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

def get_matches(board):
    '''
    return a list of groups of gems in matching triplets that should be removed
    [[(x1,y1),(x2,y2),(x3,y3)],...]
    '''
    groups_to_remove = []
    board_copy = copy.deepcopy(board)

    # loop through each space, check for 3 adjacent identical gems
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # look for horizontal matches
            if x+2 < WIDTH and board_copy[y][x] == board_copy[y][x+1] == board_copy[y][x+2] != " ":
                target = board_copy[y][x]
                offset = 0
                gems = []
                while x+offset < WIDTH and board_copy[y][x+offset] == target:
                    gems.append((x+offset, y))
                    board_copy[x+offset][y] = " "
                    offset += 1
                groups_to_remove.append(gems)

            # look for vertical matches
            if y+2 < HEIGHT and board_copy[y][x] == board_copy[y+1][x] == board_copy[y+2][x] != " ":
                target = board_copy[y][x]
                offset = 0
                gems = []
                while y+offset < HEIGHT and board_copy[y+offset][x] == target:
                    gems.append((x,y+offset))
                    board_copy[x][y+offset] = " "
                    offset += 1
                groups_to_remove.append(gems)

    return groups_to_remove

def apply_gravity(board):
    for x in range(WIDTH):
        for y in range(HEIGHT - 1):
            if board[y+1][x] == " ":
                swap_gems(board, x, y, x, y+1)

def drop_and_fill(board):
    apply_gravity(board)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[y][x] == " ":
                board[y][x] = random.choice(GEMS)
    
def print_board(board):
    for col in board:
        print("|", end="")
        for row in col:
            print(" ", row, " ", end="")
        print("|")

if __name__ == "__main__":
    main()