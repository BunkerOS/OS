import pygame
from pygame.locals import *
from enum import Enum


class WStates(Enum):
    def __init__(self, state):
        self.state = state

    ACTIVE = 0
    UNACTIVE = 1
    NOT_RESPONDING = 2


class Point:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new):
        self._x = new

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new):
        self._y = new

    def translate(self, nx, ny):
        self.x += nx
        self.y += ny

    def __iter__(self):
        yield self.x
        yield self.y


RED = (180, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 180)
YELLOW = (0, 180, 180)
PURPLE = (180, 0, 180)
ORANGE = (180, 180, 0)

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

PASTEL_BLUE = (40, 40, 150)
PASTEL_RED = (150, 40, 40)
PASTEL_GREEN = (40, 150, 40)
PASTEL_YELLOW = (40, 150, 150)
PASTEL_PURPLE = (150, 40, 150)
PASTEL_ORANGE = (150, 150, 40)

LIGHT_BLUE = (116, 208, 241)
LIGHT_RED = ()
LIGHT_GREEN = ()
LIGHT_YELLOW = ()
LIGHT_PURPLE = ()
LIGHT_ORANGE = ()

LIGHT_GREY = (172, 172, 172)

DARK_BLUE = ()
DARK_RED = ()
DARK_GREEN = ()
DARK_YELLOW = ()
DARK_PURPLE = ()
DARK_ORANGE = ()

pygame.font.init()
font = pygame.font.Font("system/resx/fonts/Hack-Regular.ttf", 16)
font_petite = pygame.font.Font("system/resx/fonts/Hack-Regular.ttf", 12)
sample_text = font.render("a", 1, BLACK)
