from Game import Game,GridWorld, ToyWorld
from QAgent import QAgent, QAgentLambda, QAgentNumpy
import matplotlib.pyplot as plt

import numpy as np







size = (20,20)
game = ToyWorld(*size)
agent = QAgentNumpy(game, (4,20,20), default = 0, epsilon = 0, alpha = .5, gamma = .99)
#agent = QAgent(game, default = -1, epsilon = .01, alpha = .1, gamma = .99)

"""
game.add_wall((2,8))
game.add_wall((2,7))
game.add_wall((2,6))
game.add_wall((2,5))
game.add_wall((2,4))
game.add_wall((2,3))
game.add_wall((2,2))
game.add_wall((2,1))
game.add_wall((2,0))

game.add_wall((5,9))
game.add_wall((5,8))
game.add_wall((5,7))
game.add_wall((5,6))
game.add_wall((5,5))
game.add_wall((5,4))
game.add_wall((5,3))
game.add_wall((5,2))
game.add_wall((5,1))
"""


game.add_block((5,5))
game.add_block((4,6))
game.add_block((6,4))
game.add_block((3,7))
game.add_block((7,3))
game.add_block((8,2))
game.add_block((2,8))


game.add_wall((6,8))
game.add_wall((8,6))
game.add_wall((4,8))
game.add_wall((8,4))
game.add_wall((4,4))

game.add_teleport((9,0),(8,8))
game.add_block((8,0))
game.add_block((6,1))
game.add_block((7,1))

game.save_initial_state()

state = game.get_start_state()
plt.show()

for episode in range(10000):
    for step in range(1000):
        action = agent.select_next_action(state)
        next_state = game.transition(state,action)
        reward = game.reward(state,action)
        agent.update(state,action,reward,next_state)
        state = next_state


        if game.is_end(state) or episode > 200 and episode % 10 == 0:
            #board = np.zeros((10,10))
            #for row in range(10):
            #    for col in range(10):
            #        board[row][col] = agent.argmax_q((row,col))
            board = np.max(agent.Q,axis=0)
            for wall in game.walls:
               board[wall[0],wall[1]] = None

            plt.imshow(board,origin='lower')
            plt.scatter(state[1],state[0],s=30,c='r',marker="o")
            for bomb in game.bombs:
                plt.scatter(bomb[1],bomb[0],s=60,c='r',marker="v")

            for block in game.blocks:
                plt.scatter(block[1],block[0],s=60,c='r',marker="X")

            for i,teleport in enumerate(game.teleports):
                plt.scatter(teleport[1],teleport[0],s=60,c='r',marker="1")
                plt.scatter(teleport[3],teleport[2],s=60,c='r',marker="2")

            plt.title("Episode " + str(episode))
            plt.draw()
            plt.pause(.01)
            plt.cla()

        if game.is_end(state):
            break
    game.reset_to_initial()
