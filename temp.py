import pygame
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
    for i in range(len(map)):
        for j in range(len(map)):
            if map[i][j] == player:
                x = i
                y = j
    file.close()
    return (x, y, size, map)

x, y, size, map = create_map('input.txt')
global WIDTH, HEIGHT
WIDTH = size * 75
HEIGHT = size * 75

#Create title and logo
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0 )
pygame.display.set_caption("Wumpus World")
logo = pygame.image.load('wumpus.png')
pygame.display.set_icon(logo)

#Object
dirt = pygame.image.load('laval_blue.png')
backgrounds = pygame.image.load('lava_black_d.png')


#Player
player_up = pygame.image.load('up.png')
player_down = pygame.image.load('down.png')
player_left = pygame.image.load('left.png')
player_right = pygame.image.load('right.png')

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

def game(x, y, map):
    player_x = x
    player_y = y
    model = player_right
    running = True
    while running:
        pygame.time.delay(75)

        screen.fill(black)
        screen.blit(backgrounds, (0,0))

        for col in range(size):
            for row in range(size):
                if map[col][row] == map[player_x][player_y]:
                    print(col, row)
                    generate_object(model, player_x * 75 + 20, player_y * 75 + 20)
                else:
                    generate_object(dirt, col * 75, row * 75)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_x - 1 >= 0:
                    model = player_left
                    player_x -= 1
                    map[player_x][player_y] = 'A'
                    map[player_x + 1][player_y] = '-'
                    print(player_x, player_y)

                if event.key == pygame.K_RIGHT and player_x + 1 < size:
                    model = player_right
                    player_x += 1
                    map[player_x][player_y] = 'A'
                    map[player_x - 1][player_y] = '-'
                    print(player_x, player_y)

                if event.key == pygame.K_UP and player_y - 1 >= 0:
                    model = player_up
                    player_y -= 1
                    map[player_x][player_y] = 'A'
                    map[player_x][player_y + 1] = '-'
                    print(player_x, player_y)

                if event.key == pygame.K_DOWN and player_y + 1 < size:
                    model = player_down
                    player_y += 1
                    map[player_x][player_y] = 'A'
                    map[player_x][player_y - 1] = '-'
                    print(player_x, player_y)

        pygame.display.update()
        mainClock.tick(60)



if __name__ == '__main__':
    game(x, y, map)
