import random

class Actor():
	def __init__(self, initial_epsilon_value, epsilon_decay_rate, discount_factor, learning_rate, trace_decay_factor):
		self.epsilon = initial_epsilon_value
		self.epsilon_decay_rate = epsilon_decay_rate
		self.discount_factor = discount_factor
		self.learning_rate = learning_rate
		self.policy = {}
		self.eligibilities = {}
		self.trace_decay_factor = trace_decay_factor
		self.td_error = None
		self.chosen_action = None

	def set_td_error(self, td_error):
		self.td_error = td_error

	def reset_eligibilities(self):
		self.eligibilities = {}

	def set_eligibilities(self, state, action):
		self.eligibilities[(state, action)] = 1

	def update_epsilon(self):
		self.epsilon *= self.epsilon_decay_rate

	def set_epsilon(self, epsilon):
		self.epsilon = epsilon

	def update_eligibilities(self, sap):
		self.eligibilities[sap] *= self.discount_factor * self.trace_decay_factor

	def update_policy(self, sap):
		try:
			self.policy[sap] += self.learning_rate * self.td_error * self.eligibilities[sap]
		
		except KeyError:
			self.policy[sap] = self.learning_rate * self.td_error * self.eligibilities[sap]

	def get_policy_for_action(self, sap):
		try:
			return self.policy[sap]

		except KeyError:
			self.policy[sap] = 0
			return self.policy[sap]

	def choose_random_action(self):
		return random.random() < self.epsilon

	def choose_action(self, state, actions):
		
		if not actions:
			self.chosen_action = None
			return 

		if self.choose_random_action():
			self.chosen_action = random.choice(actions)
			self.set_eligibilities(state, self.chosen_action)
		else:
			sap_rewards = [self.get_policy_for_action((state, action)) for action in actions]
			self.chosen_action = actions[sap_rewards.index(max(sap_rewards))]
			self.set_eligibilities(state, self.chosen_action)

	def get_chosen_action(self):
		return self.chosen_action

	def update(self, sap):

		self.update_policy(sap)
		self.update_eligibilities(sap)