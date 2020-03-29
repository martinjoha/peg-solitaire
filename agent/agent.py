from agent.actor import *
from agent.critic import *



class Agent():
	def __init__(self, critic_type,
		actor_learning_rate, critic_learning_rate,
		actor_trace_decay_factor, critic_trace_decay_factor, 
		actor_discount_factor, critic_discount_factor,
		actor_epsilon_value, actor_epsilon_decay_rate, nn_dims=[64]
		):
		self.critic_type = critic_type
		if critic_type == 'tablebasedcritic':
			self.critic = TableBasedCritic(critic_learning_rate, critic_trace_decay_factor, critic_discount_factor)
		
		elif critic_type == 'nn':
			self.critic = NeuralNetBasedCritic(critic_learning_rate, critic_trace_decay_factor, critic_discount_factor, nn_dims)
		self.actor = Actor(actor_epsilon_value, actor_epsilon_decay_rate, actor_discount_factor,
							actor_learning_rate, actor_trace_decay_factor)
		self.current_episode = []
		self.current_state = None

	def set_init_state(self, state):
		self.critic.set_init_state(state)


	def update(self, prev_state, state, actions, reward):
		self.actor.choose_action(state, actions)
		if self.critic_type == 'tablebasedcritic':
			self.critic.calculate_td_error(prev_state, state, reward)
		else: self.critic.propagate(prev_state, state, reward)
		
		self.actor.set_td_error(self.critic.td_error)
		for sap in self.current_episode:
			self.critic.update(sap[0])
			self.actor.update(sap)
		self.update_episode(state, self.actor.get_chosen_action())

	def update_episode(self, state, action):
		self.current_episode.append((state, action))
	
	def reset_episode(self):
		self.current_episode = []

	def reset(self):
		self.reset_episode()
		self.actor.reset_eligibilities()
		self.critic.reset_eligibilities()
		self.actor.update_epsilon()

	def get_chosen_action(self):
		return self.actor.get_chosen_action()
		

	def set_eligibilities(self, state, action):
		self.actor.set_eligibilities(state, action)
		self.critic.set_eligibilities(state)

	