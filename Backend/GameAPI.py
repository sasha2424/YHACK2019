from Game import ToyWorld
from QAgent import QAgentNumpy
import numpy as np

from threading import Thread


thread = None

size = (10,10)
bg_game = ToyWorld(*size)
bg_agent = QAgentNumpy(bg_game, (4,10,10), default = 0)
bg_state = bg_game.get_start_state()

fg_game = ToyWorld(*size)
fg_agent = QAgentNumpy(fg_game, (4,10,10), default = 0)
fg_state = fg_game.get_start_state()


def set_game_state(json):
    global fg_state, fg_game, fg_agent, bg_state, bg_game, bg_agent
    dict = eval(json.replace("null","None"))
    board = dict['board']
    agent = dict['agent']

    fg_game = ToyWorld(*size)
    for i,elem in enumerate(board):
        loc = (i // size[0],i % size[1])
        if elem == None:
            continue
        if elem == "bomb":
            fg_game.add_bomb(loc)
            continue
        if elem == "block":
            fg_game.add_block(loc)
            continue
        if elem == "wall":
            fg_game.add_wall(loc)
            continue
    bg_game.copy_state(fg_game)
    bg_state = tuple(agent)
    fg_state = tuple(agent)

    bg_game.save_initial_state()
    fg_game.save_initial_state()
    pass


def train_loop():
    while(True):
        for step in range(1000):
            action = bg_agent.select_next_action(bg_state)
            next_state = game.transition(bg_state,action)
            reward = game.reward(bg_state,action)
            bg_agent.update(bg_state,action,reward,bg_next_state)
            bg_state = bg_next_state

            if bg_game.is_end(bg_state):
                break
        bg_game.reset_to_initial()
        bg_state = bg.get_start_state()

def start_training():
    thread = Thread(target = train_loop)
    thread.start()

def end_training():
    thread.join()

def reset_training():
    global bg_state, bg_game, bg_agent
    bg_agent = QAgentNumpy(bg_game, (4,10,10), default = 0)
    bg_game.reset_to_initial()
    bg_agent = bg_game.get_start_state()
    pass


def reset_visual():
    global fg_state, fg_game, fg_agent
    fg_game.reset_to_initial()
    fg_state = fg_game.get_start_state()
    pass

def step_visual():
    global fg_state, fg_game, fg_agent
    action = fg_agent.select_next_action(fg_state)
    fg_state = fg_game.transition(fg_state,action)

    #construct return string
    board = [None for i in range(size[0] * size[1])]
    for block in fg_game.blocks:
        i = block[0] * size[1] + block[1]
        board[i] = 'block'
    for wall in fg_game.walls:
        i = wall[0] * size[1] + wall[1]
        board[i] = 'wall'
    for bomb in fg_game.bombs:
        i = bomb[0] * size[1] + bomb[1]
        board[i] = 'bomb'

    json = str({'board':board,'agent':list(fg_state)})
    return json

def update_Q():
    fg_agent.Q = bg_agent.Q.copy()


json = "{'board':[null,'block','bomb'],'agent':[0,0]}"
set_game_state(json)
print(step_visual())
