import random
import numpy as np

class QAgent():
    def __init__(self, game, default, alpha=0.5, epsilon=0.1, gamma=0.99):
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
        action = list(actions)[0]
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
        action = list(actions)[0]
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


class QAgentLambda():

    def __init__(self, game, default, alpha=0.5, epsilon=0.1, gamma=0.99):
        self.game = game

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.default = default
        self.q_table = {}
        self.e_table = {}


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
        delta = r + self.gamma * argmax_q - self.Q(s,a)

        for (state,action) in self.e_table.keys():
            self.q_table[state][action] += self.alpha * delta * self.e_table[(state,action)]
            self.e_table[(state,action)] = self.gamma * self.e_table[(state,action)]
        self.e_table[(s,a)] = 1


class QAgentNumpy():
    def __init__(self, game, shape, default, alpha=0.5, epsilon=0.1, gamma=0.5, lam = 0.5):
        self.game = game

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.lam = lam
        self.shape = shape

        self.default = default
        self.Q = np.zeros(self.shape)
        self.Q.fill(default)

        self.E = np.zeros(self.shape)
        self.E.fill(0)

    def reset_E(self):
        self.E = np.zeros(self.shape)


    def Q_val(self,s,a):
        I = (a,) + tuple(s)
        return self.Q[I]

    def fix_dims(self,shape):
        if len(shape) > len(self.shape):
            self.Q = np.expand_dims(self.Q,axis=len(self.shape))
            self.shape = self.Q.shape
            self.fix_dims(shape)
        if len(shape) < len(self.shape):
            self.Q = np.max(self.Q,axis=len(self.shape))
            self.shape = self.Q.shape
            self.fix_dims(shape)

    def fix_shape(self,shape):
        if len(shape) != len(self.shape):
            self.fix_dims(shape)
        delta = shape - self.shape
        zeros = np.zeros(len(delta)).astype(int)
        padding = zip(zeros,np.maximum(delta,0))
        self.Q = np.pad(self.Q, padding, mode='constant', constant_values=self.default)
        for dim in range(len(shape)):
            self.Q = self.Q.take(indices=range(shape[dim]), axis=dim)
        self.shape = shape

    def argmax_q(self, s):
        value = self.Q_val(s,0)
        for a in range(self.shape[0]):
            value = max(value,self.Q_val(s,a))
        return value

    def argmax_q_action(self, s):
        value = self.Q_val(s,0)
        action = 0
        for a in range(self.shape[0]):
            v = self.Q_val(s,a)
            if v > value:
                value = v
                action = a
        return action

    def select_next_action(self, s):
        actions = self.game.get_actions(s)

        if random.random() < self.epsilon:
            return random.choice(actions)
        else:
            return self.argmax_q_action(s)

    def update(self, s, a, r, s_):
        Q_ = self.argmax_q(s_)
        I = (a,) + tuple(s)

        self.E[I] = 1
        delta =  -self.Q_val(s,a) + r + self.gamma * Q_
        self.Q = self.Q + self.alpha * delta * self.E
        self.E = self.E * self.lam * self.gamma
