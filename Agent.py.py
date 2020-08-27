class Agent:
    def __init__(self, position):
        self.maze = [['' for _ in range(10)] for _ in range(10)]
        
        # safe: Is it safe
        # PIT: Is it a PIT
        # wumpus: Is it a wumpus
        # -1: don't know
        # 0: False
        # 1: True
        self.safe = [[-1 for _ in range(10)] for _ in range(10)]
        self.PIT = [[-1 for _ in range(10)] for _ in range(10)]
        self.wumpus = [[-1 for _ in range(10)] for _ in range(10)]
        self.pos = position
        self.score = 0
        
        # Current direction
        self.face = 'RIGHT'
        
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
        self.direction = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1'LEFT'), (0, 1, 'RIGHT')]
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
        
        print('For every x, y: Not Wumpus(x, y) Or Not PIT(x, y) Or Safe(x, y)')
        print('For every x, y: Not (0 <= x < 10) Or Not (0 <= y < 10) Or Exist(x, y)')
        print('For every x, y: Not Wumpus(x, y) Or Not Unknown(x, y) Or Or Not Exist Room(x - 1, y) Or Unknown Room(x - 1, y) Or Stench Room(x - 1, y)')
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
    def SetNewPosition(self, room, position):
        self.maze[self.pos[0]][self.pos[1]] = room
    
    def CheckExist(self, position):
        return 0 <= position[0] < self.height and 0 <= position[1] < self.width
    
    def CheckUnknown(self, position):
        if self.maze[position[0]][position[1]] = '':
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
        if self.SetNewPosition in self.maze[position[0]][position[1]]:
            return True
        return False

    def CheckPIT(self, position):
        # Use 4 first logic order in KB and resolution
        # For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or  Not Exist Room(x - 1, y) Or Unknown Room(x - 1, y) Or Breeze Room(x - 1, y) From KB
        # For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x + 1, y) Or Unknown Room(x + 1, y) Or Breeze Room(x + 1, y) From KB
        # For every x, y: Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y - 1) Or Unknown Room(x, y - 1) Or Breeze Room(x, y - 1) From KB
        # For every x,y : Not PIT(x, y) Or Not Unknown(x, y) Or Not Exist Room(x, y + 1) Or Unknown Room(x, y + 1) Or Breeze Room(x, y +  1) From KB
        # Not PIT(x, y) Negation

        for i in range(4):
            new_position = (position[0] + self.direction[i][0], position[1] + self.direction[i][1])
            if not(not self.CheckUnknown(position) or not self.CheckExist(new_position) or self.CheckUnknown(new_position) or self.CheckBreezeRoom(new_position)):
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
        # Not Wumpus(x, y) Negation
        for i in range(4):
            new_position = (position[0] + self.direction[i][0], position[1] + self.direction[i][1])
            if not(not self.CheckUnknown(position) or not self.CheckExist(new_position) or self.CheckUnknown(new_position) or self.CheckStenchRoom(new_position)):
                return False
        return True
    
    def CheckSafe(self, position):
        # Use For every x, y: Not Wumpus(x, y) Or Not PIT(x, y) Or Safe(x, y) From KB
        if not self.CheckWumpus(position) or not self.CheckPIT(position):
            return True
        return False