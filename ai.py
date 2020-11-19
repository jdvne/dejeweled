import copy, random
from itertools import combinations_with_replacement
import dejeweled


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
            matches = dejeweled.get_matches(next_node.board)

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
            dejeweled.apply_gravity(next_node.board)

            # create and fill new nodes
            for combo in combinations_with_replacement(dejeweled.GEMS, number_of_spaces):
                filled_count = new_node.filled_count + number_of_spaces
                # check for low-probability nodes
                if filled_count > FILLED_LIMIT: continue

                new_node = Node(next_node.board, next_node.score, filled_count)

                index = 0
                for x in range(dejeweled.WIDTH):
                    for y in range(dejeweled.HEIGHT):
                        if new_node.board[y][x] == " ":
                            new_node.board[y][x] = combo[index]
                            index += 1
                next_successors.append(new_node)
            
        return successors

    def util_value(self):
        score = self.score / 10
        swaps = len(dejeweled.get_valid_swaps(self.board))
        return 0.5 * score + 0.75 * swaps

    def exp_value(self):
        successors = self.get_successors()

        # Check for terminal state
        if successors == []:
            return self.util_value()

        value = 0
        for succ in successors:
            p = len(dejeweled.GEMS) ** -succ.filled_count # switch to actual prob
            value += p * self.util_value()
        return value

    def get_next_swap(self, agent="expectimax"):
        choice = 0, 0, 0, 0
        valid_swaps = dejeweled.get_valid_swaps(self.board)

        if not valid_swaps:
            return choice

        if agent == "expectimax":
            best = -1e7
            for swap in valid_swaps:
                x1, y1, x2, y2 = swap

                swapped_board = copy.deepcopy(self.board)
                dejeweled.swap_gems(swapped_board, x1, y1, x2, y2)
                swapped_node = Node(swapped_board, 0, 0)
                score = swapped_node.exp_value()
                
                if score > best:
                    choice = swap
                    best = score

        elif agent == "random":
            choice = random.sample(valid_swaps,1)[0]

        return choice