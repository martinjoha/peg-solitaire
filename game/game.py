from game.board import *
from game.player import *
from game.move import *
from game.board_drawer import *
import random
import copy


class Game():
	def __init__(self, board_type, board_size, open_cells):

		if board_type == 'triangular':
			self.board = TriangularBoard(size=board_size, open_cells=open_cells)
		else:
			self.board = DiamondBoard(size=board_size, open_cells=open_cells)
		
		self.player = Player()
		self.drawer = BoardDrawer(self.board)
		self.prev_state = None

	def is_winning_state(self):

		return self.board.get_closed_cell_count() == 1

	def perform_decoded_move(self, decoded_move):
		self.prev_state = copy.deepcopy(self.board.cells)
		y1, x1, y2, x2  = tuple(int(decoded_move[i:i + 8], 2) for i in range(0,len(decoded_move), 8))
		move = Move(self.board.cells[y1 - 1][x1 - 1], self.board.cells[y2 - 1][x2 - 1])
		self.player.move_peg(move)

	def is_lost_state(self):
		return not self.player.get_legal_moves(self.board) and self.board.get_closed_cell_count() > 1
	
	def is_end_state(self):
		return self.is_winning_state() or self.is_lost_state()

	def get_reward(self):
		if self.is_winning_state():
			return 10000
		elif self.is_lost_state():
			return -self.board.get_open_cell_count()
		else:
			return 0

	def send_information(self):
		return self.player.get_legal_moves(self.board), self.prev_state, self.board.cells, self.get_reward()

	def reset(self):
		self.board.reset()

	def simulate_game(self): # start with random moves
		while not self.is_lost_state() and not self.is_winning_state():
			moves = self.player.get_legal_moves(self.board)
			self.player.move_peg(self.board, random.choice(moves))
			self.drawer.draw_graph()
			time.sleep(.5)
		if self.is_winning_state():

			print('Congratulations, you have won')
			self.drawer.draw_graph()
		
		if self.is_lost_state():
			print('You lost.')
			self.drawer.draw_graph()		


	def visualize_episode(self, sap):
		for action in sap[:-1]:
			self.drawer.draw_graph()
			_, move = action
			self.perform_decoded_move(move)