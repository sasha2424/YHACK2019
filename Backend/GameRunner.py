from Game import Game,GridWorld, ToyWorld
from QAgent import QAgent, QAgentLambda, QAgentNumpy
import matplotlib.pyplot as plt

import numpy as np







size = (10,10)
game = ToyWorld(*size)
agent = QAgentNumpy(game, (4,10,10), default = 0, epsilon = .1, alpha = .5, gamma = .99)
#agent = QAgent(game, default = -1, epsilon = .01, alpha = .1, gamma = .99)


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
    
