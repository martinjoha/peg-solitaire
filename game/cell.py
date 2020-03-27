class Cell():
	def __init__(self, row, column, is_open):
		self.row = row
		self.column = column
		self.is_open = is_open

		self.upper_left_neighbor = None
		self.upper_right_neighbor = None
		self.middle_left_neighbor = None
		self.middle_right_neighbor = None
		self.lower_left_neighbor = None
		self.lower_right_neighbor = None

	def set_open(self):
		self.is_open = not self.is_open

	def get_neighbors(self):
		return list(set([self.upper_left_neighbor, self.upper_right_neighbor, self.middle_left_neighbor, self.middle_right_neighbor,
		 self.lower_left_neighbor, self.lower_right_neighbor]) - set([None]))

	def __repr__(self):
		return f'({self.row}, {self.column})'