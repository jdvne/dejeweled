import gemgem
import copy
import random


class Node:
    def __init__(self, board, currentScore,hasRandomGems,prob):
        self.board = board
        self.score = currentScore
        self.hasRandomGems = hasRandomGems
        self.probability = prob # saved as exponent, cutoff at .1%

    def getSuccessors(self):
        '''
        Return all possible board states
        [(Node,firstSwappingGem,secondSwappingGem)]
        '''

        successors = []

        for move in getValidMoves(self.board):
            firstSwappingGem, secondSwappingGem = move
            
            first = Node(copy.deepcopy(self.board),self.score,True,-99999)
            
            # Swap the gems in the board data structure.
            first.board[firstSwappingGem['x']][firstSwappingGem['y']] = secondSwappingGem['imageNum']
            first.board[secondSwappingGem['x']][secondSwappingGem['y']] = firstSwappingGem['imageNum']

            cur_successors = [first]

            while cur_successors != []:
                current = cur_successors[0]

                # get all matching gems.
                matchedGems = gemgem.findMatchingGems(current.board)

                # add to successors if board is fully cascaded
                if matchedGems != []:
                    successors.append(current)
                    cur_successors.remove(current)
                    continue

                # for each matching gem add some score and remove gem
                while matchedGems != []:
                    # Remove matched gems, then pull down the board.
                    for gemSet in matchedGems:
                        current.score += (10 + (len(gemSet) - 3) * 10)
                        for gem in gemSet:
                            current.board[gem[0]][gem[1]] = gemgem.EMPTY_SPACE

                # pull down the board (make new nodes for each possible new board
                cur_successors.extend(fillBoard(current))

                # for each new board
                    # if 

        # execute each move on a new board
        
        # for move in moves:
        #     firstSwappingGem, secondSwappingGem = move
            
        #     successorNode = Node(copy.deepcopy(self.board),self.score,True,0)

        #      # Swap the gems in the board data structure.
        #     successorNode.board[firstSwappingGem['x']][firstSwappingGem['y']] = secondSwappingGem['imageNum']
        #     successorNode.board[secondSwappingGem['x']][secondSwappingGem['y']] = firstSwappingGem['imageNum']

        #     # See if this is a matching move.
        #     matchedGems = gemgem.findMatchingGems(successorNode.board)

        #     # This was a matching move.
        #     scoreAdd = 0
        #     while matchedGems != []:
        #         # Remove matched gems, then pull down the board.

        #         # where on the screen to display text to show how many
        #         # points the player got. points is a list because if
        #         # the playergets multiple matches, then multiple points text should appear.
        #         points = []
        #         for gemSet in matchedGems:
        #             scoreAdd += (10 + (len(gemSet) - 3) * 10)
        #             for gem in gemSet:
        #                 successorNode.board[gem[0]][gem[1]] = gemgem.EMPTY_SPACE
        #             points.append({'points': scoreAdd,
        #                             'x': gem[0] * gemgem.GEMIMAGESIZE + gemgem.XMARGIN,
        #                             'y': gem[1] * gemgem.GEMIMAGESIZE + gemgem.YMARGIN})
        #         score += scoreAdd

        #         # Refill the board with new gems
        #         successorNode.board = gemgem.fillBoard(successorNode.board)

        #         # Check if there are any new matches.
        #         matchedGems = gemgem.findMatchingGems(successorNode.board)

        #     successorNode.score = utilityForSuccessors(successorNode,self)
        #     successors.append((successorNode,firstSwappingGem,secondSwappingGem)) 

        return successors

# def value(state):
#     # Check if it is a terminal state
#     if not gemgem.canMakeMove(state.board):
#         return utility(state)
        
    # If next agent is Exp

# We will start it off by calling maxValue in gemgem
# maxValue is at most called one time on the original start node because all successor states have some randomness
# maxValue will call expValue on its successors and opperate normally with that minor tweak
# As a result of this we no longer need the value function
# In the expValue function we will not call the value function because it is guarenteed that the next state will have random values and we just need to call expValue

def maxValue(state):
    pass

def expValue(state):
    pass

def utilityForSuccessors(successorState,currentState):
    '''
    Return a numerical value of a state relative to its successor state
    '''
    #state is a successor
    #lower down = higher utility
    #doesn't end game = very important
    #new moves >= moves before is very good
    #long chain
    utility = 0
    if(getValidMoves(currentState) == None):
        return -1000
    if(getValidMoves(successorState.board).length >= getValidMoves(currentState.board).length):
        utility += 1
    if(successorState.getValidMoves().length == 0):
        utility -= 1

    return utility


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


def fillBoard(node):
    '''
    deterministically fill in the empty spaces after making matches
    board -> all possible boards
    '''
    nodes = []
    
    board = node.board
    dropSlots = getDropSlots(board) # THIS IS WHAT CURRENTLY DOES THE RANDOMNESS
    while dropSlots != [[]] * gemgem.BOARDWIDTH:
        # do the dropping animation as long as there are more gems to drop
        movingGems = gemgem.getDroppingGems(board)
        for x in range(len(dropSlots)):
            if len(dropSlots[x]) != 0:
                # cause the lowest gem in each slot to begin moving in the DOWN direction
                movingGems.append({'imageNum': dropSlots[x][0], 'x': x, 'y': gemgem.ROWABOVEBOARD, 'direction': gemgem.DOWN})
        
        boardCopy = gemgem.getBoardCopyMinusGems(board, movingGems)
        gemgem.moveGems(board, movingGems)

        # Make the next row of gems from the drop slots
        # the lowest by deleting the previous lowest gems.
        for x in range(len(dropSlots)):
            if len(dropSlots[x]) == 0:
                continue
            board[x][0] = dropSlots[x][0]
            del dropSlots[x][0]
    
    return nodes

def getDropSlots(board): 
    # Creates a "drop slot" for each column and fills the slot with a
    # number of gems that that column is lacking. This function assumes
    # that the gems have been gravity dropped already.
    boardCopy = copy.deepcopy(board)
    gemgem.pullDownAllGems(boardCopy)

    dropSlots = []
    for _ in range(gemgem.BOARDWIDTH):
        dropSlots.append([])

    # count the number of empty spaces in each column on the board
    for x in range(gemgem.BOARDWIDTH):
        for y in range(gemgem.BOARDHEIGHT-1, -1, -1): # start from bottom, going up
            if boardCopy[x][y] == gemgem.EMPTY_SPACE:
                possibleGems = list(range(len(gemgem.GEMIMAGES)))
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    # Narrow down the possible gems we should put in the
                    # blank space so we don't end up putting an two of
                    # the same gems next to each other when they drop.
                    neighborGem = gemgem.getGemAt(boardCopy, x + offsetX, y + offsetY)
                    if neighborGem != None and neighborGem in possibleGems:
                        possibleGems.remove(neighborGem)

                # for each gem type (stop at a certain depth)
                    # make new board copy
                    # drop gem into spot
                    # dropSlots each

                newGem = random.choice(possibleGems)
                boardCopy[x][y] = newGem
                dropSlots[x].append(newGem)
    return dropSlots