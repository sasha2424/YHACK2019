from Game import Game,GridWorld
from QAgent import QAgent
import matplotlib.pyplot as plt







size = (10,10)
game = GridWorld(*size)
agent = QAgent(game)

def get_q_values():
    board = np.zeros(size)
    for row in size[0]:
        for col in size[1]:
            board[row][col] = agent.argmax_q((row,col))
    return board

state = game.get_start_state()

for episode in range(100):
    for step in range(1000):
        action = agent.select_next_action(state)
        next_state = game.transition(state,action)
        reward = game.reward(state,action)
        agent.update(state,action,reward,next_state)
        state = next_state

        plt.imshow(get_q_values())
        plt.draw()
        plt.pause(.01)
        plt.cla()
