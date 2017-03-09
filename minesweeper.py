import sys
import random

class Board:
	def __init__(self,rows,cols,bombs):
		self.rows = rows
		self.cols = cols
		self.bombs = bombs
		self.spots_found = 0
		self.alive = True
		self.win = False

		self.board = self.empty_board()
		self.board = self.add_bombs(self.board)
		self.user_board = self.empty_board()
	
	def empty_board(self):
		board = []
		for i in range(rows):
			board.append([])
			for j in range(cols):
				board[-1].append("H")
		return board

	def add_bombs(self,board):
		bombless_spaces = []
		for i in range(self.rows):
			for j in range(self.cols):
				bombless_spaces.append([i,j])
		bombs_to_place = self.bombs
		while bombs_to_place > 0:
			i = random.randint(0,len(bombless_spaces) - 1)
			space = bombless_spaces[i]
			board[space[0]][space[1]] = "B"
			bombless_spaces.pop(i)
			bombs_to_place -= 1
		return board

	def print_board(self):
		for row in self.board:
			print " ".join(map(str,row))

	def print_user_board(self):
		for row in self.user_board:
			print " ".join(map(str,row))

	# We want to show all the bombs in the user board.
	def generate_final_board(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.board[i][j] == "B":
					self.user_board[i][j] = "B"

	def is_bomb(self, r,c):
		return self.board[r][c] == "B"

	def get_nearby_bombs(self, r,c):
		neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		count = 0
		for neighbor in neighbors:
			sq = (r + neighbor[0], c + neighbor[1])
			if sq[0] >= 0 and sq[0] < self.rows and sq[1] >= 0 and sq[1] < self.cols and self.is_bomb(sq[0],sq[1]):
				count += 1
		if count > 0:
			self.spots_found += 1
			self.user_board[r][c] = str(count)
		else:
			# If there aren't any nearby bombs, we're going to go search all the nearby spaces recursively
			self.spots_found += 1
			self.user_board[r][c] = "."
			for neighbor in neighbors:
				sq = (r + neighbor[0], c + neighbor[1])
				if sq[0] >= 0 and sq[0] < self.rows and sq[1] >= 0 and sq[1] < self.cols and self.user_board[sq[0]][sq[1]] == "H":
					self.get_nearby_bombs(sq[0],sq[1])

def get_user_input():
	row = int(raw_input("Please enter a row: "))
	col = int(raw_input("Please enter a column: "))
	return [row,col]

# Allows for large boards with few bombs on it. Resetting this is a downside of using recursion here.
sys.setrecursionlimit(10000)

rows = int(sys.argv[1])
cols = int(sys.argv[2])
bombs = int(sys.argv[3])

if bombs >= rows * cols:
	sys.exit("That is not a valid board")

board = Board(rows,cols,bombs)

print("Welcome to Minesweeper! This game is zero-indexed.")

while board.alive and not board.win:
	print("----------------------")
	board.print_user_board()
	row, col = get_user_input()
	if row < 0 or col < 0 or row >= board.rows or col >= board.cols or board.user_board[row][col] != "H":
		print("Invalid input! Try again.")
	elif board.is_bomb(row,col):
		print("You Lose!")
		board.alive = False
	else:
		board.get_nearby_bombs(row,col)
		if board.spots_found == board.rows * board.cols - bombs:
			print("You Win!")
			board.win = True

#Print the final board either way
board.generate_final_board()
board.print_user_board()
print("----------------------")
