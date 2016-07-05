# -*- coding: utf-8 -*-

from . import Window
from ..utils import *
import time


class KeysRepeatWindow(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Keys Repeat Setting",
            version=1.0,
            pos=(screen.get_width() - 400, screen.get_height() - 170 - EPAISSEUR_BARRE),
            size=(400, 170),
            couleur=WHITE
        )
        self.before, self.then = "200", "100"
        self.changing_first = True
        self.texts = {
            "ex": font_petite.render("1st box:set the time before repeating", 1, BLACK),
            "ex2": font_petite.render("2nd box:set the time between each repeat", 1, BLACK),
            "done": font.render("Done !", 1, BLACK)
        }
        self.box1 = (10, 60, 100, 100)
        self.box2 = (290, 60, 100, 100)
        self.print_done = False
        self.done_time = -1

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))
        if not self.print_done:
            self._content.blit(self.texts['ex'], (10, 10))
            self._content.blit(self.texts['ex2'], (10, 30))
        else:
            self._content.blit(self.texts['done'], (10, 10))

        if self.changing_first:
            pygame.draw.rect(self._content, LIGHT_BLUE, (self.box1[0] - 2, self.box1[1] - 2, self.box1[2] + 4, self.box1[3] + 4))
        else:
            pygame.draw.rect(self._content, LIGHT_BLUE, (self.box2[0] - 2, self.box2[1] - 2, self.box2[2] + 4, self.box2[3] + 4))
        pygame.draw.rect(self._content, GREY, self.box1)
        pygame.draw.rect(self._content, GREY, self.box2)
        bef = font.render(str(self.before), 1, BLACK)
        the = font.render(str(self.then), 1, BLACK)
        self._content.blit(bef, (self.box1[0] + self.box1[2] // 2 - bef.get_width() // 2, self.box1[1] + self.box1[3] // 2 - bef.get_height() // 2))
        self._content.blit(the, (self.box2[0] + self.box2[2] // 2 - the.get_width() // 2, self.box2[1] + self.box2[3] // 2 - the.get_height() // 2))

    def trigger_user(self, event):
        if event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT):
                self.changing_first = not self.changing_first
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                if self.before.isdigit() and self.then.isdigit():
                    pygame.key.set_repeat(int(self.before), int(self.then))
                    self.print_done = True
                    self.done_time = time.time() + 5
            elif event.key == K_BACKSPACE:
                if self.changing_first:
                    self.before = self.before[:-1]
                else:
                    self.then = self.then[:-1]
            else:
                if self.changing_first:
                    self.before += event.unicode
                else:
                    self.then += event.unicode

    def update(self):
        if self.done_time != -1 and time.time() >= self.done_time:
            self.print_done = False
            self.done_time = -1
