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

def generate_Ghost_new_position(_ghost, _type: int = 0) -> list[list[int]]:
    _ghost_new_position = []
    if _type == 1:
        for idx in range(len(_ghost)):
            [row, col] = _ghost[idx].getRC()

            rnd = random.randint(0, 3)
            new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]
            while not isValid2(_map, new_row, new_col, N, M):
                rnd = random.randint(0, 3)
                new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]

            _ghost_new_position.append([new_row, new_col])

    # update latest
    elif _type == 2:
        for idx in range(len(_ghost)):
            [start_row, start_col] = _ghost[idx].getRC()
            [end_row, end_col] = PacMan.getRC()
            _ghost_new_position.append(Ghost_move_level4(_map, start_row, start_col, end_row, end_col, N, M))

    return _ghost_new_position


def check_collision_ghost(_ghost, pac_row=-1, pac_col=-1) -> bool:
    Pac_pos = [pac_row, pac_col]
    if pac_row == -1:
        Pac_pos = PacMan.getRC()
    for g in _ghost:
        Ghost_pos = g.getRC()
        if Pac_pos == Ghost_pos:
            return True

    return False

def change_direction_PacMan(new_row, new_col):
    global PacMan, _state_PacMan
    [current_row, current_col] = PacMan.getRC()
    _state_PacMan = (_state_PacMan + 1) % len(IMAGE_PACMAN)

    if new_row > current_row:
        PacMan.change_state(-90, IMAGE_PACMAN[_state_PacMan])
    elif new_row < current_row:
        PacMan.change_state(90, IMAGE_PACMAN[_state_PacMan])
    elif new_col > current_col:
        PacMan.change_state(0, IMAGE_PACMAN[_state_PacMan])
    elif new_col < current_col:
        PacMan.change_state(180, IMAGE_PACMAN[_state_PacMan])


def randomPacManNewPos(_map, row, col, _N, _M):
    for [d_r, d_c] in DDX:
        new_r, new_c = d_r + row, d_c + col
        if isValid2(_map, new_r, new_c, _N, _M):
            return [new_r, new_c]
