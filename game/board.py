from game.cell import *
import random

class Board():
	def __init__(self, size, open_cells=[(3,2)]): #open cells is just an integer to indicate the initial open cells
		self.cells = []
		self.size = size
		self.edges = [] # pairs of edges between cells
		self.open_cells = open_cells


	def add_edges(self, cell1, cell2):
		self.edges.append((cell1, cell2))
		

	def set_open_cells(self, open_cells):
		self.open_cells = open_cells

	def set_initial_open_cells(self):
		for open_cell in self.open_cells:
			self.cells[open_cell[0]][open_cell[1]].is_open = True
	
	def set_initial_open_cells_random(self):
		open_cells_remaining = self.open_cells

		while open_cells_remaining > 0:
			random_row = random.choice(self.cells)
			random_cell = random.choice(random_row)
			if random_cell.is_open:
				continue
			random_cell.is_open = True
			open_cells_remaining -= 1
	
	def reset(self):
		for row in self.cells:
			for cell in row:
				cell.is_open = False
		self.set_initial_open_cells()


	def get_open_cell_count(self):
		open_cells = 0 
		for row in self.cells:
			for cell in row:
				open_cells += 1 if cell.is_open else 0

		return open_cells
	
	def get_closed_cell_count(self):
		closed_cells = 0
		for row in self.cells:
			for cell in row:
				closed_cells += 1 if not cell.is_open else 0
		
		return closed_cells


	def encode_board(self):
		bit_string = ''
		for row in self.cells:
			for cell in row:
				bit_string += '1' if cell.is_open else '0'

	def __repr__(self):
		return str(self.cells)

class TriangularBoard(Board):
	def __init__(self, size, open_cells=1):
		super().__init__(size, open_cells)
		self.generate_cells()
		self.generate_edges()
		self.set_initial_open_cells()

	def generate_cells(self):
		self.cells = [[Cell(i, j, False) for j in range(1, i + 1)] for i in range(1, self.size + 1)]

	def generate_edges(self):
		for row in range(len(self.cells)):
			for column in range(len(self.cells[row])):
				if row < self.size - 1:
					self.cells[row][column].lower_left_neighbor = self.cells[row + 1][column]
					self.cells[row + 1][column].upper_right_neighbor = self.cells[row][column]
					self.cells[row][column].lower_right_neighbor = self.cells[row + 1][column + 1]
					self.cells[row + 1][column + 1].upper_left_neighbor = self.cells[row][column]
					self.cells[row][column].lower_left_neighbor = self.cells[row + 1][column]
					self.add_edges(self.cells[row][column], self.cells[row + 1][column])		
					self.add_edges(self.cells[row][column], self.cells[row + 1][column + 1])		

				if column < len(self.cells[row]) - 1:
					self.cells[row][column].middle_right_neighbor = self.cells[row][column + 1]
					self.cells[row][column + 1].middle_left_neighbor = self.cells[row][column]
					self.add_edges(self.cells[row][column], self.cells[row][column + 1])


class DiamondBoard(Board):
	def __init__(self, size, open_cells=1):
		super().__init__(size, open_cells)
		self.generate_cells()
		self.generate_edges()
		self.set_initial_open_cells()

	def generate_cells(self):
		upper_rows = [[Cell(i, j, False) for j in range(1, i + 1)] for i in range(1, self.size)]
		middle_row = [Cell(self.size, i, False) for i in range(1, self.size + 1)]
		lower_rows = [[Cell(i, j, False) for j in range(1, self.size * 2 - i + 1)] for i in range(self.size * 2 - 1, self.size, -1)]
		self.cells = upper_rows + [middle_row] + lower_rows[::-1]

	def generate_edges(self):
		#generate upper half of diamond
		for row in range(self.size):
			for column in range(len(self.cells[row])):
				if row < self.size - 1:
					self.cells[row][column].lower_left_neighbor = self.cells[row + 1][column]
					self.cells[row + 1][column].upper_right_neighbor = self.cells[row][column]
					self.cells[row][column].lower_right_neighbor = self.cells[row + 1][column + 1]
					self.cells[row + 1][column + 1].upper_left_neighbor = self.cells[row][column]
					self.cells[row][column].lower_left_neighbor = self.cells[row + 1][column]
					self.add_edges(self.cells[row][column], self.cells[row + 1][column])		
					self.add_edges(self.cells[row][column], self.cells[row + 1][column + 1])		

				if column < len(self.cells[row]) - 1:
					self.cells[row][column].middle_right_neighbor = self.cells[row][column + 1]
					self.cells[row][column + 1].middle_left_neighbor = self.cells[row][column]
					self.add_edges(self.cells[row][column], self.cells[row][column + 1])

		for row in range(len(self.cells) - 1, self.size - 1, -1):
			for column in range(len(self.cells[row])):
				self.cells[row][column].upper_left_neighbor = self.cells[row - 1][column]
				self.cells[row - 1][column].lower_right_neighbor = self.cells[row][column]
				self.cells[row][column].upper_right_neighbor = self.cells[row - 1][column + 1]
				self.cells[row - 1][column + 1].lower_left_neighbor = self.cells[row][column]
				self.add_edges(self.cells[row][column], self.cells[row - 1][column])
				self.add_edges(self.cells[row][column], self.cells[row - 1][column + 1])

				if column < len(self.cells[row]) - 1:
					self.cells[row][column].middle_right_neighbor = self.cells[row][column + 1]
					self.cells[row][column + 1].middle_left_neighbor = self.cells[row][column]
					self.add_edges(self.cells[row][column], self.cells[row][column + 1])
		