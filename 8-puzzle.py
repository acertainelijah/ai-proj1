import heapq
import Queue
import operator
from copy import copy, deepcopy

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
    print("Done with 8-puzzle!")
    print("total_nodes: " + str(total_nodes))
    print("max_in_queue: " + str(max_in_queue))
    print("goal_depth: " + str(goal_depth))

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
    #temp_puzzle = [(int(i) for i in row) & list(row) for row in temp_puzzle]
    #temp_puzzle = [int(i) for i in temp_puzzle]
    print type(temp_puzzle)
    print type(temp_puzzle[0])
    print type(temp_puzzle[0][0])
    print temp_puzzle
    return temp_puzzle


def run_algorithm(puzzle, algorithm_number):
    print('\n')
    if algorithm_number == 1:
        print("You selected: Uniform Cost" + '\n')
        uniform_cost_search(puzzle)
    if algorithm_number == 2:
        print("You selected: A* with the Misplaced Tile heuristic" + '\n')
        misplaced_tile_search(puzzle)
        #call Misplaced Tile, h = number of tiles that differ from goal state
    if algorithm_number == 3:
        print("You selected: Manhattan distance heuristic" + '\n')
        #add the distance each tile is away from the goal state

def uniform_cost_search(puzzle):
    global max_in_queue, total_nodes, goal_depth

    print("Expanding state: ")
    print_puzzle(puzzle)
    heuristic = 0
    init_node = Node(1, heuristic, puzzle)
    #add initial node to the queue
    nodes.append(init_node)
    puzzles_found.append(init_node.puzzle)
    print("Initial puzzle: ")
    print init_node.puzzle

    while len(nodes) > 0:
        max_in_queue = max(max_in_queue, len(nodes))
        node = nodes.pop(0)
        puzzles_found.append(node.puzzle)
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
            run_A_star(node, node.h, node.g) #expand function
            # run_A_star(init_node)

        # print the puzzles in init_node
        print "Done running A-star algorithm on 8-puzzle!"
        print "Printing Nodes from init_node:"
        print_node(init_node)

        # now that tree is created, traverse tree shortest path.

def misplaced_tile_search(puzzle):
    global max_in_queue, total_nodes, goal_depth

    print("Expanding state: ")
    print_puzzle(puzzle)
    heuristic = find_missing_tiles(puzzle)
    print("Number of missing tiles: " + str(heuristic))
    init_node = Node(1, heuristic, puzzle)
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
            run_A_star(node, node.h, node.g) #expand function
            # run_A_star(init_node)

        # print the puzzles in init_node
        print "Done running A-star algorithm on 8-puzzle!"
        print "Printing Nodes from init_node:"
        print_node(init_node)

def find_missing_tiles(puzzle):
    num_missing = 0
    for i in xrange(3):
        for j in xrange(3):
            if(puzzle[i][j] != 0 and puzzle[i][j] != eight_goal_state[i][j]):
                num_missing = num_missing + 1
    return num_missing




def run_A_star(start_node, h, g):
#def run_A_star(start_node, heuristic/algorithm):
    #how do I know what children to add?
    #how do I take this 8-puzzle and put it into a node data structure

    #TODO**** use a queue
    #TODO******** Instead of creating the whole tree, create the cheapest tree

    #TODO: use only one variable instead of 4
    parent_puzzle = deepcopy(start_node.puzzle)
    parent_puzzle1 = deepcopy(start_node.puzzle)
    parent_puzzle2 = deepcopy(start_node.puzzle)
    parent_puzzle3 = deepcopy(start_node.puzzle)
    #nested for loop for this?
    for i in xrange(3):
        print i
        for j in xrange(3):
            if start_node.puzzle[i][j] == 0:
                blank_x = j
                blank_y = i
                print "Init Blank x and y: "
                print blank_x
                print '\n'
                print blank_y
                print start_node.puzzle[i][j]

    if((blank_x < 3 and blank_y - 1 < 3) and (blank_x >= 0 and blank_y - 1 >= 0 )): #swap blank tile with tile 'Up'
        up_child = create_child(list(parent_puzzle), "up", blank_x, blank_y, h, g)
        # check if child exists, add if doesn't exist
        node_exists = False
        # iterate through and find
        if up_child.puzzle in puzzles_found:
            node_exists = True
            print("Down Node already exists! Not pushing")

        if node_exists == False:
            print("Pushing Up Node!")
            start_node.add_child(up_child)
            nodes.append(up_child)
            puzzles_found.append(up_child)

    if ((blank_x < 3 and blank_y + 1 < 3) and (blank_x >= 0 and blank_y + 1 >= 0)):  # swap blank tile with tile 'Down'
        down_child = create_child(list(parent_puzzle1), "down", blank_x, blank_y, h, g)
        # check if child exists, add if doesn't exist
        node_exists = False
        # iterate through and find
        if down_child.puzzle in puzzles_found:
            node_exists = True
            print("Down Node already exists! Not pushing")

        if node_exists == False:
            print("Pushing Down Node!")
            start_node.add_child(down_child)
            nodes.append(down_child)
            puzzles_found.append(down_child)

    #add states for moving blank up, down, left, or right
    if ((blank_x + 1 < 3 and blank_y < 3) and (blank_x + 1 >= 0 and blank_y >= 0)):  # swap blank tile with tile 'Right'
        right_child = create_child(list(parent_puzzle3), "right", blank_x, blank_y, h, g)
        # check if child exists, add if doesn't exist
        node_exists = False
        # iterate through and find
        if right_child.puzzle in puzzles_found:
            node_exists = True
            print("Right Node already exists! Not pushing")

        if node_exists == False:
            print("Pushing Right Node!")
            start_node.add_child(right_child)
            nodes.append(right_child)
            puzzles_found.append(right_child)


    if ((blank_x - 1 < 3 and blank_y < 3) and (blank_x - 1 >= 0 and blank_y >= 0)):  # swap blank tile with tile 'Left'
        left_child = create_child(list(parent_puzzle2), "left", blank_x, blank_y, h, g)
        # check if child exists, add if doesn't exist
        node_exists = False
        if left_child.puzzle in puzzles_found:
            node_exists = True
            print("Left Node already exists! Not pushing")

        if node_exists == False:
            print("Pushing Left Node!")
            start_node.add_child(left_child)
            nodes.append(left_child)
            puzzles_found.append(left_child)






    #todo output like this: print("The best state to expand with a g(n) = 1 and h(n) = 4 is")

def create_child(puzzle, swap_index, blank_x, blank_y, h, g):
    child_puzzle = list(puzzle)
    new_x = 4
    new_y = 4
    blank_x = int(blank_x)
    blank_y = int(blank_y)
    print swap_index
    print "Blank x and y: "
    print blank_x
    print '\n'
    print blank_y
    print '\n'
    if swap_index == "up":
        # y - 1 goes up
        new_x, new_y = blank_x, blank_y - 1
        print("new_x: " + str(new_x) + " new_y: " + str(new_y) + '\n')
    if swap_index == "down":
        # y + 1 goes down
        new_x, new_y = blank_x, blank_y + 1
        print("new_x: " + str(new_x) + " new_y: " + str(new_y) + '\n')
    if swap_index == "left":
        # x - 1 goes left
        new_x, new_y = blank_x - 1, blank_y
        print("new_x: " + str(new_x) + " new_y: " + str(new_y) + '\n')
    if swap_index == "right":
        # x + 1 goes right
        new_x, new_y = blank_x + 1, blank_y
        print("new_x: " + str(new_x) + " new_y: " + str(new_y) + '\n')


    print new_x
    print new_y
    print blank_x
    print blank_y
    #swap blank to swap_index to create child puzzle
    tmp = child_puzzle[new_y][new_x]
    child_puzzle[new_y][new_x] = child_puzzle[blank_y][blank_x]
    child_puzzle[blank_y][blank_x] = tmp
    print tmp
    print child_puzzle[new_y][new_x]
    print child_puzzle[blank_y][blank_x]
    print "Child Puzzle for " + swap_index
    print_puzzle(child_puzzle)
    print ""
    #child_puzzle[new_x][new_y], child_puzzle[blank_x][blank_y] = child_puzzle[blank_x][blank_y], child_puzzle[new_x][new_y]
    # if(child_puzzle == eight_goal_state): #if goal state, done!
    #     print("Goal!")
    return Node(g + 1, h, child_puzzle)
    # else:
    #     print("Not Goal :( keep going!!!")
    #     run_A_star(Node(1, 0, 0, child_puzzle))



def print_node(start_node):
    # print(start_node.puzzle)
    print_puzzle(start_node.puzzle)
    print("=== Printing Children ===" + '\n')
    for c in start_node.children:
        print print_node(c)



class Node(object):
    def __init__(self, g, h, puzzle):
        self.g = g  # cost to next node
        self.h = h  # heuristic value from goal state
        self.f = g + h  # f = g + h
        self.puzzle = puzzle
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)



#below 2 lines are used to call main function
if __name__ == "__main__":
    main()