import heapq
import Queue
import operator
import time
from copy import copy, deepcopy

start_time = time.time()

trivial = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 0]]

very_easy = [[1, 2, 3],
             [4, 5, 6],
             [7, 0, 8]]

easy = [[1, 2, 0],
        [4, 5, 3],
        [7, 8, 6]]

doable = [[0, 1, 2],
          [4, 5, 3],
          [7, 8, 6]]

oh_boy = [[8, 7, 1],
          [6, 0, 2],
          [5, 4, 3]]

impossible = [[1, 2, 3],
              [4, 5, 6],
              [8, 7, 0]]

default_puzzles = [trivial, very_easy, easy, doable, oh_boy, impossible]

eight_goal_state = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 0]]
#Global queue of Nodes
nodes = []
puzzles_found = []
#nodes = Queue.Queue()
#TODO check for repeated states!!!


#update and return these 3 variables at the end of the program
total_nodes = 0
max_in_queue = 0
goal_depth = 0



def main():
    puzzle_mode = input("Welcome to an 8-Puzzle Solver." + '\n'
                        + "Type '1' to use a default puzzle, or '2' to create your own." + '\n')
    print(type(puzzle_mode))

    # Initialize current puzzle
    if puzzle_mode == 1:
        curr_puzzle = choose_default_puzzle()
        #choose_algorithm(choose_default_puzzle()
    if puzzle_mode == 2:
        print("Enter your own puzzle, use a zero to represent the blank")
        curr_puzzle = create_puzzle()

    # Print current puzzle
    print("Your init state of current puzzle:" + '\n')
    print_puzzle(curr_puzzle)

    curr_algorithm = input("Enter your choice of algorithm: " + '\n'
                        + "    (1: Uniform Cost)" + '\n'
                        + "    (2: A* with the Misplaced Tile heuristic)" + '\n'
                        + "    (3: A* with the Manhattan distance heuristic)" + '\n')

    #run puzzle on a selected A* search algorithm
    run_algorithm(curr_puzzle, curr_algorithm)
    print("8-puzzle Program Successful!")
    print ""
    print("   To solve this problem the search algorithm expanded a total of " + str(total_nodes) + " nodes.")
    print("   The maximum number of nodes in the queue at any one time was " + str(max_in_queue) + ".")
    print("   The depth of the goal node was " + str(goal_depth) + ".")
    print("This 8-puzzle program ran in %s seconds" % (time.time() - start_time))

def print_puzzle(puzzle):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in puzzle]))

def choose_default_puzzle():
    selected_difficulty = input("You choose to use a default puzzle. Please enter a desired difficulty on a scale from "
                                "0 to 5 (with 5 being impossible!)." + '\n')
    return default_puzzles[selected_difficulty]

def create_puzzle():
    temp_puzzle = []
    print("Enter your 3x3 puzzle, one row at a time, with each column separated by a space")
    for i in xrange(3):
        temp_puzzle.append(list(int(i) for i in (raw_input('Input for row ' + str(i) + ': ').split())))
    return temp_puzzle


def run_algorithm(puzzle, algorithm_number):
    print('\n')
    if algorithm_number == 1:
        print("You selected: Uniform Cost" + '\n')
        print("Expanding state: ")
        print_puzzle(puzzle)
        uniform_cost_search(puzzle)
    elif algorithm_number == 2:
        print("You selected: A* with the Misplaced Tile heuristic" + '\n')
        print("Expanding state: ")
        print_puzzle(puzzle)
        misplaced_tile_search(puzzle)
    elif algorithm_number == 3:
        print("You selected: Manhattan distance heuristic" + '\n')
        print("Expanding state: ")
        print_puzzle(puzzle)
        manhattan_search(puzzle)

def uniform_cost_search(puzzle):
    global max_in_queue, total_nodes, goal_depth

    heuristic = 0
    f = 1 + heuristic
    init_node = Node(1, heuristic, f, puzzle)
    # add initial node to the queue
    nodes.append(init_node)
    puzzles_found.append(init_node.puzzle)

    while len(nodes) > 0:
        max_in_queue = max(max_in_queue, len(nodes))
        node = nodes.pop(0)
        puzzles_found.append(node.puzzle)

        print "The best state to expand with a g(n) = " + str(node.g) + "h(n) = " + str(node.h) + " is..."
        print print_puzzle(node.puzzle)
        print "    Expanding this node..."

        # populate init_node with children
        if node.puzzle == eight_goal_state:
            print "Goal!"
            print_puzzle(node.puzzle)
            goal_depth = node.g - 1
            break
        else:
            total_nodes = total_nodes + 1
            run_A_star(node, node.h, node.g, "uniform") # Expand function

    print "Done running A-star algorithm (Uniform) on 8-puzzle!"


def misplaced_tile_search(puzzle):
    global max_in_queue, total_nodes, goal_depth

    heuristic = find_missing_tiles(puzzle)
    print("Number of missing tiles: " + str(heuristic))
    f = 1 + heuristic
    init_node = Node(1, heuristic, f, puzzle)
    #add initial node to the queue
    nodes.append(init_node)
    puzzles_found.append(init_node.puzzle)
    print("Initial puzzle: ")
    print init_node.puzzle

    while len(nodes) > 0:
        nodes.sort(key=operator.attrgetter('f'))
        max_in_queue = max(max_in_queue, len(nodes))
        node = nodes.pop(0)
        puzzles_found.append(node.puzzle)

        print "The best state to expand with a g(n) = " + str(node.g) + "h(n) = " + str(node.h) + " is..."
        print_puzzle(node.puzzle)
        print "    Expanding this node..."

        # populate init_node with children
        print("Checking node puzzle")
        if node.puzzle == eight_goal_state:
            print "Goal!"
            print_puzzle(node.puzzle)
            goal_depth = node.g - 1
            break
        else:
            print "Populating Tree!"
            total_nodes = total_nodes + 1
            run_A_star(node, find_missing_tiles(node.puzzle), node.g, "misplaced") #Expand function

    # print the puzzles in init_node
    print "Done running A-star algorithm (Missing Tiles) on 8-puzzle!"

def find_missing_tiles(puzzle):
    num_missing = 0
    for i in xrange(3):
        for j in xrange(3):
            if(puzzle[i][j] != 0 and puzzle[i][j] != eight_goal_state[i][j]):
                num_missing = num_missing + 1
    return num_missing

def manhattan_search(puzzle):
    global max_in_queue, total_nodes, goal_depth

    heuristic = find_manhattan_tiles(puzzle)
    print("Cost (g) of current tile tiles: " + str(heuristic))
    f = 1 + heuristic
    init_node = Node(1, heuristic, f, puzzle)

    # add initial node to the queue
    nodes.append(init_node)
    puzzles_found.append(init_node.puzzle)
    print("Initial puzzle: ")
    print init_node.puzzle

    while len(nodes) > 0:
        nodes.sort(key=operator.attrgetter('f'))
        max_in_queue = max(max_in_queue, len(nodes))
        node = nodes.pop(0)
        puzzles_found.append(node.puzzle)

        print "The best state to expand with a g(n) = " + str(node.g) + "h(n) = " + str(node.h) + " is..."
        print_puzzle(node.puzzle)
        print "    Expanding this node..."

        # populate init_node with children
        print("Checking node puzzle")
        if node.puzzle == eight_goal_state:
            print "Goal!"
            print_puzzle(node.puzzle)
            goal_depth = node.g - 1
            break
        else:
            total_nodes = total_nodes + 1
            run_A_star(node, find_manhattan_tiles(node.puzzle), node.g, "manhattan") # Expand function

    print "Done running A-star algorithm Manhattan on 8-puzzle!"

def find_manhattan_tiles(puzzle):
    total_tiles_from_goal = 0 # This is the sum of all spaces each num is away from their goal
    for i in xrange(3):
        for j in xrange(3):
            if(puzzle[i][j] != 0 and puzzle[i][j] != eight_goal_state[i][j]):
                total_tiles_from_goal += calc_manhattan_h(puzzle[i][j], i, j)
    return total_tiles_from_goal

def calc_manhattan_h(curr_num, i, j):
    tiles_from_goal = 0
    for k in xrange(3): # search puzzle from curr_num to goal
        for l in xrange(3):
            if curr_num == eight_goal_state[k][l]:
                tiles_from_goal = abs(i - k) + abs(j - l) # this find the distance away the curr_num is from the goal
                return tiles_from_goal
    return tiles_from_goal


def run_A_star(start_node, h, g, mode):
    parent_puzzle = deepcopy(start_node.puzzle)
    parent_puzzle1 = deepcopy(start_node.puzzle)
    parent_puzzle2 = deepcopy(start_node.puzzle)
    parent_puzzle3 = deepcopy(start_node.puzzle)
    for i in xrange(3):
        for j in xrange(3):
            if start_node.puzzle[i][j] == 0:
                blank_x = j
                blank_y = i

    if((blank_x < 3 and blank_y - 1 < 3) and (blank_x >= 0 and blank_y - 1 >= 0 )): #swap blank tile with tile 'Up'
        up_child = create_child(list(parent_puzzle), "up", blank_x, blank_y, h, g, mode)
        # check if child exists, add if doesn't exist
        node_exists = False
        # iterate through and find
        if up_child.puzzle in puzzles_found:
            node_exists = True

        if node_exists == False:
            start_node.add_child(up_child)
            nodes.append(up_child)
            puzzles_found.append(up_child)

    if ((blank_x < 3 and blank_y + 1 < 3) and (blank_x >= 0 and blank_y + 1 >= 0)):  # swap blank tile with tile 'Down'
        down_child = create_child(list(parent_puzzle1), "down", blank_x, blank_y, h, g, mode)
        # check if child exists, add if doesn't exist
        node_exists = False
        # iterate through and find
        if down_child.puzzle in puzzles_found:
            node_exists = True

        if node_exists == False:
            start_node.add_child(down_child)
            nodes.append(down_child)
            puzzles_found.append(down_child)

    #add states for moving blank up, down, left, or right
    if ((blank_x + 1 < 3 and blank_y < 3) and (blank_x + 1 >= 0 and blank_y >= 0)):  # swap blank tile with tile 'Right'
        right_child = create_child(list(parent_puzzle3), "right", blank_x, blank_y, h, g, mode)
        # check if child exists, add if doesn't exist
        node_exists = False
        # iterate through and find
        if right_child.puzzle in puzzles_found:
            node_exists = True

        if node_exists == False:
            start_node.add_child(right_child)
            nodes.append(right_child)
            puzzles_found.append(right_child)


    if ((blank_x - 1 < 3 and blank_y < 3) and (blank_x - 1 >= 0 and blank_y >= 0)):  # swap blank tile with tile 'Left'
        left_child = create_child(list(parent_puzzle2), "left", blank_x, blank_y, h, g, mode)
        # check if child exists, add if doesn't exist
        node_exists = False
        if left_child.puzzle in puzzles_found:
            node_exists = True

        if node_exists == False:
            start_node.add_child(left_child)
            nodes.append(left_child)
            puzzles_found.append(left_child)

def create_child(puzzle, swap_index, blank_x, blank_y, h, g, mode):
    child_puzzle = list(puzzle)
    new_x = 4
    new_y = 4
    blank_x = int(blank_x)
    blank_y = int(blank_y)

    if swap_index == "up":
        # y - 1 goes up
        new_x, new_y = blank_x, blank_y - 1
    elif swap_index == "down":
        # y + 1 goes down
        new_x, new_y = blank_x, blank_y + 1
    elif swap_index == "left":
        # x - 1 goes left
        new_x, new_y = blank_x - 1, blank_y
    elif swap_index == "right":
        # x + 1 goes right
        new_x, new_y = blank_x + 1, blank_y


    # swap blank to swap_index to create child puzzle
    tmp = child_puzzle[new_y][new_x]
    child_puzzle[new_y][new_x] = child_puzzle[blank_y][blank_x]
    child_puzzle[blank_y][blank_x] = tmp

    # change the value of h
    if mode == "misplaced":
        h = find_missing_tiles(child_puzzle)
    elif mode == "manhattan":
        h = find_manhattan_tiles(child_puzzle)

    # set the value of f for the child node
    f = (g + 1) + h


    return Node(g + 1, h, f, child_puzzle)


class Node(object):
    def __init__(self, g, h, f, puzzle):
        self.g = g  # cost to next node
        self.h = h  # heuristic value from goal state
        self.f = f  # f = g + h
        self.puzzle = puzzle
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)



# Below 2 lines are used to call main function
if __name__ == "__main__":
    main()