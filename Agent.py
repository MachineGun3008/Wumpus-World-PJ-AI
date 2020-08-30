import queue
class Agent:
    def __init__(self, position):
        self.maze = [['' for _ in range(10)] for _ in range(10)]
        
        # safe: Is it safe
        # PIT: Is it a PIT
        # wumpus: Is it a wumpus
        # -1: don't know
        # 0: False
        # 1: True
        #self.safe = [[-1 for _ in range(10)] for _ in range(10)]
        #self.PIT = [[-1 for _ in range(10)] for _ in range(10)]
        self.wumpus = [[-1 for _ in range(10)] for _ in range(10)]
        self.start_pos = position
        self.pos = position
        self.score = 0
        self.maze[position[0]][position[1]] = '-'
        
        # Current direction
        self.face = 'RIGHT'
        self.command = ['']
        
        # Constant variable
        self.empty_room = '-'
        self.breeze = 'B'
        self.stench = 'S'
        self.gold = 'G'
        self.real_wumpus = 'W'
        self.real_pit = 'P'
        self.point_for_dying = -10000
        self.point_for_picking_up_gold = 100
        self.point_for_shooting_arrow = -100
        self.point_for_moving = -10
        self.point_for_climbing_out = 10
        self.direction = [[-1, 0, 'UP'], [0, -1, 'LEFT'], [0, 1, 'RIGHT'], [1, 0, 'DOWN']]
        self.height = 10
        self.width = 10
    
    def ListOfAdjacentRoom(self, position):
        AdjacentRoom = []
        for i in range(4):
            x, y = position[0] + self.direction[i][0], position[1] + self.direction[i][1]
            if 0 <= x < 10 and 0 <= y < 10:
                AdjacentRoom.append((x, y))
        
        return AdjacentRoom

    
    def PrintKB(self):
        KB = []
        for i in range(self.height):
            for j in range(self.width):
                literals = []
                if self.empty_room in self.maze[i][j]:
                    literals.append('Empty room ({0}, {1})'.format(i, j))
                if self.breeze in self.maze[i][j]:
                    literals.append('Breeze room ({0}, {1})'.format(i, j))
                if self.stench in self.maze[i][j]:
                    literals.append('Stench room ({0}, {1})'.format(i, j))
                if self.wumpus[i][j] == 0:
                    literals.append('Not Wumpus({0}, {1})'.format(i, j))
                clause = ''
                for u in range(len(literals), -1, -1):
                    clause += literals[u]
                    if u:
                        clause += ' Or '
                KB.append(clause)
        
        print('For every x, y: Not Exist(x, y) Or Wumpus(x, y) Or PIT(x, y) Or Safe(x, y)')
        print('For every x, y: Not (0 <= x < 10) Or Not (0 <= y < 10) Or Exist(x, y)')
        print('For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x - 1, y) Or Unknown Room(x - 1, y) Or Stench Room(x - 1, y)')
        print('For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x + 1, y) Or Unknown Room(x + 1, y) Or Stench Room(x + 1, y)')
        print('For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y - 1) Or Unknown Room(x, y - 1) Or Stench Room(x, y - 1)')
        print('For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y + 1) Or Unknown Room(x, y + 1) Or Stench Room(x, y + 1)')
        print('For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x - 1, y) Or Unknown Room(x - 1, y) Or Breeze Room(x - 1, y)')
        print('For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x + 1, y) Or Unknown Room(x + 1, y) Or Breeze Room(x + 1, y)')
        print('For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y - 1) Or Unknown Room(x, y - 1) Or Breeze Room(x, y - 1)')
        print('For every x,y : Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y + 1) Or Unknown Room(x, y + 1) Or Breeze Room(x, y +  1)')
       
        for i in range(len(KB)):
            print(KB[i], end = '')
            print()
    
    # When Agent reach new room, it has to expand its KB
    def SetMaze(self, map):
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] != '':
                    room = map[i][j]
                    if 'A' in room:
                        outstr = room
                        room = outstr.replace('A', '')
                    self.maze[i][j] = room

    def SetNewRoom(self, position):
        self.maze[position[0]][position[1]] = '-'
    
    def CheckExist(self, position):
        return 0 <= position[0] < self.height and 0 <= position[1] < self.width
    
    def CheckUnknown(self, position):
        if not self.CheckExist(position):
            return True
        if self.maze[position[0]][position[1]] == '':
            return True
        return False

    def CheckStenchRoom(self, position):
        if self.stench in self.maze[position[0]][position[1]]:
            return True
        return False
    
    def CheckBreezeRoom(self, position):
        if self.breeze in self.maze[position[0]][position[1]]:
            return True
        return False

    def CheckStenchRoom(self, position):
        if not self.CheckExist(position):
            return False
        if self.stench in self.maze[position[0]][position[1]]:
            return True
        return False

    def CheckPIT(self, position):
        # Use 4 first logic order in KB and resolution
        # For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x - 1, y) Or Unknown Room(x - 1, y) Or Breeze Room(x - 1, y) From KB
        # For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x + 1, y) Or Unknown Room(x + 1, y) Or Breeze Room(x + 1, y) From KB
        # For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y - 1) Or Unknown Room(x, y - 1) Or Breeze Room(x, y - 1) From KB
        # For every x,y : Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y + 1) Or Unknown Room(x, y + 1) Or Breeze Room(x, y +  1) From KB
        # Not PIT(postion) Negation

        if self.CheckUnknown(position) == False:
            return False
        for i in range(4):
            new_position = (position[0] + self.direction[i][0], position[1] + self.direction[i][1])
            if self.CheckExist(new_position) and not (self.CheckUnknown(new_position) or self.CheckBreezeRoom(new_position)):
                return False
        return True

    def CheckWumpus(self, position):
        # Check in KB, has Agent already known that room doesn't have wumpus
        if not self.wumpus[position[0]][position[1]]:
            return False

        # Use 4 first logic order in KB and resolution
        # For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x - 1, y) Or Unknown Room(x - 1, y) Or Stench Room(x - 1, y) From KN
        # For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x + 1, y) Or Unknown Room(x + 1, y) Or Stench Room(x + 1, y) From KB
        # For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y - 1) Or Unknown Room(x, y - 1) Or Stench Room(x, y - 1) From KB
        # For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y + 1) Or Unknown Room(x, y + 1) Or Stench Room(x, y + 1) From KB
        # Not Wumpus(position) Negation
        if self.CheckUnknown(position) == False:
            return False
        for i in range(4):
            new_position = (position[0] + self.direction[i][0], position[1] + self.direction[i][1])
            count = 0
            if self.CheckExist(new_position) and not(self.CheckUnknown(new_position) or self.CheckStenchRoom(new_position)):
                return False
        return True
    
    def CheckSafe(self, position):
        # Use resolution
        # For every x, y: Not Exist(x, y) Or Wumpus(x, y) Or PIT(x, y) Or Safe(x, y) From KB
        # Not Safe(position)
        if not self.CheckExist(position) or self.CheckWumpus(position) or self.CheckPIT(position):
            return False
        return True
    
    def FindPathWithGoal(self, goal):
        #bfs
        parent = [[(-1, -1) for _ in range(self.width)] for _ in range(self.height)]
        q = queue.Queue()
        q.put(self.pos)
        parent[self.pos[0]][self.pos[1]] = 0
        while not q.empty() and parent[goal[0]][goal[1]] == (-1, -1):
            position = q.get()
            for i in range(4):
                new_position = (position[0] + self.direction[i][0], position[1] + self.direction[i][1])
                if self.CheckSafe(new_position) and parent[new_position[0]][new_position[1]] == (-1, -1):
                    parent[new_position[0]][new_position[1]] = position
                    q.put(new_position)
        
        # Put path into command
        position = goal
        while position != self.pos:
            if self.gold in self.maze[position[0]][position[1]]:
                self.command.append('TAKE GOLD')
                oldstr = self.maze[position[0]][position[1]]
                self.maze[position[0]][position[1]] = oldstr.replace('G', '-')
            #if self.CheckWumpus(position):
            #    self.command.append('SHOT')
            self.command.append('GO')
            for i in range(4):
                if position[0] - parent[position[0]][position[1]][0] == self.direction[i][0] and position[1] - parent[position[0]][position[1]][1] == self.direction[i][1]:
                    self.command.append(self.direction[i][2])
                    position = parent[position[0]][position[1]]
                    break
                    
    def FindPath(self):
        q = queue.Queue()
        q.put(self.pos)
        visited = set()
        visited.add(self.pos)
        count = [1, 0]
        level = 0
        goal = self.pos
        deep = 10000
        while not q.empty():
            posititon = q.get()
            count[0] -= 1
            for i in range(4):
                new_position = (posititon[0] + self.direction[i][0], posititon[1] + self.direction[i][1])
                if self.CheckSafe(new_position) and new_position not in visited:
                    visited.add(new_position)
                    q.put(new_position)
                    count[1] += 1
                    if self.gold in self.maze[new_position[0]][new_position[1]]:
                        goal = new_position
                        deep = -1
                    if self.maze[new_position[0]][new_position[1]] == '' and level + 1 < deep:
                        goal = new_position
                        deep = level
            if count[0] == 0:
                count[0] = count[1]
                count[1] = 0
                level += 1
                if goal != self.pos:
                    return goal
        return goal
    def CalProbility(self, position, model):
        if model == 0:
            count = 0
            for i in range(4):
                count += self.CheckWumpus((position[0] + self.direction[i][0], position[1] + self.direction[i][1]))
            return count
        else:
            count = 4
            for i in range(4):
                if self.CheckExist((position[0] + self.direction[i][0], position[1] + self.direction[i][1])) and self.maze[position[0] + self.direction[i][0]][position[1] + self.direction[i][1]] != '':
                    count = min(count, self.CalProbility((position[0] + self.direction[i][0], position[1] + self.direction[i][1]), 0))
            return count
    def FindWumpus(self):
        q = queue.Queue()
        q.put(self.pos)
        visited = set()
        visited.add(self.pos)
        count = [1, 0]
        level = 0
        goal, wumpus_pos = self.pos, (-1, -1)
        price = -10**18
        while not q.empty():
            position = q.get()
            count[0] -= 1
            for i in range(4):
                new_position = (position[0] + self.direction[i][0], position[1] + self.direction[i][1])
                if self.CheckExist(new_position) and new_position not in visited:
                    visited.add(new_position)
                    if self.maze[new_position[0]][new_position[1]] != '':
                        q.put(new_position)
                    count[1] += 1
                    if new_position == (1, 3):
                        print('test')
                    if self.maze[new_position[0]][new_position[1]] == '' and self.CheckWumpus(new_position):
                        new_price = (level + 1) * self.point_for_moving + self.point_for_shooting_arrow * self.CalProbility(new_position, 1)
                        if price < new_price:
                            price = new_price 
                            goal, wumpus_pos = position, new_position
            if count[0] == 0:
                count[0] = count[1]
                count[1] = 0
                level += 1
                if wumpus_pos != (-1, -1):
                    return goal, wumpus_pos
        return goal, wumpus_pos

    def GetActions(self):
        self.command.pop()

        # If still have command, just do it
        if len(self.command):
            return self.command[-1]
        if self.gold in self.maze[self.pos[0]][self.pos[1]]:
            self.command.append('TAKE GOLD')
            return self.command[-1]
        # Find the safest path
        if self.pos == (5, 0):
            print('test')
        goal = self.FindPath()
        if goal != self.pos:
            self.FindPathWithGoal(goal)
            self.pos = goal
            return self.command[-1]
        
        # If don't have safest path, we have to hunt wumpus to create new path
        goal, wumpus_pos = self.FindWumpus()
        if wumpus_pos != (-1, -1):
            for i in range(4):
                if wumpus_pos[0] - goal[0] == self.direction[i][0] and wumpus_pos[1] - goal[1] == self.direction[i][1]:
                    self.command.append('SHOT')
                    self.command.append(self.direction[i][2])
            self.wumpus[wumpus_pos[0]][wumpus_pos[1]] = 0
            self.FindPathWithGoal(goal)
            self.pos = goal
            return self.command[-1]
        
        # If don't have another choice, return and climb up
        self.command.append('CLIMB UP')
        self.FindPathWithGoal(self.start_pos)
        self.pos = goal
        return self.command[-1]