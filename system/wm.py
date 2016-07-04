#-*-coding:Utf-8-*-

import time
import os
import math
from glob import glob
from .utils import *
from . import process_manager
from . import connect


class DesktopManager:
    def __init__(self, screen):
        self.screen = screen
        self.session = "NONE"
        self.done = False
        self.show_main_menu = False
        self.tskb_size = (120, self.screen.get_height())
        self.cl_tskb = GREEN
        self.apps = []
        self.dl_apps = []
        self.texts = {
            "bapps": font.render("Bunker Apps", 1, BLACK),
            "uapps": font.render("User Apps", 1, BLACK),
            "load": font.render("Load Apps list", 1, BLACK)
        }
        self.main_txt_tsk_bar = pygame.image.load("system/resx/logo.png").convert_alpha()
        self._content = pygame.Surface((self.screen.get_width() - self.tskb_size[0], self.screen.get_height()))

    def load_apps_list(self):
        self.apps = []
        self.dl_apps = []

        for file in glob("system/apps/*.py"):
            fname = os.path.basename(file)
            if fname != '__init__.py':
                self.apps.append(fname[:-3])
        self.apps = sorted(self.apps)
        apps = []
        for app in self.apps:
            apps.append(font.render(app, 1, BLACK))
        self.apps = list(zip(self.apps, apps[:]))

        for file in glob("apps/*.py"):
            fname = os.path.basename(file)
            if fname != '__init__.py':
                self.dl_apps.append(fname[:-3])
        self.dl_apps = sorted(self.dl_apps)
        uapps = []
        for uapp in self.dl_apps:
            uapps.append(font.render(uapp, 1, BLACK))
        self.dl_apps = list(zip(self.dl_apps, uapps[:]))

    def update(self):
        # process_manager.ProcessManager.reoder_ifalive()
        self.draw()
        for win in process_manager.ProcessManager.windows():
            process_manager.ProcessManager.update_process(win)
        pygame.display.flip()

    # TODO: prévoir un écran de connexion
    def on_start(self):
        start_screen = connect.Connect()
        start_screen.run()
        self.session = start_screen.session[1]
        process_manager.ProcessManager.set_session(self.session)

        process_manager.ProcessManager.init_windows_with(self._content)
        w, h = self.main_txt_tsk_bar.get_size()
        self.main_txt_tsk_bar = pygame.transform.scale(self.main_txt_tsk_bar,
            (self.tskb_size[0], int(self.tskb_size[0] / w * h))
        )

    # TODO: prévoir un écran de déconnexion
    def on_end(self):
        pass

    def run(self):
        self.on_start()

        while not self.done:
            process_manager.ProcessManager.clock().tick()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.done = True
                else:
                    self.trigger(event)
            self.update()

        self.on_end()

    def draw(self):
        pygame.draw.rect(self._content, BLACK, (0, 0) + self._content.get_size())

        for i in process_manager.ProcessManager.windows()[::-1]:
            process_manager.ProcessManager.draw_process(i)
        self.draw_task_bar()
        self.main_button_tsk_bar()
        self.print_time()
        if self.show_main_menu:
            self.draw_main_menu()
        self.screen.blit(self._content, (self.tskb_size[0], 0))

    def draw_main_menu(self):
        pygame.draw.rect(self._content, PURPLE, (0, 0, 250, 375))
        self._content.blit(self.texts['bapps'], (10, 10))
        self._content.blit(self.texts['uapps'], (220 - self.texts['uapps'].get_width(), 10))
        y = 30
        for i, bapp in enumerate(self.apps):
            self._content.blit(bapp[1], (10, y + i * 20))
        for i, uapp in enumerate(self.dl_apps):
            self._content.blit(uapp[1], (220 - self.texts['uapps'].get_width(), y + i * 20))
        pygame.draw.rect(self._content, GREEN, (
            238 - self.texts['load'].get_width(), 363 - self.texts['load'].get_height(),
            4 + self.texts['load'].get_width(), 4 + self.texts['load'].get_height()
        ))
        self._content.blit(self.texts['load'], (240 - self.texts['load'].get_width(), 365 - self.texts['load'].get_height()))

    def draw_task_bar(self):
        pygame.draw.rect(self.screen, self.cl_tskb, (0, 0) + self.tskb_size)
        y = self.main_txt_tsk_bar.get_height() + 10
        dispo = math.ceil(self.tskb_size[0] / sample_text.get_width())
        color = RED
        xm, ym = pygame.mouse.get_pos()
        mo = self.mouseover_prog(ym)
        for i, w in enumerate(process_manager.ProcessManager.windows()):
            if w.state == WStates.ACTIVE:
                color = WHITE
            elif w.state == WStates.UNACTIVE:
                color = BLACK
            elif w.state == WStates.NOT_RESPONDING:
                color = BLUE
            elif w.state == WStates.WAITING:
                color = YELLOW

            txt = font_petite.render(w.get_title()[:dispo], 1, color)
            if i == mo and xm <= self.tskb_size[0]:
                pygame.draw.rect(self.screen, RED, (0, y - 2, self.tskb_size[0], txt.get_height() + 4))
            self.screen.blit(txt, (4, y))
            y += txt.get_height() + 4

    def main_button_tsk_bar(self):
        pygame.draw.rect(self.screen, YELLOW, (0, 0, self.tskb_size[0], self.main_txt_tsk_bar.get_height()))
        self.screen.blit(self.main_txt_tsk_bar, (0, 0))

    def mouseover_prog(self, y):
        real_select = (y - self.main_txt_tsk_bar.get_height() - 10) // sample_text.get_height()
        if 0 <= real_select < len(process_manager.ProcessManager.windows()):
            return real_select
        return - 1

    def select_prog(self, y):
        process_manager.ProcessManager.set_as_toplevel(y)

    def kill_prog(self, y):
        process_manager.ProcessManager.remove_process(y)

    def print_time(self):
        t = time.strftime("%A")
        self.screen.blit(font.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 46))
        t = time.strftime("%d %B")
        self.screen.blit(font.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 32))
        t = time.strftime("%H:%M :%S")
        self.screen.blit(font.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 18))

    def trigger(self, event):
        # clic hors de la barre des taches
        if (event.type == MOUSEBUTTONDOWN and event.pos[0] > self.tskb_size[0]) or event.type != MOUSEBUTTONDOWN:
            # correction de la position
            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
                event.pos = (event.pos[0] - self.tskb_size[0], event.pos[1])
            # clic dans le menu
            if self.show_main_menu and event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                dimension = (238 - self.texts['load'].get_width(), 363 - self.texts['load'].get_height(),
                             4 + self.texts['load'].get_width(), 4 + self.texts['load'].get_height())
                if dimension[0] <= x <= dimension[0] + dimension[2] and dimension[1] <= y <= dimension[1] + dimension[3]:
                    self.load_apps_list()
            # mise en actif d'un processus
            w = process_manager.ProcessManager.get_first_active()
            if w:
                if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
                    event.pos = (event.pos[0] - w.pos.x, event.pos[1] - w.pos.y)
                w.trigger(event)
        # clic sur la barre des taches
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            # select/kill prog
            if x <= self.tskb_size[0] and y > self.main_txt_tsk_bar.get_height():
                mo = self.mouseover_prog(y)
                if mo != -1:
                    if event.button == 1:
                        self.select_prog(mo)
                    elif event.button == 3:
                        self.kill_prog(mo)
            # activation ou non du menu
            elif 0 <= x <= self.tskb_size[0] and 0 <= y <= self.main_txt_tsk_bar.get_height():
                self.show_main_menu = not self.show_main_menu
