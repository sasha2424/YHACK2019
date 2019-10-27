from flask import Flask, request, Response
from Game import ToyWorld
from QAgent import QAgentNumpy
import json
import numpy as np

from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'


thread = None

size = (10,10)
bg_game = ToyWorld(*size)
bg_agent = QAgentNumpy(bg_game, (4,10,10), default = 0)
bg_state = bg_game.get_start_state()

fg_game = ToyWorld(*size)
fg_agent = QAgentNumpy(fg_game, (4,10,10), default = 0)
fg_state = fg_game.get_start_state()


@app.route('/api/set-state', methods=['POST'])
def set_game_state():
    global fg_state, fg_game, fg_agent, bg_state, bg_game, bg_agent
    data = request.get_json(force=True)
    print(data)
    # data = eval(json.replace("null","None"))
    board = data['board']
    agent = data['agent']

    fg_game = ToyWorld(*size)
    bg_game = ToyWorld(*size)
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
    return "success"


def train_loop():
    global bg_state, bg_agent, bg_game
    while(True):
        for step in range(1000):
            # print(step)
            action = bg_agent.select_next_action(bg_state)
            bg_next_state = bg_game.transition(bg_state,action)
            reward = bg_game.reward(bg_next_state,action)
            print(reward)
            bg_agent.update(bg_state,action,reward,bg_next_state)
            bg_state = bg_next_state

            if bg_game.is_end(bg_state):
                break
        bg_game.reset_to_initial()
        bg_state = bg_game.get_start_state()

@app.route('/api/start', methods=['POST'])
def start_training():
    thread = Thread(target = train_loop)
    thread.start()
    return "success"

@app.route('/api/end', methods=['POST'])
def end_training():
    thread.join()
    return "success"

def reset_training():
    global bg_state, bg_game, bg_agent
    bg_agent = QAgentNumpy(bg_game, (4,10,10), default = 0)
    bg_game.reset_to_initial()
    bg_agent = bg_game.get_start_state()
    pass


@app.route('/api/reset-visual', methods=['POST'])
def reset_visual():
    global fg_state, fg_game, fg_agent
    fg_game.reset_to_initial()
    fg_state = fg_game.get_start_state()
    return "success"

@app.route('/api/step-visual', methods=['POST'])
def step_visual():
    update_Q()
    global fg_state, fg_game, fg_agent
    action = fg_agent.select_next_action(fg_state)
    fg_state = fg_game.transition(fg_state,action)
    if fg_game.is_end(fg_state):
        fg_game.reset_to_initial()
        

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
    q_table = np.max(bg_agent.Q,axis=0)
    q_table -= np.min(q_table)
    q_table = q_table / (np.max(q_table) + .001)
    q_table = q_table.flatten().tolist()
    data = json.dumps({'board':board,'agent':list(fg_state),'qtable':q_table})
    # print(data)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

def update_Q():
    fg_agent.Q = bg_agent.Q.copy()


# json = "{'board':[null,'block','bomb'],'agent':[0,0]}"
# set_game_state(json)
# print(step_visual())
