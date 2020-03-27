from game.move import Move

class Player():

	def move_peg(self, move):
		move.from_cell.is_open = True
		move.to_cell.is_open = False
		over_cell = self.get_over_cell(move.from_cell, move.to_cell)
		over_cell.is_open = True

	def get_over_cell(self, from_cell, to_cell):
		neighborhood_intersection = set(from_cell.get_neighbors()).intersection(set(to_cell.get_neighbors()))
		if len(neighborhood_intersection) == 1 and not from_cell in to_cell.get_neighbors():
			return list(neighborhood_intersection)[0]
		else:
			return None

	def get_legal_moves(self, board):
		legal_moves = []
		for row in board.cells: 
			for cell in row:
				if cell.is_open:
					neighbors = cell.get_neighbors()
					for over_cell in neighbors:
						if not over_cell.is_open:
							for from_cell in over_cell.get_neighbors():
								if not from_cell.is_open:
									if self.get_over_cell(from_cell, cell) == over_cell:
										legal_moves.append(Move(from_cell, cell))

		return legal_moves