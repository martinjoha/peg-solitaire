
from agent.agent import *
from game.game import *
from game.board_drawer import *
from learning_plot import *

import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

import time
def decode_board(board):
	bit_string = ''
	for row in board:
		for cell in row:
			bit_string += '1' if cell.is_open else '0'
	return bit_string


def decode_move(move):
	from_cell_row = '{:08b}'.format(move.from_cell.row)
	from_cell_column = '{:08b}'.format(move.from_cell.column)
	to_cell_row = '{:08b}'.format(move.to_cell.row)
	to_cell_column = '{:08b}'.format(move.to_cell.column)
	return f'{from_cell_row}{from_cell_column}{to_cell_row}{to_cell_column}'




def main():
	game = Game('fdsf', 4, [(4,2)])
	agent = Agent('nn', 0.05, 0.01, 0.9, 0.9, 0.9, 0.9, 0.5, 0.99, [124, 64])
	drawer = BoardDrawer(game.board)

	closed_cell_count = []
	decoded_init_state = decode_board(game.board.cells) 
	agent.set_init_state(decoded_init_state) # to set up the critic initially
	start = time.time()
	n = 1000
	for i in range(n):

		if i == n - 1: # for the last episode set epsilon to 0 to use target policy
			agent.actor.set_epsilon(0)
		init_legal_moves, _1, init_state, _2 = game.send_information()
		decoded_state = decode_board(init_state)
		decoded_actions = [decode_move(move) for move in init_legal_moves]
		agent.actor.choose_action(decoded_state, decoded_actions)
		action = agent.get_chosen_action()
		agent.update_episode(decoded_state, action)

		if i == 500:
			print('fdfd')
		while not game.is_end_state():
			chosen_action = agent.get_chosen_action()
			game.perform_decoded_move(chosen_action)
			legal_moves, prev_state, current_state, reward = game.send_information()
			decoded_moves = [decode_move(move) for move in legal_moves]
			decoded_prev_state = decode_board(prev_state)
			decoded_current_state = decode_board(current_state)
			agent.update(decoded_prev_state, decoded_current_state, decoded_moves, reward) # chose action, and update tables
		print(game.is_lost_state(), i)
		
		closed_cell_count.append(game.board.get_closed_cell_count())
		game.reset()

		if i == n - 1:
			print(time.time() - start)
			game.visualize_episode(agent.current_episode)
		agent.reset()

	draw_learning_curve(closed_cell_count)

	
		


if __name__ == '__main__':
	start = time.time()
	main()
	print(time.time() - start)
