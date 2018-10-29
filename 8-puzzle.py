import heapq

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
        #call Misplaced Tile, h = number of tiles that differ from goal state
    if algorithm_number == 3:
        print("You selected: Manhattan distance heuristic" + '\n')
        #add the distance each tile is away from the goal state

def uniform_cost_search(puzzle):
    print("Expanding state: ")
    print_puzzle(puzzle)
    init_node = Node(1,0,0, puzzle)
    print("Initial puzzle: ")
    print init_node.puzzle

    # populate init_node with children
    run_A_star(init_node)

    # print the puzzles in init_node
    print_node(init_node)


def run_A_star(start_node):
    #how do I know what children to add?
    #how do I take this 8-puzzle and put it into a node data structure

    #nested for loop for this?
    for i in xrange(3):
        for j in xrange(3):
            if start_node.puzzle[i][j] == 0:
                blank_x = i
                blank_y = j

    #add states for moving blank up, down, left, or right
    if((blank_x < 3 or blank_y - 1 < 3) and (blank_x >= 0 or blank_y - 1 >= 0 )): #swap blank tile with tile up
        start_node.add_child( create_child(start_node.puzzle, "up", blank_x, blank_y) )
    if ((blank_x < 3 or blank_y + 1 < 3) and (blank_x >= 0 or blank_y + 1 >= 0)):  # swap blank tile with tile up
        start_node.add_child( create_child(start_node.puzzle, "down", blank_x, blank_y) )
    if ((blank_x - 1 < 3 or blank_y < 3) and (blank_x - 1 >= 0 or blank_y >= 0)):  # swap blank tile with tile up
        start_node.add_child( create_child(start_node.puzzle, "left", blank_x, blank_y) )
    if ((blank_x + 1 < 3 or blank_y < 3) and (blank_x + 1 >= 0 or blank_y >= 0)):  # swap blank tile with tile up
        start_node.add_child( create_child( start_node.puzzle, "right", blank_x, blank_y) )

    print("The best state to expand with a g(n) = 1 and h(n) = 4 is")

def create_child(puzzle, swap_index, blank_x, blank_y):
    child_puzzle = puzzle
    new_x = 4
    new_y = 4
    blank_x = int(blank_x)
    blank_y = int(blank_y)
    print "Blank x and y: "
    print blank_x
    print '\n't
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

    child_puzzle[new_x, new_y], child_puzzle[blank_x, blank_y] = child_puzzle[blank_x, blank_y], child_puzzle[new_x, new_y]
    return child_puzzle

def print_node(start_node):
    print(start_node.puzzle)
    print("=== Printing Children ===" + '\n')
    for c in init_node.children:
        print print_node(c.puzzle)



class Node(object):
    def __init__(self, g, h, f, puzzle):
        self.g = g  # cost to next node
        self.h = h  # heuristic value from goal state
        self.f = f  # f = g + h
        self.puzzle = puzzle
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)



#below 2 lines are used to call main function
if __name__ == "__main__":
    main()