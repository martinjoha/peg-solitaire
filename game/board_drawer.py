import matplotlib.pyplot as plt
import networkx as nx
import time
from game.board import *

# Simple class to visualize what happens on the board
class BoardDrawer():
	def __init__(self, board):
		self.board = board
		self.graph = self.generate_graph()
		self.positions = self.generate_node_positions()

	def generate_graph(self):
		G = nx.Graph()
		for row in self.board.cells:
			for cell in row:
				G.add_node(cell)

		G.add_edges_from(self.board.edges)
		return G

	def generate_node_positions(self):
		positions = {}
		for row in range(len(self.board.cells)):
			for column in range(len(self.board.cells[row])):
				y =  - row
				x = column - len(self.board.cells[row]) / 2
				positions[self.board.cells[row][column]] = (x, y)
		return positions


	def draw_graph(self):
		color_map = []
		for row in self.board.cells:
			for cell in row:
				color_map.append('white' if cell.is_open else 'black')
		
		nx.draw_networkx_nodes(self.graph, node_color=color_map, edge_colors='black', pos=self.positions, edgecolors='black', linewidths=2)
		nx.draw_networkx_edges(self.graph, pos=self.positions)

		plt.show()

