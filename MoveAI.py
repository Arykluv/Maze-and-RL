import numpy as np 
from collections import deque 

#constant 
Agent = 1 
Passenger = 4 
Goal = 8 
Barrier = -1 

#class & shits 

class Map: 
    def __init__(self, length, height, barriers, agent, passenger, goal):
        self.length = length
        self.height = height 
        self.map = np.zeros((self.length, self.height))
        self.barriers =barriers
        self.agent = agent
        self.passenger = passenger
        self.goal = goal

    def get_agent(self): 
        return tuple(self.agent)
    def get_passenger(self): 
        return tuple(self.passenger)
    def get_goal(self): 
        return tuple(self.goal)


    def fill_map(self):
        if len(self.barriers) != 0: 
            for barrier in self.barriers: 
                self.map[tuple(barrier)] = Barrier
        self.map[self.get_agent()] = Agent    
        self.map[self.get_passenger()] = Passenger
        self.map[self.get_goal()] = Goal 
        print(self.map)

    def search(self, start, end):
        queue = deque([[start]])
        seen = set([start])
        while queue: 
            path = queue.popleft()
            x , y = path[-1]
            if (x,y) == end: 
                return path 
            
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < self.length and 0 <= y2 < self.height and self.map[x2][y2] != Barrier and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2,y2))
    def convert(self, path, action):
        out = []
        for i in range(1, len(path)):
            current = path[i-1]
            next_pos = path[i]
            dx = next_pos[0] - current[0]
            dy = next_pos[1] - current[1]
            if dx == 1: out.append("Down")
            elif dx == -1: out.append("Up")
            elif dy == 1: out.append("Right")
            elif dy == -1: out.append("Left")
        out.append(action)
        return out
    def find_passenger(self):
        path = self.search(self.get_agent(), self.get_passenger())
        if path is None:
            return None
        return self.convert(path, "Pick up")
    def find_goal(self):
        path = self.search(self.get_passenger(), self.get_goal())
        return self.convert(path, "Put down")
        self.agent = self.passenger
    
    def run(self):
        self.fill_map()
        pick_passenger = self.find_passenger()
        leave_at_goal = self.find_goal()
        return(pick_passenger, leave_at_goal)
    
# Agent = 1 
# Passenger = 4 
# Goal = 8 
# Barrier = -1 
if __name__ == "__main__":
    env = Map(4,4, [], [0,0], [1,1], [3,3]) #(Map Length(),Map Height(),barriers Coordination[(),...,()],Location agent[],Location passenger[],coordination goal[])
    print(env.run())