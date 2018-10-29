import TreeNode
import heapq as min_heap_esque_queue # because it sort of acts like a min heap

trivial = [[1, 2, 3],
 	[4, 5, 6],
 	[7, 8, 0]]
veryEasy = [[1, 2, 3],
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

def main():

puzzle_mode = input("Welcome to an 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own."+ '\n')
	if puzzle_mode == "1":
 		select_and_init_algorithm(init_default_puzzle_mode())
 	if puzzle_mode == "2":

def select_and_init_algorithm(puzzle):
