import gemgem
import copy

# this is the gem format for falling gems -> {'imageNum': 3, 'x': 3, 'y': 0, 'direction': 'down'}


class Node:
    def __init__(self, board, currentScore):
        self.board = board
        self.score = currentScore

    def getSuccessors(self):
        moves = getValidMoves(self.board)
        successors = []
        # execute each move on a new board
        for firstXY,secondXY in moves: # TODO CHANGE HOW THIS WORKS BECASUE WE ARENT USING COORDINATE PAIRS ANYMORE
            tempBoard = copy.deepcopy(self.board)
            # TODO make gemgem actually consider our AI's moves instead of user input
            gemgem.getSwappingGems(tempBoard,firstXY,secondXY)
            successors.append(tempBoard)

        return successors

    def expectiMax(self):
        pass


def getValidMoves(board):
    '''
    Return a list of Gems (dictionary gem things)
    '''

    # Moves is positions to swap
    moves = set()

    g = lambda x,y : {'imageNum': board[x][y],'x': x, 'y': y}

    # X represents a gem of a specific type
    for x in range(gemgem.BOARDWIDTH):
        for y in range(gemgem.BOARDHEIGHT):
            current_gem = gemgem.getGemAt(board, x, y)
            if(current_gem == gemgem.getGemAt(board, x+1, y) != None):
                # Case  _ X x _
                # check left up
                if(current_gem == gemgem.getGemAt(board, x-1, y-1)):
                    moves.add([g(x-1, y-1), g(x-1, y)])
                # check left down
                if(current_gem == gemgem.getGemAt(board, x-1, y+1)):
                    moves.add([g(x-1, y), g(x-1, y+1)])
                # check left left
                if(current_gem == gemgem.getGemAt(board, x-2, y)):
                    moves.add([g(x-2, y), g(x-1, y)])
                # check right up
                if(current_gem == gemgem.getGemAt(board, x+2, y-1)):
                    moves.add([g(x+2, y-1), g(x+2, y)])
                # check right down
                if(current_gem == gemgem.getGemAt(board, x+2, y+1)):
                    moves.add([g(x+2, y), g(x+2, y+1)])
                # check right right
                if(current_gem == gemgem.getGemAt(board, x+3, y)):
                    moves.add([g(x+2, y), g(x+3, y)])

            elif(current_gem == gemgem.getGemAt(board, x+2, y) != None):
                # Case X _ x
                # check down
                if(current_gem == gemgem.getGemAt(board, x+1, y+1)):
                    moves.add([g(x+1, y), g(x+1, y+1)])
                # check up
                if(current_gem == gemgem.getGemAt(board, x+1, y-1)):
                    moves.add([g(x+1, y), g(x+1, y-1)])

            if(current_gem == gemgem.getGemAt(board, x, y+1) != None):
                # Case _
                #      X
                #      x
                #      _
                # Check up right
                if(current_gem == gemgem.getGemAt(board, x+1, y-1)):
                    moves.add([g(x, y-1), g(x+1, y-1)])

                # Check up left
                if(current_gem == gemgem.getGemAt(board, x-1, y-1)):
                    moves.add([g(x, y-1), g(x-1, y-1)])

                # Check up up
                if(current_gem == gemgem.getGemAt(board, x, y-2)):
                    moves.add([g(x, y-2), g(x, y-1)])

                # Check down left
                if(current_gem == gemgem.getGemAt(board, x-1, y+2)):
                    moves.add([g(x-1, y+2), g(x, y+2)])

                # Check down right
                if(current_gem == gemgem.getGemAt(board, x+1, y+2)):
                    moves.add([g(x, y+2), g(x+1, y+2)])

                # Check down down
                if(current_gem == gemgem.getGemAt(board, x, y+3)):
                    moves.add([g(x, y+2), g(x, y+3)])

            elif(current_gem == gemgem.getGemAt(board, x, y+2) != None):
                # Case X
                #      _
                #      x
                # check left right
                if(current_gem == gemgem.getGemAt(board, x+1, y+1)):
                    moves.add([g(x, y+1), g(x+1, y+1)])
                if(current_gem == gemgem.getGemAt(board, x-1, y+1)):
                    moves.add([g(x-1, y+1), g(x, y+1)])

    return moves