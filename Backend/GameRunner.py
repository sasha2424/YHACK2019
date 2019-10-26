from Game import Game,GridWorld
from QAgent import QAgent
import matplotlib.pyplot as plt

import numpy as np







size = (5,8)
game = GridWorld(*size)
agent = QAgent(game, default = 0, alpha = .5)

def get_q_values():
    board = np.zeros(size)
    for row in range(size[0]):
        for col in range(size[1]):
            board[row][col] = agent.argmax_q((row,col))
    return board

state = game.get_start_state()

for episode in range(10000):
    for step in range(1000):
        action = agent.select_next_action(state)
        next_state = game.transition(state,action)
        reward = game.reward(state,action)
        agent.update(state,action,reward,next_state)
        state = next_state


        if game.is_goal(state) or episode > 10 and episode % 10 == 0:
            plt.imshow(get_q_values())
            plt.scatter(state[1],state[0],s=30,c='r')
            plt.title("Episode " + str(episode))
            plt.draw()
            plt.pause(.01)
            plt.cla()

        if episode == 39:
            game = GridWorld(8,5)
            size = (8,5)

        if game.is_goal(state):
            break
