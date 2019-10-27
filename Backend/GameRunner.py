from Game import Game,GridWorld, ToyWorld
from QAgent import QAgent, QAgentLambda, QAgentNumpy
import matplotlib.pyplot as plt

import numpy as np







size = (20,20)
game = ToyWorld(*size)
agent = QAgentNumpy(game, (4,20,20), default = 0, epsilon = .1, alpha = .5, gamma = .99)
#agent = QAgent(game, default = -1, epsilon = .01, alpha = .1, gamma = .99)



for i in range(20):
    i = np.random.randint(size[1]*size[0])
    loc = (i // size[1], i % size[0])
    if(game.is_empty(loc)):
        game.add_block(loc)

for i in range(15):
    i = np.random.randint(size[1]*size[0])
    loc = (i // size[1], i % size[0])
    if(game.is_empty(loc)):
        game.add_wall(loc)

for i in range(15):
    i = np.random.randint(size[1]*size[0])
    loc = (i // size[1], i % size[0])
    if(game.is_empty(loc)):
        game.add_bomb(loc)


game.save_initial_state()

state = game.get_start_state()
plt.show()

for episode in range(10000):
    for step in range(100):
        action = agent.select_next_action(state)
        next_state = game.transition(state,action)
        reward = game.reward(state,action)
        agent.update(state,action,reward,next_state)
        state = next_state


        if game.is_end(state) or episode > 500 and episode % 50 == 0:
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
