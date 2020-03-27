import random 
class Critic():
	def __init__(self, learning_rate, trace_decay_factor, discount_factor):
		self.value_function = {}
		self.eligibilities = {}
		self.trace_decay_factor = trace_decay_factor
		self.learning_rate = learning_rate
		self.discount_factor = discount_factor
		self.td_error = None

	def reset_eligibilities(self):
		self.eligibilities = {}
	
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


class NeuralNetBasedCritic():
	def __init__():
		pass