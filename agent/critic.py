import random 
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim



class Critic():
	def __init__(self, learning_rate, trace_decay_factor, discount_factor):
		self.value_function = {}
		self.eligibilities = {}
		self.trace_decay_factor = trace_decay_factor
		self.learning_rate = learning_rate
		self.discount_factor = discount_factor
		self.td_error = None
	
	def get_td_error(self):
		return self.td_error

	
class TableBasedCritic(Critic):
	def __init__(self, learning_rate, trace_decay_factor, discount_factor):
		super().__init__(learning_rate, trace_decay_factor, discount_factor)

	def set_init_state(self, state):
		self.value_function[state] = random.random() * .01
		self.eligibilities[state] = 1

	def calculate_td_error(self, prev_state, state, reward):
		try:
			self.value_function[state]
		
		except KeyError:
			self.value_function[state] = random.random() * .01

		self.td_error = reward + self.discount_factor * self.value_function[state] - self.value_function[prev_state]
	

	def reset_eligibilities(self):
			self.eligibilities = {}

	def update_value_function(self, state):
		try:
			self.value_function[state] += self.learning_rate * self.td_error * self.eligibilities[state]

		except KeyError:
			self.set_init_state(state)
			self.update_value_function(state)
		
	def update_eligibilities(self, state):
		try: 
			self.eligibilities[state] *= self.discount_factor * self.trace_decay_factor

		except KeyError:
			self.set_init_state(state)
			self.update_eligibilities(state)


	def set_eligibilities(self, state):
		self.eligibilities[state] = 1

	def update(self, state):
		self.update_value_function(state)
		self.update_eligibilities(state)


class NeuralNetBasedCritic(Critic):
	def __init__(self, learning_rate, trace_decay_factor, discount_factor, nn_dims):
		super().__init__(learning_rate, trace_decay_factor, discount_factor)
		self.nn_dims = nn_dims
		self.network = None
		self.loss = None

	def calculate_target(self, state, reward):
		return reward + self.forward(state)
	
	def set_td_error(self, prev_state, state, reward):
		self.td_error = self.calculate_target(state, reward) - self.forward(prev_state)

	def get_td_error(self):
		return self.td_error[0]

	def calculate_loss(self):
		return self.td_error ** 2

	def initialize_eligibilities(self):
		self.eligibilities = []
		for layer in self.network.parameters():

			self.eligibilities.append(T.zeros(layer.shape))

	def update_eligibilities(self):
		for i, layer in enumerate(self.network.layers):
			self.eligibilities[i] = T.add(self.eligibilities[i], layer.weight.grad)

	def reset_eligibilities(self):
		self.initialize_eligibilities()

	def update_weights(self):
		for i, layer in enumerate(self.network.layers):
			eligibility_trace = self.discount_factor * self.learning_rate * self.eligibilities[i]
			layer = T.add(layer.weight, eligibility_trace)

	def convert_state_to_tensor(self, state):
		char_list = [float(char) for char in state]
		return T.tensor(char_list)

	def forward(self,state):
		x = F.relu(self.network.layers[0](state))
		for layer in self.network.layers[1:]:
			x = F.relu(layer(x))
		return x

	def propagate(self, prev_state, current_state, reward):
		prev_state = self.convert_state_to_tensor(prev_state)
		current_state = self.convert_state_to_tensor(current_state)
		self.set_td_error(prev_state, current_state,reward)
		loss = self.calculate_loss()
		loss.backward()
		self.network.optimizer.step()
		
	def set_init_state(self, state):
		self.network = NeuralNet(self.nn_dims, len(state), self.learning_rate)
		self.initialize_eligibilities()

	def update(self, state):
		self.update_eligibilities()
		self.update_weights()

class NeuralNet(nn.Module):
	def __init__(self, nn_dims, input_dims, learning_rate):
		super(NeuralNet, self).__init__()
		self.layers = nn.ModuleList()
		# add first layer
		self.layers.append(nn.Linear(input_dims, nn_dims[0], bias=False))
		#add hidden layers
		for i, layer in enumerate(nn_dims[:-1]):
			self.layers.append(nn.Linear(nn_dims[i], nn_dims[i + 1], bias=False))
		
		# add output layer
		self.layers.append(nn.Linear(nn_dims[-1], 1, bias=False))

		self.optimizer = optim.SGD(self.layers.parameters(), lr=learning_rate)