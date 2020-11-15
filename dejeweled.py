import random
import copy
import ai

WIDTH = 8
HEIGHT = 10
GEMS = ["△", "◆", "◙", "▩", "◎", "◓"] # ,"▢"]

def main():
    # setup board with random values
    BOARD = [[random.choice(GEMS) for c in range(WIDTH)] for r in range(HEIGHT)]
    SCORE = 0
    MOVES = 0
    GEMS_CLEARED = 0
    CASCADES = 0

    # clear matches
    while get_matches(BOARD) != []:
        for match in get_matches(BOARD):
            for gem in match:
                BOARD[gem[1]][gem[0]] = random.choice(GEMS)

    # game loop
    while(True):
        #print("\nscore: ", SCORE)
        #print_board(BOARD)
        #sys.stdout.flush()

        # print("enter pairs to swap: x1 y1 x2 y2")
        # coords = [int(val) for val in input().split(" ")]

        current_node = ai.Node(BOARD, SCORE, 0)
        if not current_node.get_valid_swaps():
            print("GAME OVER")
            print_board(BOARD)
            print("final score:    ", SCORE)
            print("moves:          ", MOVES)
            print("gems cleared:   ", GEMS_CLEARED)
            print("cascades:       ", CASCADES)
            print("avg gems/move:  ", float(GEMS_CLEARED) / float(MOVES))
            print("avg score/move: ", float(SCORE) / float(MOVES))
            exit()

        MOVES += 1
        coords = current_node.get_next_swap()

        # make swap on prospective next board
        next_board = copy.deepcopy(BOARD)
        swap_gems(next_board,coords[0], coords[1], coords[2], coords[3])
        
        # check that match is valid
        matches = get_matches(next_board)
        if matches == []: continue
        BOARD = next_board

        # track if we are cascading
        settled_once = False
        # clear matches and increment score until settled
        while get_matches(BOARD) != []:
            if settled_once: CASCADES += 1
            for match in get_matches(BOARD):
                for gem in match:
                    SCORE += (10 + (len(match) - 3) * 10)
                    BOARD[gem[1]][gem[0]] = " "
                    GEMS_CLEARED += 1

            settled_once = True
            drop_and_fill(BOARD)

def get_gem(board, x, y):
    '''
    get gem on board at specified (x, y)
    ensures x and y are within bounds of board
    '''
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT): return " "
    else: return board[y][x]

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
            if board_copy[y][x] == get_gem(board_copy,x+1,y) == get_gem(board_copy,x+2,y) != " ":
                target = board_copy[y][x]
                offset = 0
                gems = []
                while get_gem(board_copy,x+offset,y) == target:
                    gems.append((x+offset, y))
                    board_copy[y][x+offset] = " "
                    offset += 1
                groups_to_remove.append(gems)

            # look for vertical matches
            if board_copy[y][x] == get_gem(board_copy,x,y+1) == get_gem(board_copy,x,y+2) != " ":
                target = board_copy[y][x]
                offset = 0
                gems = []
                while get_gem(board_copy,x,y+offset) == target:
                    gems.append((x,y+offset))
                    board_copy[y+offset][x] = " "
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
        print("║ ", end="")
        for row in col:
            print(row, " ", end="")
        print("║")

if __name__ == "__main__":
    main()