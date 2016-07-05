from . import Window
from .. import widgets
from ..utils import *
import re


class EditeurTexte(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Text Editor",
            version=1.0,
            pos=(screen.get_width() // 2, 0),
            size=(screen.get_width() // 2, screen.get_height() // 2),
            couleur=WHITE
        )
        self.texts = {
            "content": [],
            "cli_datas": {"line": 0, "char": 0},
            "cli": font.render("_", 1, RED)
        }
        self.text = ""
        self.curseur = 0
        self.offsets = Point(0, 0)
        self.widgets.append(widgets.Button(self._content, pos=(0, 0), size=(40, 25), bg_color=LIGHT_GREY, fg_color=BLACK, mouseover_color=GREY, text="Open", text_centered=True))
        self.widgets.append(widgets.Button(self._content, pos=(45, 0), size=(40, 25), bg_color=LIGHT_GREY, fg_color=BLACK, mouseover_color=GREY, text="Save", text_centered=True))
        self.widgets[0].register(print, "open")
        self.widgets[1].register(print, "save")

    def open(self, path):
        with open(path, encoding="utf-8") as file:
            self.text = file.read()
        self.offsets.x = 0
        self.offsets.y = 0
        self.curseur = 0

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, tuple(self.offsets) + tuple(self.size))
        y = 25

        # texte
        for li, line in enumerate(self.texts["content"]):
            if li == self.texts["cli_datas"]["line"]:
                self._content.blit(self.texts["cli"], (self.texts["cli_datas"]["char"] * sample_text.get_width() + self.offsets.x, y + 2 + self.offsets.y))
            self._content.blit(line, (self.offsets.x, y + self.offsets.y))
            y += line.get_height() + 2

        # barre menu
        pygame.draw.rect(self._content, LIGHT_GREY, (0, 0, self.size.x, 25))

    def trigger_user(self, event):
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.text = self.text[:self.curseur] + self.text[self.curseur + 1:]
                self.curseur -= 1
            elif event.key == K_DELETE:
                self.text = self.text[:self.curseur] + self.text[self.curseur + 1:]
            elif event.key in (K_RETURN, K_KP_ENTER):
                self.text += "\n"
                self.curseur += 1
            elif event.key == K_TAB:
                self.text += " " * 4
                self.curseur += 4
            elif event.key == K_LEFT:
                if self.curseur > 0:
                    self.curseur -= 1
            elif event.key == K_RIGHT:
                if self.curseur < len(self.text) - 1:
                    self.curseur += 1
            else:
                self.text += event.unicode
                self.curseur += 1
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                self.offsets.y -= sample_text.get_height()
            elif event.button == 5:
                self.offsets.y += sample_text.get_height()

    # TODO: ne générer que la partie visible du texte
    def update_user(self):
        text = self.text.split('\n')
        self.texts['content'] = []
        tot = 0
        for li, line in enumerate(text):
            for ch, char in enumerate(line):
                if tot == self.curseur:
                    self.texts["cli_datas"]["line"] = li
                    self.texts["cli_datas"]["char"] = ch
                    break
                tot += 1
            self.texts['content'].append(font.render(line, 1, BLACK))
