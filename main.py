import pygame
import numpy as np
import os
import sys
import time
from pygame.locals import *
from Agent import Agent

pygame.init()
mainClock = pygame.time.Clock()

#Font
font1 = pygame.font.Font('Spooky Cat Font.otf', 140)
font2 = pygame.font.Font('Spooky Cat Font.otf', 100)
font3 = pygame.font.Font('Spooky Cat Font.otf', 150)
font4 = pygame.font.Font('Spooky Cat Font.otf', 90)
font5 = pygame.font.Font('Spooky Cat Font.otf', 80)
font6 = pygame.font.Font('Spooky Cat Font.otf', 190)

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
            if player in map[i][j]:
                y = i
                x = j
                map[i][j] += '-'
    file.close()
    return gold, x, y, size, map

map_list = ['Map\\map0.txt', 'Map\\map1.txt', 'Map\\map2.txt', 'Map\\map3.txt', 'Map\\map4.txt', 'Map\\map5.txt']
gold, x, y, size, map = create_map(map_list[np.random.randint(0,5)])

global WIDTH, HEIGHT
WIDTH = size * 75 + 550
HEIGHT = size * 75


#Create title and logo
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
pygame.display.set_caption("Wumpus World")
logo = pygame.image.load('wumpus_logo.png')
pygame.display.set_icon(logo)
pygame.display.flip()

#Object
fog = pygame.image.load('rock.png')
floor = pygame.image.load('graybrick.png')
wind = pygame.image.load('whirlwind.png')
gold = pygame.image.load('gold.png')
smell = pygame.image.load('stinksmell.png')
wumpus = pygame.image.load('wumpus.png')
hole = pygame.image.load('blackhole.png')
wumpus_big = pygame.image.load('wumpus_bigsize.png')
background = pygame.image.load('cave.png')
entrance1 = pygame.image.load('entrance.png')

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



#Generate object
def generate_object(obj_img, x, y):
    screen.blit(obj_img, (x, y))

def game(x, y, map, gold):
    gold_collect = 0
    wumpus_kill = 0
    score = 0
    player_x = x # Column
    player_y = y # Row
    model = player_right
    direction = 'RIGHT'
    path = np.zeros((size, size))
    knight = Agent((y, x))
    knight.SetMaze(map)

    running = True
    while running:
        pygame.time.delay(50)

        screen.fill(black)
        screen.blit(background, (0,0))
        draw_text("Hunt", font1, lemon, screen, size * 75 + 70, size - 10)
        draw_text("the", font2, lemon, screen, size * 75 + 100, size + 100)
        draw_text("WUMPUS", font3, red_ferrari, screen, size * 75 + 20, size + 170)
        draw_text("Score:", font4, lemon, screen, size * 75 + 70, size + 400)
        draw_text(str(score), font5, black, screen, size * 75 + 290, size + 410)
        generate_object(wumpus_big, size * 75 + 320, size)
        
        for col in range(size):
            for row in range(size):
                generate_object(floor, col * 75, row * 75)
                generate_object(entrance1, x * 75, y * 75)

                if path[row][col] != 1 and map[row][col].find('A') == -1:
                    generate_object(fog, col * 75, row * 75)
                else:
                    if map[row][col].find('G') != -1:
                        generate_object(gold, col * 75 + 20, row * 75 + 20)
                    if map[row][col].find('B') != -1:
                        generate_object(wind, col * 75 + 15, row * 75 + 10)
                    if map[row][col].find('S') != -1:
                        generate_object(smell, col * 75 + 40, row * 75 + 10)
                    if map[row][col].find('W') != -1:
                        generate_object(wumpus, col * 75 + 5, row * 75 + 5)
                    if map[row][col].find('P') != -1:
                        generate_object(hole, col * 75, row * 75)

                if map[row][col].find('A') != -1:
                    generate_object(model, player_x * 75 + 20, player_y * 75 + 20)

        if map[player_y][player_x].find('W') != -1 or map[player_y][player_x].find('P') != -1:
            score -= 10000
            game_over(wumpus_kill, gold_collect, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        command = knight.GetActions()            

        if command == 'LEFT' or command == 'RIGHT' or command == 'DOWN' or command == 'UP':
            if direction == command:
                command = knight.GetActions()
            else:
                direction = command
                if command == 'LEFT':
                    model = player_left
                elif command == 'RIGHT':
                    model = player_right
                elif command == 'UP':
                    model = player_up
                elif command == 'DOWN':
                    model = player_down
        if command == 'GO':
            score -= 10
            if direction == 'LEFT':
                if player_x - 1 >= 0:
                    player_x -= 1
                    map[player_y][player_x] += 'A'
                    oldstr = map[player_y][player_x + 1]
                    map[player_y][player_x + 1] = oldstr.replace('A', '')
                    path[player_y][player_x + 1] = 1
            elif direction == 'RIGHT':
                if player_x + 1 < size:
                    player_x += 1
                    map[player_y][player_x] += 'A'
                    oldstr = map[player_y][player_x - 1]
                    map[player_y][player_x - 1] = oldstr.replace('A', '')
                    path[player_y][player_x - 1] = 1
            elif direction == 'DOWN':
                if player_y + 1 < size:
                    player_y += 1
                    map[player_y][player_x] += 'A'
                    oldstr = map[player_y - 1][player_x]
                    map[player_y - 1][player_x] = oldstr.replace('A', '')
                    path[player_y - 1][player_x] = 1
            elif direction == 'UP':
                if player_y - 1 >= 0:
                    player_y -= 1
                    map[player_y][player_x] += 'A'
                    oldstr = map[player_y + 1][player_x]
                    map[player_y + 1][player_x] = oldstr.replace('A', '')
                    path[player_y + 1][player_x] = 1
            knight.SetNewRoom((player_y, player_x))
            
        elif command == 'SHOT':
            score -= 100
            wp_x, wp_y = -1, -1
            if direction == 'LEFT':
                if map[player_y][player_x - 1].find('W') != -1:
                    wp_x = player_x - 1
                    wp_y = player_y
                    oldstr = map[wp_y][wp_x]
                    map[wp_y][wp_x] = oldstr.replace('W', '-')
                    path[wp_y][wp_x] = 1
                    if wp_y - 1 >= 0:
                        # Wumpus's left cell
                        oldstr = map[wp_y - 1][wp_x]
                        map[wp_y - 1][wp_x] = oldstr.replace('S', '-')
                    if wp_y + 1 < size:
                        # Wumpus's right cell
                        oldstr = map[wp_y + 1][wp_x]
                        map[wp_y + 1][wp_x] = oldstr.replace('S', '-')
                    if wp_x - 1 >= 0:
                        # Wumpus's upper cell
                        oldstr = map[wp_y][wp_x - 1]
                        map[wp_y][wp_x - 1] = oldstr.replace('S', '-')
                    if wp_x + 1 < size:
                        # Wumpus's lower cell
                        oldstr = map[wp_y][wp_x + 1]
                        map[wp_y][wp_x + 1] = oldstr.replace('S', '-')
                    knight.SetNewRoom((wp_y, wp_x))
                    wumpus_kill += 1
            elif direction == 'RIGHT':
                if map[player_y][player_x + 1].find('W') != -1:
                    wp_x = player_x + 1
                    wp_y = player_y
                    oldstr = map[wp_y][wp_x]
                    map[wp_y][wp_x] = oldstr.replace('W', '-')
                    path[wp_y][wp_x] = 1
                    if wp_y - 1 >= 0:
                        # Wumpus's left cell
                        oldstr = map[wp_y - 1][wp_x]
                        map[wp_y - 1][wp_x] = oldstr.replace('S', '-')
                    if wp_y + 1 < size:
                        # Wumpus's right cell
                        oldstr = map[wp_y + 1][wp_x]
                        map[wp_y + 1][wp_x] = oldstr.replace('S', '-')
                    if wp_x - 1 >= 0:
                        # Wumpus's upper cell
                        oldstr = map[wp_y][wp_x - 1]
                        map[wp_y][wp_x - 1] = oldstr.replace('S', '-')
                    if wp_x + 1 < size:
                        # Wumpus's lower cell
                        oldstr = map[wp_y][wp_x + 1]
                        map[wp_y][wp_x + 1] = oldstr.replace('S', '-')
                    knight.SetNewRoom((wp_y, wp_x))
                    wumpus_kill += 1
            elif direction == 'UP':
                if map[player_y - 1][player_x].find('W') != -1:
                    wp_x = player_x
                    wp_y = player_y - 1
                    oldstr = map[wp_y][wp_x]
                    map[wp_y][wp_x] = oldstr.replace('W', '-')
                    path[wp_y][wp_x] = 1
                    if wp_y - 1 >= 0:
                        # Wumpus's left cell
                        oldstr = map[wp_y - 1][wp_x]
                        map[wp_y - 1][wp_x] = oldstr.replace('S', '-')
                    if wp_y + 1 < size:
                        # Wumpus's right cell
                        oldstr = map[wp_y + 1][wp_x]
                        map[wp_y + 1][wp_x] = oldstr.replace('S', '-')
                    if wp_x - 1 >= 0:
                        # Wumpus's upper cell
                        oldstr = map[wp_y][wp_x - 1]
                        map[wp_y][wp_x - 1] = oldstr.replace('S', '-')
                    if wp_x + 1 < size:
                        # Wumpus's lower cell
                        oldstr = map[wp_y][wp_x + 1]
                        map[wp_y][wp_x + 1] = oldstr.replace('S', '-')
                    knight.SetNewRoom((wp_y, wp_x))
                    wumpus_kill += 1
            elif direction == 'DOWN':
                if map[player_y + 1][player_x].find('W') != -1:
                    wp_x = player_x
                    wp_y = player_y + 1
                    oldstr = map[wp_y][wp_x]
                    map[wp_y][wp_x] = oldstr.replace('W', '-')
                    path[wp_y][wp_x] = 1
                    if wp_y - 1 >= 0:
                        # Wumpus's left cell
                        oldstr = map[wp_y - 1][wp_x]
                        map[wp_y - 1][wp_x] = oldstr.replace('S', '-')
                    if wp_y + 1 < size:
                        # Wumpus's right cell
                        oldstr = map[wp_y + 1][wp_x]
                        map[wp_y + 1][wp_x] = oldstr.replace('S', '-')
                    if wp_x - 1 >= 0:
                        # Wumpus's upper cell
                        oldstr = map[wp_y][wp_x - 1]
                        map[wp_y][wp_x - 1] = oldstr.replace('S', '-')
                    if wp_x + 1 < size:
                        # Wumpus's lower cell
                        oldstr = map[wp_y][wp_x + 1]
                        map[wp_y][wp_x + 1] = oldstr.replace('S', '-')
                    knight.SetNewRoom((wp_y, wp_x))
                    wumpus_kill += 1
        elif command == 'TAKE GOLD':
            if map[player_y][player_x].find('G') != -1:
                score += 100
                gold_collect += 1
                oldstr = map[player_y][player_x]
                map[player_y][player_x] = oldstr.replace('G','-')
        elif command == 'CLIMB UP':
            score += 10
            draw_text("You won!", font1, red_ferrari, screen, size * 75 + 70, size + 500)
            game_over(wumpus_kill, gold_collect, score)

        
        for col in range(size):
            for row in range(size):
                if map[row][col].find('W') != -1:
                    if row - 1 >= 0:
                        map[row - 1][col] += 'S' if 'S' not in map[row - 1][col] else ''
                    if row + 1 < size:
                        map[row + 1][col] += 'S' if 'S' not in map[row + 1][col] else ''
                    if col - 1 >= 0:
                        map[row][col - 1] += 'S' if 'S' not in map[row][col - 1] else ''
                    if col + 1 < size:
                        map[row][col + 1] += 'S' if 'S' not in map[row][col + 1] else ''
        knight.SetMaze(map)

        # Print KB
        print('---------------------------------------')
        print(command)
        knight.PrintKB()
        print('Score: {0}'.format(score))

        pygame.display.update()
        mainClock.tick(240)
        time.sleep(2)

click = False

def game_over(n_wumpus_kill, n_gold_collect, score):
    while True:
        screen.fill(black)


        quit = pygame.Rect(size + 540, size + 550, 220, 120)
        pygame.draw.rect(screen, black, quit)
        screen.blit(background, (0,0))

        draw_text("GAMEOVER!", font6, red_ferrari, screen, size + 270, size)
        draw_text("Score:", font4, lemon, screen, size + 500, size + 200)
        draw_text(str(score), font5, black, screen, size + 700, size + 210)
        draw_text("Golds collected:", font4, lemon, screen, size + 400, size + 300)
        draw_text(str(n_gold_collect), font5, black, screen, size+ 910, size + 315)
        draw_text("Wumpuses killed:", font4, lemon, screen, size + 375, size + 400)
        draw_text(str(n_wumpus_kill), font5, black, screen, size + 940, size + 415)
        draw_text("Quit", font1, white, screen, size + 550, size + 520)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if quit.collidepoint((mx,my)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        mainClock.tick(240)

if __name__ == '__main__':
    game(x, y, map, gold)
