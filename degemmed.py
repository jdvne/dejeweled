import random, copy, sys
import pygame
from itertools import combinations_with_replacement
from pygame.locals import *

WINDOWWIDTH = 600  # width of the program's window, in pixels
WINDOWHEIGHT = 600 # height in pixels
GEMIMAGESIZE = 64 # width & height of each space in pixels

NUMMATCHSOUNDS = 6

MOVERATE = 25 # 1 to 100, larger num means faster animations
DEDUCTSPEED = 0.8 # reduces score by 1 point every DEDUCTSPEED seconds.

BGCOLOR = Color("#4ba173") # background color on the screen
GRIDCOLOR = Color("#63d297") # color of the game board
SCORECOLOR = Color("#deffce") # color of the text for the player's score

USER_INPUT = False
PRINT_BOARDS = False

WIDTH = 8
HEIGHT = 8
GEMS = ["△", "◆", "◙", "▩", "◎", "◓"] #, "▢"]

XMARGIN = int((WINDOWWIDTH - GEMIMAGESIZE * WIDTH) / 2)
YMARGIN = int((WINDOWHEIGHT - GEMIMAGESIZE * HEIGHT) / 2)

AGENT = "expectimax"

BOARDCELLS = []
for x in range(WIDTH):
    BOARDCELLS.append([])
    for y in range(HEIGHT):
        r = pygame.Rect((XMARGIN + x * GEMIMAGESIZE,
                            YMARGIN + y * GEMIMAGESIZE,
                            GEMIMAGESIZE,
                            GEMIMAGESIZE))
        BOARDCELLS[x].append(r)

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Load the images
GEMIMAGES = []
for i in range(1, len(GEMS)+1):
    gemImage = pygame.image.load('res/gem%s.png' % i)
    if gemImage.get_size() != (GEMIMAGESIZE, GEMIMAGESIZE):
        gemImage = pygame.transform.smoothscale(gemImage, (GEMIMAGESIZE, GEMIMAGESIZE))
    GEMIMAGES.append(gemImage)

def main():
    # initialize pygame
    pygame.init()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    pygame.display.set_caption('Dejeweled')
    
    BOARD = [[random.randrange(len(GEMS)) for c in range(WIDTH)] for r in range(HEIGHT)]
    SCORE = MOVES = GEMS_CLEARED = CASCADES = 0

    # clear spawned matches
    while get_matches(BOARD) != []:
        for match in get_matches(BOARD):
            for gem in match:
                BOARD[gem[1]][gem[0]] = random.randrange(len(GEMS))

    # game loop
    while True:
        # check if the current board has valid moves
        if not get_valid_swaps(BOARD): break

        if PRINT_BOARDS:
            print("\nscore: ", SCORE)
            print_board(BOARD)

        # check if the user quit
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        # get next swap
        if USER_INPUT:
            print("enter pairs to swap: x1 y1 x2 y2")
            coords = [int(val) for val in input().split(" ")]
        else:
            current_node = Node(BOARD, SCORE, 0)
            coords = current_node.get_next_swap(AGENT)
        
        MOVES += 1

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

        # draw the board
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(BOARD)

        # draw the score
        scoreImg = BASICFONT.render(str(SCORE), 1, SCORECOLOR)
        scoreRect = scoreImg.get_rect()
        scoreRect.bottomleft = (10, WINDOWHEIGHT - 6)
        DISPLAYSURF.blit(scoreImg, scoreRect)

        # draw the name of the agent
        agentImg = BASICFONT.render(str(AGENT), 1, SCORECOLOR)
        agentRect = agentImg.get_rect()
        agentRect.bottomright = (WINDOWWIDTH - 10, WINDOWHEIGHT - 6)
        DISPLAYSURF.blit(agentImg, agentRect)

        # update the display
        pygame.display.update()

    print("GAME OVER")
    print_board(BOARD)
    print("agent:          ", AGENT)
    print("final score:    ", SCORE)
    print("moves:          ", MOVES)
    print("gems cleared:   ", GEMS_CLEARED)
    print("cascades:       ", CASCADES)
    print("avg gems/move:  ", float(GEMS_CLEARED) / float(MOVES))
    print("avg score/move: ", float(SCORE) / float(MOVES))

    wait_on_user()

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

def get_valid_swaps(board):
    '''
    Return a list of pairs to swap
    '''
    swaps = set()

    # X represents a gem of a specific type
    for x in range(WIDTH):
        for y in range(HEIGHT):
            current_gem = board[y][x]
            if(current_gem == get_gem(board, x+1, y) != " "):
                # Case  _ X x _
                # check left up
                if(current_gem == get_gem(board, x-1, y-1)):
                    swaps.add((x-1, y-1, x-1, y))
                # check left down
                if(current_gem == get_gem(board, x-1, y+1)):
                    swaps.add((x-1, y, x-1, y+1))
                # check left left
                if(current_gem == get_gem(board, x-2, y)):
                    swaps.add((x-2, y, x-1, y))
                # check right up
                if(current_gem == get_gem(board, x+2, y-1)):
                    swaps.add((x+2, y-1, x+2, y))
                # check right down
                if(current_gem == get_gem(board, x+2, y+1)):
                    swaps.add((x+2, y, x+2, y+1))
                # check right right
                if(current_gem == get_gem(board, x+3, y)):
                    swaps.add((x+2, y, x+3, y))

            elif(current_gem == get_gem(board, x+2, y) != " "):
                # Case X _ x
                # check down
                if(current_gem == get_gem(board, x+1, y+1)):
                    swaps.add((x+1, y, x+1, y+1))
                # check up
                if(current_gem == get_gem(board, x+1, y-1)):
                    swaps.add((x+1, y, x+1, y-1))

            if(current_gem == get_gem(board, x, y+1) != " "):
                # Case _
                #      X
                #      x
                #      _
                # Check up right
                if(current_gem == get_gem(board, x+1, y-1)):
                    swaps.add((x, y-1, x+1, y-1))

                # Check up left
                if(current_gem == get_gem(board, x-1, y-1)):
                    swaps.add((x, y-1, x-1, y-1))

                # Check up up
                if(current_gem == get_gem(board, x, y-2)):
                    swaps.add((x, y-2, x, y-1))

                # Check down left
                if(current_gem == get_gem(board, x-1, y+2)):
                    swaps.add((x-1, y+2, x, y+2))

                # Check down right
                if(current_gem == get_gem(board, x+1, y+2)):
                    swaps.add((x, y+2, x+1, y+2))

                # Check down down
                if(current_gem == get_gem(board, x, y+3)):
                    swaps.add((x, y+2, x, y+3))

            elif(current_gem == get_gem(board, x, y+2) != " "):
                # Case X
                #      _
                #      x
                # check left right
                if(current_gem == get_gem(board, x+1, y+1)):
                    swaps.add((x, y+1, x+1, y+1))
                if(current_gem == get_gem(board, x-1, y+1)):
                    swaps.add((x-1, y+1, x, y+1))

    return swaps

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
                board[y][x] = random.randrange(len(GEMS))
    
def print_board(board):
    for col in board:
        print("║ ", end="")
        for row in col:
            print(GEMS[row], "", end="")
        print("║")

def draw_board(board):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            pygame.draw.rect(DISPLAYSURF, GRIDCOLOR, BOARDCELLS[x][y], 1)
            DISPLAYSURF.blit(GEMIMAGES[board[y][x]], BOARDCELLS[x][y])

def wait_on_user():
    global AGENT
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                main()
            elif event.type == KEYDOWN and event.key == K_ENTER:
                if AGENT == "random": AGENT = "expectimax"
                else:                 AGENT = "random"
                main()

# essentially the max filling depth for our nodes
FILLED_LIMIT = 7

class Node:
    def __init__(self, board, score, filled_count):
        self.board = board
        self.score = score
        self.filled_count = filled_count # probability = 1/(7^filled_count)

    def get_successors(self):
        successors = []
        next_successors = [self]

        while next_successors != []:
            next_node = next_successors.pop()
            matches = get_matches(next_node.board)

            # check if cascaded fully
            if matches != []:
                successors.append(next_node)
                continue

            # clear matches
            number_of_spaces = 0
            for match in matches:
                for gem in match:
                    next_node.score += (10 + (len(match) - 3) * 10) # bonus points here?
                    if next_node.board[gem[1]][gem[0]] != " ":
                        number_of_spaces += 1
                        next_node.board[gem[1]][gem[0]] = " "

            # drop gems
            apply_gravity(next_node.board)

            # create and fill new nodes
            for combo in combinations_with_replacement(GEMS, number_of_spaces):
                filled_count = new_node.filled_count + number_of_spaces
                # check for low-probability nodes
                if filled_count > FILLED_LIMIT: continue

                new_node = Node(next_node.board, next_node.score, filled_count)

                index = 0
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if new_node.board[y][x] == " ":
                            new_node.board[y][x] = combo[index]
                            index += 1
                next_successors.append(new_node)
            
        return successors

    def util_value(self):
        score = self.score / 10
        swaps = len(get_valid_swaps(self.board))
        return 0.5 * score + 0.75 * swaps

    def exp_value(self):
        successors = self.get_successors()

        # Check for terminal state
        if successors == []:
            return self.util_value()

        value = 0
        for succ in successors:
            p = len(GEMS) ** -succ.filled_count # switch to actual prob
            value += p * self.util_value()
        return value

    def get_next_swap(self, agent="expectimax"):
        choice = 0, 0, 0, 0
        valid_swaps = get_valid_swaps(self.board)

        if not valid_swaps:
            return choice

        if agent == "expectimax":
            best = -1e7
            for swap in valid_swaps:
                x1, y1, x2, y2 = swap

                swapped_board = copy.deepcopy(self.board)
                swap_gems(swapped_board, x1, y1, x2, y2)
                swapped_node = Node(swapped_board, 0, 0)
                score = swapped_node.exp_value()
                
                if score > best:
                    choice = swap
                    best = score

        elif agent == "random":
            choice = random.sample(valid_swaps,1)[0]

        return choice

if __name__ == "__main__":
    main()