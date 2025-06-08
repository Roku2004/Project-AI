import sys

import pygame
import random

from Algorithms.Ghost_Move import Ghost_move_level4
from Algorithms.SearchAgent import SearchAgent
from Object.Food import Food
from Object.Player import Player
from Object.Wall import Wall
from Utils.utils import DDX, isValid2
from constants import *
from Object.Menu import Menu, Button

N = M = Score = _state_PacMan = 0
_map = []
_wall = []
_road = []
_food = []
_ghost = []
_food_Position = []
_ghost_Position = []
_visited = []
PacMan: Player
Level = 1
Map_name = ""

# Initial Pygame --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font_2 = pygame.font.SysFont('Comic Sans MS', 100)


# ------------------------------------------

def readMapInFile(map_name: str):
    f = open(map_name, "r")
    x = f.readline().split()
    global N, M, _map
    _map = []
    N, M = int(x[0]), int(x[1])
    for _ in range(N):
        line = f.readline().split()
        _m = []
        for j in range(M):
            _m.append(int(line[j]))
        _map.append(_m)

    global PacMan
    x = f.readline().split()

    MARGIN["TOP"] = max(0, (HEIGHT - N * SIZE_WALL) // 2)
    MARGIN["LEFT"] = max(0, (WIDTH - M * SIZE_WALL) // 2)
    PacMan = Player(int(x[0]), int(x[1]), IMAGE_PACMAN[0])

    f.close()


# --------------------------------- MAIN ---------------------

def check_Object(_map, row, col):
    if _map[row][col] == WALL:
        _wall.append(Wall(row, col, BLUE))

    # hidden else later
    else:
        pass
        # _road.append(Food(row, col, BLOCK_SIZE // 3, BLOCK_SIZE // 3, GREEN))

    if _map[row][col] == FOOD:
        _food.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, YELLOW))
        _food_Position.append([row, col])

    if _map[row][col] == MONSTER:
        _ghost.append(Player(row, col, IMAGE_GHOST[len(_ghost) % len(IMAGE_GHOST)]))
        _ghost_Position.append([row, col])

def initData() -> None:
    global N, M, _map, _food_Position, _food, _road, _wall, _ghost, _visited, Score, _state_PacMan, _ghost_Position
    N = M = Score = _state_PacMan = 0
    _map = []
    _wall = []
    _road = []
    _food = []
    _ghost = []
    _food_Position = []
    _ghost_Position = []

    readMapInFile(map_name=Map_name)
    _visited = [[0 for _ in range(M)] for _ in range(N)]

    for row in range(N):
        for col in range(M):
            check_Object(_map, row, col)


def Draw(_screen) -> None:
    for wall in _wall:
        wall.draw(_screen)
    for road in _road:
        road.draw(_screen)
    for food in _food:
        food.draw(_screen)
    for ghost in _ghost:
        ghost.draw(_screen)

    PacMan.draw(_screen)

    text_surface = my_font.render('Score: {Score}'.format(Score=Score), False, RED)
    screen.blit(text_surface, (0, 0))