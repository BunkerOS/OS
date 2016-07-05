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
            size=(450, 500),
            couleur=WHITE
        )
        self.max_update = -1
        self.texts = {
            "name": font_petite.render("NAME", 1, BLACK),
            "update": font_petite.render("UPDATE (ms)", 1, BLACK),
            "draw": font_petite.render("DRAW (ms)", 1, BLACK),
            "status": font_petite.render("STATUS", 1, BLACK),
            "session": font_petite.render("Running under : %s" % ProcessManager.session(), 1, BLACK)
        }

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))

        self._content.blit(self.texts["session"], (0, 0))
        self._content.blit(font_petite.render(" | FPS: %3.2f" % ProcessManager.clock().get_fps(), 1, BLACK), (self.texts["session"].get_width(), 0))
        self._content.blit(self.texts["name"], (0, 30))
        self._content.blit(self.texts["update"], (175, 30))
        self._content.blit(self.texts["draw"], (275, 30))
        self._content.blit(self.texts["status"], (375, 30))

        y, h = 50, 15
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
            if len(ProcessManager.execution_datas()[window.id]['draw_times']) >= 1:
                t = (sum(ProcessManager.execution_datas()[window.id]['draw_times']) / len(ProcessManager.execution_datas()[window.id]['draw_times']))
                draw = "%3.2f" % t
            else:
                draw = "NONE"

            if self.max_update != -1 and dt != "NONE":
                if float(dt) <= 0.25 * self.max_update:
                    pygame.draw.rect(self._content, LIGHT_BLUE, (0, y, self.size.x, h))
                elif 0.25 * self.max_update < float(dt) <= 0.5 * self.max_update:
                    pygame.draw.rect(self._content, LIGHT_GREEN, (0, y, self.size.x, h))
                elif 0.5 * self.max_update < float(dt) <= 0.75 * self.max_update:
                    pygame.draw.rect(self._content, LIGHT_YELLOW, (0, y, self.size.x, h))
                elif 0.75 * self.max_update < float(dt):
                    pygame.draw.rect(self._content, LIGHT_RED, (0, y, self.size.x, h))

            dt = font_petite.render(dt, 1, BLACK)
            draw = font_petite.render(draw, 1, BLACK)

            self._content.blit(name, (4, y))
            self._content.blit(dt, (200, y))
            self._content.blit(draw, (275, y))
            self._content.blit(status, (375, y))

            y += h

    def trigger_user(self, event):
        if event.type == MOUSEBUTTONUP:
            x, y = event.pos
            real_select = (y - 15) // 15
            if 0 <= real_select < len(ProcessManager.windows()):
                if ProcessManager.windows()[real_select].state != WStates.UNACTIVE:
                    ProcessManager.windows()[real_select].set_alive(WStates.UNACTIVE)
