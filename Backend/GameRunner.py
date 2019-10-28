from Game import Game,GridWorld, ToyWorld
from QAgent import QAgent, QAgentLambda, QAgentNumpy
import matplotlib.pyplot as plt

import numpy as np







size = (20,20)
game = ToyWorld(*size)
agent = QAgentNumpy(game, (4,20,20), default = 0, epsilon = .1, alpha = .99, gamma = .99, lam = .5)
#agent = QAgent(game, default = -1, epsilon = .01, alpha = .1, gamma = .99)

num = (size[0] * size[1])
for i in range(num // 5):
    i = np.random.randint(1,num-1)
    loc = (i // size[0], i % size[1])
    game.add_wall(loc)

for i in range(num // 5):
    i = np.random.randint(1,num-1)
    loc = (i // size[0], i % size[1])
    game.add_block(loc)


game.add_block((1,2))

game.save_initial_state()

state = game.get_start_state()
plt.show()

for episode in range(10000):
    for step in range(400):
        action = agent.select_next_action(state)
        next_state = game.transition(state,action)
        reward = game.reward(state,action)
        agent.update(state,action,reward,next_state)
        state = next_state


        if game.is_end(state) or episode > 100 and episode % 20 == 0:
            #board = np.zeros((10,10))
            #for row in range(10):
            #    for col in range(10):
            #        board[row][col] = agent.argmax_q((row,col))
            board = np.max(agent.Q,axis=0)
            for wall in game.walls:
               board[wall[0],wall[1]] = None

            plt.imshow(board,origin='lower')
            plt.scatter(state[1],state[0],s=80,c='r',marker="o")
            for bomb in game.bombs:
                plt.scatter(bomb[1],bomb[0],s=80,c='r',marker="v")

            for block in game.blocks:
                plt.scatter(block[1],block[0],s=80,c='r',marker="X")

            for i,teleport in enumerate(game.teleports):
                plt.scatter(teleport[1],teleport[0],s=80,c='r',marker="1")
                plt.scatter(teleport[3],teleport[2],s=80,c='r',marker="2")

            plt.title("Episode " + str(episode))
            plt.draw()
            plt.pause(.01)
            plt.cla()

        if game.is_end(state):
            break
    state = game.get_start_state()
    game.reset_to_initial()
    agent.reset_E()
