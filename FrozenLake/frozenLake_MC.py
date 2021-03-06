import gym
import numpy as np
import random

import policy.table

env = gym.make('FrozenLake-v0')

all_actions = [0,1,2,3]

# Hyper parameters
gamma = 0.9
epsilon = 0.5
batch_size = 1

# tabular policy
q = policy.table.Table()

#initialize
step = 1
episode = 0
alpha = 1
samples = []

for j in range(20000):

	epsilon = epsilon * 0.9999  # decay epsilon
	episode += 1

	# init episode
	state = env.reset()
	trajectory = []
	gt = 0
	# run episode
	while True:
		step += 1
		
		action = env.action_space.sample()
		if epsilon < random.random():
			action = np.argmax(q.get_q_values(state, all_actions))

		next_state, reward, terminated, info = env.step(action)
		trajectory.append([state, action, reward])
		state = next_state
		gt += reward
		if terminated:
			samples.append(trajectory)
			print("#%08d, step:%08d, epsilon %.5f gt:%d alpha:%.6f" %
			      (episode, step, epsilon, gt, alpha))
			break
	
	if len(samples) > batch_size:
		alpha = 1/(episode**0.5)  # GLIE
		for trjectory in samples:
			T = len(trjectory)
			visitLog = {}
			for t in range(T):
				state = trjectory[t][0]
				if state in visitLog == False:
					visitLog[state] = True # MC with first visit
					action = trjectory[t][1]
					gt = sum([(gamma**k) * trjectory[t+k][2] for k in range(0, T-t)])				
					qVal = q.get_q_value(state, action)
					q.update(alpha, state, action, gt)
		samples = []
