import numpy as np

class Game:

    def __init__(self):
        pass

    def get_start_state(self):
        pass

    def get_actions(self,s):
        pass

    def transition(self,s,a):
        pass

    def reward(self,s,a,s_):
        pass

    def is_end(self,s):
        pass

    def show(self,plt):
        pass


class GridWorld(Game):

    def __init__(self, row, col):
        self.rows = row
        self.cols = col

    def get_start_state(self):
        return (0,0)

    def get_actions(self,s):
        return [0,1,2,3]

    def transition(self,s,a):
        if s[0] == self.rows-1:
            if s[1] == self.cols-1:
                return (0,0)
        if(a == 0): #DOWN
            if not s[0] == self.rows-1:
                return (s[0] + 1, s[1])
        if(a == 1): #RIGHT
            if not s[1] == self.cols-1:
                return (s[0], s[1] + 1)
        if(a == 2): #UP
            if not s[0] == 0:
                return (s[0] - 1, s[1])
        if(a == 3):
            if not s[1] == 0:
                return (s[0], s[1] - 1)
        return s

    def reward(self,s,a):
        if self.is_end(s):
            return 100
        return -1

    def is_end(self,s):
        if s[0] == self.rows-1:
            if s[1] == self.cols-1:
                return True
        return False

    def show(self, agent, plt, size, state,episode):

        board = np.zeros(size)
        for row in range(size[0]):
            for col in range(size[1]):
                SUM = 0
                for a in [1,2,3,4]:
                    SUM += agent.Q((row,col),a)
                board[row][col] = SUM / 4

        plt.imshow(get_q_values())
        plt.scatter(state[1],state[0],s=30,c='r')
        plt.title("Episode " + str(episode))
        plt.draw()
        plt.pause(.01)
        plt.cla()


class ToyWorld(Game):
        def __init__(self, row, col):
            self.rows = row
            self.cols = col
            #self.blocks = []
            self.bombs = []
            self.teleports = []
            self.walls = []

        def get_start_state(self):
            return (0,0)

        def get_actions(self,s):
            return [0,1,2,3]

        def transition(self,s,a):
            if self.is_end(s):
                return (0,0)

            for teleport in self.teleports:
                if s[0] == teleport[0] and s[1] == teleport[1]:
                    s = (teleport[2],teleport[3])

            if(a == 0): #DOWN
                if not s[0] == self.rows-1:
                    if not self.is_wall((s[0] + 1, s[1])):
                        s = (s[0] + 1, s[1])
            if(a == 1): #RIGHT
                if not s[1] == self.cols-1:
                    if not self.is_wall((s[0], s[1] + 1)):
                        s = (s[0], s[1] + 1)
            if(a == 2): #UP
                if not s[0] == 0:
                    if not self.is_wall((s[0] - 1, s[1])):
                        s =  (s[0] - 1, s[1])
            if(a == 3):
                if not s[1] == 0:
                    if not self.is_wall((s[0], s[1] - 1)):
                        s =  (s[0], s[1] - 1)

            return s

        def is_wall(self,s):
            for wall in self.walls:
                if s[0] == wall[0] and s[1] == wall[1]:
                    return True
            return False

        def reward(self,s,a):
            if self.is_goal(s):
                return 1000
            for bomb in self.bombs:
                if s[0] == bomb[0] and s[1] == bomb[1]:
                    return -10
            return -1

        def is_goal(self,s):
            if s[0] == self.rows-1:
                if s[1] == self.cols-1:
                    return True
            return False

        def is_end(self,s):
            if s[0] == self.rows-1:
                if s[1] == self.cols-1:
                    return True

            for bomb in self.bombs:
                if s[0] == bomb[0] and s[1] == bomb[1]:
                    return True
            return False

        def add_wall(self,s):
            self.walls.append(s)

        def remove_wall(self,s):
            try:
                self.walls.remove(s)
            except:
                pass

        def add_bomb(self,s):
            self.bombs.append(s)

        def remove_wall(self,s):
            try:
                self.bombs.remove(s)
            except:
                pass

        def add_teleport(self,s,s_):
            self.teleports.append((s[0],s[1],s_[0],s_[1]))

        def remove_teleport(self,s,s_):
            try:
                self.teleports.remove((s[0],s[1],s_[0],s_[1]))
            except:
                pass
