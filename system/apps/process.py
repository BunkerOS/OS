# -*- coding: utf-8 -*-

from . import Window
from ..utils import *
from ..process_manager import *


class ProcessManagerWindow(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Process Manager",
            version=1.0,
            pos=(50, 50),
            size=(350, 500),
            couleur=WHITE
        )
        self.max_update = -1

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))

        text = font_petite.render("NAME", 1, BLACK)
        text2 = font_petite.render("UPDATE (ms)", 1, BLACK)
        text3 = font_petite.render("STATUS", 1, BLACK)
        self._content.blit(text, (0, 0))
        self._content.blit(text2, (175, 0))
        self._content.blit(text3, (275, 0))

        y, h = 30, 15
        s = "UNKNOW"
        for window in ProcessManager.windows():
            if window.state == WStates.ACTIVE:
                s = "ACTIVE"
            elif window.state == WStates.UNACTIVE:
                s = "UNACTIVE"
            elif window.state == WStates.NOT_RESPONDING:
                s = "NOT RESPONDING"

            name = font_petite.render(window.get_title(), 1, BLACK)
            status = font_petite.render(s, 1, BLACK)
            if len(ProcessManager.execution_datas()[window.id]['exc_times']) >= 1:
                t = (sum(ProcessManager.execution_datas()[window.id]['exc_times']) / len(ProcessManager.execution_datas()[window.id]['exc_times']))
                if t > self.max_update:
                    self.max_update = t
                dt = "%3.2f" % t
            else:
                dt = "NONE"
            if self.max_update != -1:
                if float(dt) <= 0.25 * self.max_update:
                    pygame.draw.rect(self._content, LIGHT_BLUE, (0, y, self.size.x, h))
                elif 0.25 < float(dt) <= 0.5 * self.max_update:
                    pygame.draw.rect(self._content, LIGHT_GREEN, (0, y, self.size.x, h))
                elif 0.5 < float(dt) <= 0.75 * self.max_update:
                    pygame.draw.rect(self._content, LIGHT_YELLOW, (0, y, self.size.x, h))
                elif 0.75 < float(dt):
                    pygame.draw.rect(self._content, LIGHT_RED, (0, y, self.size.x, h))
            dt = font_petite.render(dt, 1, BLACK)
            self._content.blit(name, (4, y))
            self._content.blit(dt, (175, y))
            self._content.blit(status, (275, y))
            y += h

    def trigger_user(self, event):
        if event.type == MOUSEBUTTONUP:
            x, y = event.pos
            real_select = (y - 15) // 15
            if 0 <= real_select < len(ProcessManager.windows()):
                if ProcessManager.windows()[real_select].state != WStates.UNACTIVE:
                    ProcessManager.windows()[real_select].set_alive(WStates.UNACTIVE)
