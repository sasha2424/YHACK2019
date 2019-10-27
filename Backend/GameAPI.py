from Game import ToyWorld
from QAgent import QAgentNumpy
import numpy as np

size = (10,10)
bg_game = ToyWorld(*size)
bg_agent = QAgentNumpy(bg_game, (4,10,10), default = 0)

fg_game = ToyWorld(*size)
fg_agent = QAgentNumpy(fg_game, (4,10,10), default = 0)



def set_game_state(json):
    list = eval(json.replace("null","None"))
    
    print(list)
    pass


def start_training():
    pass

def reset_training():
    bg_agent.Q
    pass


def reset_visual():
    pass

def step_visual():
    pass # return next state

def update_Q():
    fg_agent.Q = bg_agent.Q.copy()



set_game_state(json)
