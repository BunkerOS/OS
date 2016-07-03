#-*-coding:Utf-8-*-

import time
from .utils import *
from . import process_manager
from . import connect


class DesktopManager:
    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.show_main_menu = False
        self.tskb_size = (120, self.screen.get_height())
        self.cl_tskb = GREEN
        self.main_txt_tsk_bar = pygame.image.load("system/resx/logo.png").convert_alpha()
        self._content = pygame.Surface((self.screen.get_width() - self.tskb_size[0], self.screen.get_height()))

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
            i.draw()
        self.draw_task_bar()
        self.main_button_tsk_bar()
        self.print_time()
        if self.show_main_menu:
            self.draw_main_menu()
        self.screen.blit(self._content, (self.tskb_size[0], 0))

    def draw_main_menu(self):
        pass

    def draw_task_bar(self):
        pygame.draw.rect(self.screen, self.cl_tskb, (0, 0) + self.tskb_size)
        y = self.main_txt_tsk_bar.get_height() + 10
        dispo = (self.tskb_size[0] - 8) // 6
        color = RED
        for i in process_manager.ProcessManager.windows():
            if i.state == WStates.ACTIVE:
                color = WHITE
            elif i.state == WStates.UNACTIVE:
                color = BLACK
            elif i.state == WStates.NOT_RESPONDING:
                color = BLUE
            elif i.state == WStates.WAITING:
                color = YELLOW
            txt = font_petite.render(i.get_title()[:dispo], 1, color)
            self.screen.blit(txt, (4, y))
            y += txt.get_height() + 4

    def main_button_tsk_bar(self):
        pygame.draw.rect(self.screen, YELLOW, (0, 0, self.tskb_size[0], self.main_txt_tsk_bar.get_height()))
        self.screen.blit(self.main_txt_tsk_bar, (0, 0))

    def select_prog(self, y):
        real_select = (y - self.main_txt_tsk_bar.get_height() - 10) // 14
        if 0 <= real_select < len(process_manager.ProcessManager.windows()):
            if real_select < len(process_manager.ProcessManager.windows()):
                process_manager.ProcessManager.set_as_toplevel(real_select)

    def kill_prog(self, y):
        real_select = (y - self.main_txt_tsk_bar.get_height() - 10) // 14
        if 0 <= real_select < len(process_manager.ProcessManager.windows()):
            if real_select < len(process_manager.ProcessManager.windows()):
                process_manager.ProcessManager.kill_process(real_select)

    def print_time(self):
        t = time.strftime("%A")
        self.screen.blit(font_petite.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 42))
        t = time.strftime("%H : %M : %S")
        self.screen.blit(font_petite.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 14))
        t = time.strftime("%d %B")
        self.screen.blit(font_petite.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 28))

    def trigger(self, event):
        if event.type == MOUSEBUTTONDOWN and event.pos[0] > self.tskb_size[0] or event.type != MOUSEBUTTONDOWN:
            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
                event.pos = (event.pos[0] - self.tskb_size[0], event.pos[1])
            if process_manager.ProcessManager.get_first_active():
                process_manager.ProcessManager.get_first_active().trigger(event)
        elif event.type == MOUSEBUTTONDOWN and event.pos[0] <= self.tskb_size[0] and event.pos[1] > self.main_txt_tsk_bar.get_height():
            if event.button == 1:
                self.select_prog(event.pos[1])
            elif event.button == 3:
                self.kill_prog(event.pos[1])
        elif event.type == MOUSEBUTTONDOWN and 0 <= event.pos[0] <= self.tskb_size[0] and 0 <= event.pos[1] <= self.main_txt_tsk_bar.get_height():
            self.show_main_menu = True
