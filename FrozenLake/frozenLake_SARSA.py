import gym
import gym.spaces
import numpy as np
import random

import policy.table

env = gym.make('FrozenLake-v0')
all_actions = [0,1,2,3]

# Hyper parameters
gamma = 0.95
epsilon = 0.3

#intialize
step = 1
episode = 0
q = policy.table.Table()

for j in range(20000):

	epsilon = epsilon * 0.9999  # decay epsilon
	episode += 1

	# init episode
	state = env.reset()
	action = env.action_space.sample()
	if epsilon < random.random():
		action = np.argmax(q.get_q_values(state, all_actions))
	gt = 0
	
	# run episode
	while True:
		step += 1
		next_state, reward, terminated, info = env.step(action)

		# make TD target
		next_q_values = q.get_q_values(next_state, all_actions)

		if epsilon < random.random():
			next_action = np.argmax(next_q_values)
		else:
			next_action = env.action_space.sample()

		bootstrap_q_value = next_q_values[next_action]
		td_target = reward + gamma * bootstrap_q_value
		gt += reward

		# update q value
		alpha = 1/(episode**0.5) # GLIE
		q.update(alpha, state, action, td_target)

		state = next_state
		action = next_action

		if terminated:
			print("#%08d, step:%08d, epsilon %.5f gt:%d alpha:%.6f" %
			      (episode, step, epsilon, gt, alpha))
			break
