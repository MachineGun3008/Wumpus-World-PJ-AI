import pygame
import numpy as np
import os
import sys
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

#Color
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
lemon = (239, 253, 95)
green = (0,255,0)
blue = (0,0,255)
red_ferrari = (255,40,0)

#Load map
def create_map(filename):
    if (not os.path.exists(filename)):
        return (0, None)
    file = open(filename, 'r')
    size = int(file.readline())
    map = []
    i = 1
    for i in range(size):
        data = file.readline().strip().split('.')
        map.append(data)

    player = 'A'
    x = 0
    y = 0
    gold = 0
    for i in range(len(map)):
        for j in range(len(map)):
            if map[i][j] == 'G':
                gold += 1
            if map[i][j] == player:
                x = i
                y = j
    file.close()
    return gold, x, y, size, map

map_list = ['Map\\map0.txt', 'Map\\map1.txt', 'Map\\map2.txt', 'Map\\map3.txt', 'Map\\map4.txt','Map\\map5.txt']
gold, x, y, size, map = create_map('Map\\map5.txt')
print(gold)
global WIDTH, HEIGHT
WIDTH = size * 75
HEIGHT = size * 75

#Create title and logo
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0 )
pygame.display.set_caption("Wumpus World")
logo = pygame.image.load('wumpus_logo.png')
pygame.display.set_icon(logo)

#Object
fog = pygame.image.load('rock.png')
floor = pygame.image.load('graybrick.png')
# mark = pygame.image.load('cobblestone.png')
wind = pygame.image.load('whirlwind.png')
gold = pygame.image.load('gold.png')
smell = pygame.image.load('stinksmell.png')
wumpus = pygame.image.load('wumpus.png')
hole = pygame.image.load('blackhole.png')

#Player
player_up = pygame.image.load('player_up.png')
player_down = pygame.image.load('player_down.png')
player_left = pygame.image.load('player_left.png')
player_right = pygame.image.load('player_right.png')

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def move_animation(command):
    # time.sleep(0.5)
    if command == 'END_GAME':
        print('game over')
        return False
    if command == 'LEFT' and maze[y // 20][(x - 20) // 20] != 1:
        x -= 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img180
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img180
    if command == 'RIGHT' and maze[y // 20][(x + 20) // 20] != 1:
        x += 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img0
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img0
    if command == 'UP' and maze[(y - 20) // 20][x // 20] != 1:
        y -= 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img90
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img90
    if command == 'DOWN' and maze[(y + 20) // 20][x // 20] != 1:
        y += 20
        if maze[y // 20][x // 20] == 2:
            score += 20
            maze[y // 20][x // 20] = 0
            player_img = player_img270
            food_list.remove((y // 20, x // 20))
            print((y // 20, x // 20))
        elif maze[y // 20][x // 20] == 3:
            print('game over')
            return False
        else:
            score -= 1
            player_img = player_img270

    return True

#Generate object
def generate_object(obj_img, x, y):
    screen.blit(obj_img, (x, y))

def game(x, y, map, gold):
    print(gold)
    gold_collect = 0
    player_x = x
    player_y = y
    model = player_down
    direction = 0
    path = np.zeros((size, size))


    running = True
    while running:
        pygame.time.delay(75)

        screen.fill(black)

        pos_x = 0
        pos_y = 0
        for col in range(size):
            for row in range(size):
                generate_object(floor, col * 75, row * 75)
                if path[col][row] != 1 and map[col][row].find('A') == -1:
                    generate_object(fog, col * 75, row * 75)
                else:
                    # if path[col][row] == 1:
                    #     generate_object(mark, col * 75, row * 75)
                    if map[col][row].find('G') != -1:
                        generate_object(gold, col * 75 + 20, row * 75 + 20)
                    if map[col][row].find('B') != -1:
                        generate_object(wind, col * 75 + 15, row * 75 + 10)
                    if map[col][row].find('S') != -1:
                        generate_object(smell, col * 75 + 40, row * 75 + 10)
                    if map[col][row].find('W') != -1:
                        generate_object(wumpus, col * 75 + 5, row * 75 + 5)
                    if map[col][row].find('P') != -1:
                        generate_object(hole, col * 75, row * 75)

                if map[col][row].find('A') != -1:
                    generate_object(model, player_x * 75 + 20, player_y * 75 + 20)

        # if map[player_x][player_y].find('W') != -1 or map[player_x][player_y].find('P') != -1:
        #     running = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if direction == 'left':
                        if map[player_x - 1][player_y].find('W') != -1:
                            wp_x = player_x - 1
                            wp_y = player_y

                            if wp_x == 0: #Wumpus at x axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y] #Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1] #Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1] #Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_x == size - 1: #Wumpus at x border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x][wp_y - 1] #Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y] #Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1] #Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == 0: #Wumpus at y axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y] #Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y] #Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1] #Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == size - 1: #Wumpus at y border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y] #Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1] #Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y] #Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                            else: #Wumpus not at axis or border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x - 1][wp_y] #Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x + 1][wp_y] #Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1] #Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1] #Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                    if direction == 'right':
                        if map[player_x + 1][player_y].find('W') != -1:
                            wp_x = player_x + 1
                            wp_y = player_y

                            if wp_x == 0:  # Wumpus at x axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_x == size - 1:  # Wumpus at x border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == 0:  # Wumpus at y axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == size - 1:  # Wumpus at y border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                            else:  # Wumpus not at axis or border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                    if direction == 'up':
                        if map[player_x][player_y - 1].find('W') != -1:
                            wp_x = player_x
                            wp_y = player_y - 1

                            if wp_x == 0:  # Wumpus at x axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_x == size - 1:  # Wumpus at x border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == 0:  # Wumpus at y axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == size - 1:  # Wumpus at y border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                            else:  # Wumpus not at axis or border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                    if direction == 'down':
                        if map[player_x][player_y + 1].find('W') != -1:
                            wp_x = player_x
                            wp_y = player_y + 1

                            if wp_x == 0:  # Wumpus at x axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_x == size - 1:  # Wumpus at x border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == 0:  # Wumpus at y axis
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')
                            elif wp_y == size - 1:  # Wumpus at y border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                            else:  # Wumpus not at axis or border
                                oldstr = map[wp_x][wp_y]
                                map[wp_x][wp_y] = oldstr.replace('W', '')
                                path[wp_x][wp_y] = 1

                                oldstr = map[wp_x - 1][wp_y]  # Left of wumpus
                                map[wp_x - 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x + 1][wp_y]  # Right of wumpus
                                map[wp_x + 1][wp_y] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y - 1]  # Backward of wumpus
                                map[wp_x][wp_y - 1] = oldstr.replace('S', '')
                                oldstr = map[wp_x][wp_y + 1]  # Forward of wumpus
                                map[wp_x][wp_y + 1] = oldstr.replace('S', '')

                if event.key == pygame.K_RETURN:
                    if map[player_x][player_y].find('G') != -1:
                        gold_collect += 1
                        print(gold_collect)
                        oldstr = map[player_x][player_y]
                        map[player_x][player_y] = oldstr.replace('G','')


                if event.key == pygame.K_LEFT:
                    if direction != 'left':
                        model = player_left
                        direction = 'left'
                    else:
                        if player_x - 1 >= 0:
                            player_x -= 1
                            map[player_x][player_y] += 'A'
                            oldstr = map[player_x + 1][player_y]
                            map[player_x + 1][player_y] = oldstr.replace('A', '')
                            path[player_x + 1][player_y] = 1

                if event.key == pygame.K_RIGHT:
                    if direction != 'right':
                        model = player_right
                        direction = 'right'
                    else:
                        if player_x + 1 < size:
                            player_x += 1
                            map[player_x][player_y] += 'A'
                            oldstr = map[player_x - 1][player_y]
                            map[player_x - 1][player_y] = oldstr.replace('A', '')
                            path[player_x - 1][player_y] = 1

                if event.key == pygame.K_UP:
                    if direction != 'up':
                        model = player_up
                        direction = 'up'
                    else:
                        if player_y - 1 >= 0:
                            player_y -= 1
                            map[player_x][player_y] += 'A'
                            oldstr = map[player_x][player_y + 1]
                            map[player_x][player_y + 1] = oldstr.replace('A', '')
                            path[player_x][player_y + 1] = 1

                if event.key == pygame.K_DOWN:
                    if direction != 'down':
                        model = player_down
                        direction = 'down'
                    else:
                        if player_y + 1 < size:
                            player_y += 1
                            map[player_x][player_y] += 'A'
                            oldstr = map[player_x][player_y - 1]
                            map[player_x][player_y - 1] = oldstr.replace('A', '')
                            path[player_x][player_y -1] = 1


        pygame.display.update()
        mainClock.tick(60)



if __name__ == '__main__':
    game(x, y, map, gold)
