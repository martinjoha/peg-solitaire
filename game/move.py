# simple helper class to represent the moves in the legal moves list
class Move():
	def __init__(self, from_cell, to_cell):
		self.from_cell = from_cell
		self.to_cell = to_cell

	def __repr__(self):
		return f'{str(self.from_cell)} to {str(self.to_cell)}'