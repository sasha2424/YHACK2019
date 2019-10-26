

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

    def is_goal(self,s):
        pass

    def show(selfaxis):
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
        if self.is_goal(s):
            return 100
        return -1

    def is_goal(self,s):
        if s[0] == self.rows-1:
            if s[1] == self.cols-1:
                return True
        return False

    def show(self,axis):
        pass
