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

eight_goal_state = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 0]]
default_puzzles = [trivial, very_easy, easy, doable, oh_boy, impossible]

def main():
    puzzle_mode = input("Welcome to an 8-Puzzle Solver." + '\n'
                        + "Type '1' to use a default puzzle, or '2' to create your own." + '\n')
    print(type(puzzle_mode))

    # Initialize current puzzle
    if puzzle_mode == 1:
        curr_puzzle = choose_default_puzzle()
        #choose_algorithm(choose_default_puzzle()
    if puzzle_mode == 2:
        print("Enter your own puzzle!")
        curr_puzzle = create_puzzle()

    # Print current puzzle
    print("Your init state of current puzzle:" + '\n')
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in curr_puzzle]))

    curr_algorithm = input("Enter your choice of algorithm: " + '\n'
                        + "    (1: Uniform Cost)" + '\n'
                        + "    (2: A* with the Misplaced Tile heuristic)" + '\n'
                        + "    (3: A* with the Manhattan distance heuristic)" + '\n')

    #run puzzle on a selected A* search algorithm
    run_algorithm(curr_puzzle, curr_algorithm)



def choose_default_puzzle():
    selected_difficulty = input("You choose to use a default puzzle. Please enter a desired difficulty on a scale from "
                                "0 to 5." + '\n')
    return default_puzzles[selected_difficulty]

def create_puzzle():
    temp_puzzle = []
    print("Enter your 3x3 puzzle one row at a time, with each col separated by a space")
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
    if algorithm_number == 2:
        print("You selected: A* with the Misplaced Tile heuristic" + '\n')
    if algorithm_number == 3:
        print("You selected: Manhattan distance heuristic" + '\n')


#below 2 lines are used to call main function
if __name__ == "__main__":
    main()