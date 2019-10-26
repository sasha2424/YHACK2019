import random
import numpy as np

class QAgent():

    def __init__(self, game, default, alpha=0.5, epsilon=0.01, gamma=0.99):
        self.game = game

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.default = default
        self.q_table = {}


    def Q(self,s,a):
        if s in self.q_table.keys():
            if a in self.q_table[s].keys():
                return self.q_table[s][a]
            self.fix_actions(s)
            return self.q_table[s][a]
        self.fix_states(s)
        self.fix_actions(s)
        return self.q_table[s][a]

    def argmax_q(self, s):
        if not s in self.q_table.keys():
            self.fix_states(s)
            self.fix_actions(s)
        actions = self.q_table[s].keys()
        action = actions[0]
        value = self.q_table[s][action]
        for a in actions:
            if self.q_table[s][a] > value:
                value = self.q_table[s][a]
                action = a
        return value

    def argmax_q_action(self, s):
        if not s in self.q_table.keys():
            self.fix_states(s)
            self.fix_actions(s)
        actions = self.q_table[s].keys()
        action = actions[0]
        value = self.q_table[s][action]
        for a in actions:
            if self.q_table[s][a] > value:
                value = self.q_table[s][a]
                action = a
        return action

    def fix_actions(self, s):
        actions = self.game.get_actions(s)
        for a in actions:
            if a in self.q_table[s].keys():
                continue
            self.q_table[s][a] = self.default

        for a in self.q_table[s].keys():
            if a in actions:
                continue
            self.q_table[s].pop(a)

    def fix_states(self, s):
        if not s in self.q_table.keys():
            self.q_table[s] = {}

    def select_next_action(self, s):
        self.fix_states(s)
        self.fix_actions(s)
        actions = self.game.get_actions(s)

        if random.random() < self.epsilon:
            return random.choice(actions)
        else:
            return self.argmax_q_action(s)

    def update(self, s, a, r, s_):
        actions = self.game.get_actions(s)
        argmax_q = self.argmax_q(s_)
        #print(self.q_table)
        q_sa = self.Q(s, a)
        self.q_table[s][a] = (1-self.alpha) * q_sa + self.alpha * (r + self.gamma * argmax_q)
