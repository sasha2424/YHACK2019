import random

class QAgent():

    def __init__(self, game, default = 10000, alpha=0.01, epsilon=0.1, gamma=0.99):
        self.game = game

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.default = default
        self.q_table = {}
        self.Q = lambda s, a: self.q_table[s][a]

    def argmax_q(self, s):
        return max(self.q_table[s].values())

    def argmax_q_action(self, s):
        actions = self.q_table[s].keys()
        return max(actions, lambda a : self.q_table[s][a])

    def fix_actions(self, s):
        actions = self.game.get_actions(s)
        for a in actions:
            if a in self.q_table[s].keys():
                continue
            self.q_table[s][a] = self.default

        for a in self.q_table[s].keys():
            if a in actions:
                continue
            self.q_table[s].del(a)

    def fix_states(self, s):
        if not s in self.q_table.keys():
            self.q_table[s] = {}

    def select_next_action(self, s):
        # Epsilon-greedy selection w.r.t. valid actions/skills
        self.fix_states(s)
        self.fix_actions(s)
        actions = self.game.get_actions(s)

        if random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            return self.argmax_q_action(s)

    def update(self, s, a, r, s_):
        actions = self.game.get_actions(s)
        argmax_q = self.argmax_q(s_)
        q_sa = self.Q(s, a)
        self.q_table[s][a] = (1-self.alpha) * q_sa + self.alpha * (r + self.gamma * argmax_q)
