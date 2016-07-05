from . utils import *
from . import bad_2048
from glob import glob
import os
import time


TIMER_LOGIN = 3


class Connect:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.files = {}
        self.done = False
        self.connected = False
        self.user_pwd = ""
        self.session = (0, "user")
        self.session_text = font.render(self.session[1], 1, BLACK)
        self.text = font.render("", 1, WHITE)
        self.max_len_pwd = 20
        self.quitter = font.render("Quitter", 1, WHITE)
        self.wrong = font.render("WRONG", 1, BLACK)
        self.pos_text_box = ((self.screen.get_width() - 200) // 2, (self.screen.get_height() - 20) // 2)
        self.error_box_pos = ((self.screen.get_width() - 225) // 2, (self.screen.get_height() - 150) // 2)
        self.wrong_pos = ((self.screen.get_width() - self.wrong.get_width()) // 2, (self.screen.get_height() - self.wrong.get_height()) // 2)
        self.avatar_pos = ((self.screen.get_width() - 200) // 2, (self.screen.get_height() - 200) // 2 - 200)
        self.user_pos = ((self.screen.get_width() - self.session_text.get_width()) // 2, (self.screen.get_height() - self.session_text.get_height()) // 2 - 50)
        try:
            self.sessions = eval(open("system/datas/sessions.bad").read())
        except SyntaxError:
            raise RuntimeError("Sessions corrupted. Can not continue.")
        else:
            for s in self.sessions:
                if s['name'] != "guest" and s['password'] == []:
                    raise RuntimeError('Empty password, can not continue')

    def load(self):
        _sessions = [e['name'] for e in self.sessions]
        for file in glob("system/resx/connect/*.png"):
            self.files[os.path.basename(file).split('.')[0]] = pygame.image.load(file).convert_alpha()
            if os.path.basename(file).split('.')[0] in _sessions:
                self.files[os.path.basename(file).split('.')[0]] = pygame.transform.scale(self.files[os.path.basename(file).split('.')[0]], (200, 200))
        self.files["logo"] = pygame.image.load("system/resx/logo.png").convert_alpha()

    def _check(self):
        if bad_2048.crypt(4, self.user_pwd) == self.sessions[self.session[0]]["password"]:
            self.connected = True
            self.done = True
        else:
            self.user_pwd = ""
            self._error("Wrong password")

    def _error(self, message):
        self.wrong = font.render(message, 1, BLACK)
        self.wrong_pos = ((self.screen.get_width() - self.wrong.get_width()) // 2, (self.screen.get_height() - self.wrong.get_height()) // 2)

        while True:
            ev = pygame.event.poll()
            if ev.type == KEYDOWN and ev.key == K_RETURN:
                break

            pygame.draw.rect(self.screen, RED, self.error_box_pos + (255, 150))
            self.screen.blit(self.wrong, self.wrong_pos)

            pygame.display.flip()

    def _change_session(self, new):
        for i, e in enumerate(self.sessions):
            if i == new:
                self.session = (i, e['name'])
                self.session_text = font.render(self.session[1], 1, BLACK)
                self.user_pos = ((self.screen.get_width() - self.session_text.get_width()) // 2, (self.screen.get_height() - self.session_text.get_height()) // 2 - 50)
                if self.session[1] == "guest":
                    self.connected = True
                    self.done = True
                return
        self._error("Non existing session")

    def _welcome(self):
        until = time.time() + TIMER_LOGIN
        w, h = 200, 20
        bar_size = lambda: (TIMER_LOGIN - (until - time.time())) / TIMER_LOGIN * w

        xsc, ysc = self.screen.get_width() // 2, self.screen.get_height() // 2
        xl, yl = self.files['logo'].get_width(), self.files['logo'].get_height()
        xc, yc = lambda x: xsc - x // 2, lambda y: ysc - y // 2

        while time.time() <= until:
            pygame.draw.rect(self.screen, PASTEL_GREEN, (0, 0) + self.screen.get_size())
            self.screen.blit(self.files['logo'], (xc(xl), yc(yl)))

            # barre de chargement
            pygame.draw.rect(self.screen, BLACK, (xc(w) - 2, yc(h) + 2 * yl // 3 - 2, w + 4, h + 4))
            a = int(bar_size())
            pygame.draw.rect(self.screen, LIGHT_BLUE, (xc(w), yc(h) + 2 * yl // 3, a, h))

            ev = pygame.event.poll()

            pygame.display.flip()

    def run(self):
        self.load()

        while not self.done:
            pygame.draw.rect(self.screen, PASTEL_BLUE, (0, 0) + self.screen.get_size())
            pygame.draw.rect(self.screen, PASTEL_ORANGE, (4 * self.screen.get_width() / 5, 0, self.screen.get_width() / 5, self.screen.get_height()))
            self.screen.blit(font.render("Sessions", 1, BLACK), (4 * self.screen.get_width() / 5 + 10, 10))
            for i, s in enumerate(self.sessions):
                self.screen.blit(font.render("-> " + s['name'], 1, BLACK), (4 * self.screen.get_width() / 5 + 10, 50 + i * 40))
                self.screen.blit(font.render("_" * int(self.screen.get_width() / 5 / sample_text.get_width() - 1), 1, BLACK), (4 * self.screen.get_width() / 5 + 10, 55 + i * 40))

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # sessions
                    if x >= 4 * self.screen.get_width() / 5:
                        ry = (y - 50) // 40
                        if 0 <= ry < len(self.sessions):
                            self._change_session(ry)
                    if 0 <= x <= self.quitter.get_width() and self.screen.get_height() - self.quitter.get_height() <= y <= self.screen.get_height():
                        exit()
                if event.type == KEYDOWN:
                    if event.key in (K_RETURN, K_KP_ENTER):
                        self._check()
                    elif event.key == K_ESCAPE:
                        self.done = True
                    elif event.key == K_BACKSPACE:
                        self.user_pwd = self.user_pwd[:-1]
                    else:
                        if len(self.user_pwd) < self.max_len_pwd:
                            self.user_pwd += event.unicode
                    self.text = font.render("*" * len(self.user_pwd), 1, WHITE)

            self.screen.blit(self.quitter, (0, self.screen.get_height() - self.quitter.get_height()))
            pygame.draw.rect(self.screen, GREY, (self.pos_text_box[0] - 2, self.pos_text_box[1] - 2, 204, 24))
            pygame.draw.rect(self.screen, BLACK, self.pos_text_box + (200, 20))
            self.screen.blit(self.text, ((self.screen.get_width() - self.text.get_width()) // 2, (self.screen.get_height() - self.text.get_height()) // 2))
            self.screen.blit(self.files[self.session[1]], self.avatar_pos)
            self.screen.blit(self.session_text, self.user_pos)

            pygame.display.flip()

        if self.connected:
            self._welcome()
        else:
            exit()
