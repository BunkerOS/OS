from . import Window
from ..utils import *
from .. import seveci as sh


class SeveciShell(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Seveci Shell",
            version=1.0,
            pos=(50, 80),
            size=(500, 300),
            couleur=BLACK
        )
        self.texts = {
            "content": [],
            "main": font.render("Seveci 1.0 interpreter", 1, WHITE)
        }
        self.output = ""
        self.file = None
        self.offset = 0
        self.state = WStates.UNACTIVE

    def start(self, file):
        self.file = iter(sh.eval_and_exec(file))

    def print(self, text):
        self.output += text + "\n"
        self.update_text()
        self.draw()

    def input(self, text):
        ret = ""
        self.output += text
        self.update_text()
        while True:
            ev = pygame.event.poll()
            if ev.type == KEYDOWN:
                if ev.key not in (K_RETURN, K_KP_ENTER):
                    ret += ev.unicode
                    self.output += ev.unicode
                else:
                    self.output += "\n"
                    break
                self.update_text()
            self.draw()

            pygame.display.flip()
        return ret

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))

        # texte
        self._content.blit(self.texts["main"], (5, 5))
        y = self.texts["main"].get_height() + 10 + self.offset
        for t in self.texts["content"]:
            if 0 <= y <= self.size.y:
                self._content.blit(t, (5, y))
            else:
                self.offset = -y
            y += t.get_height() + 5

    def trigger_user(self, event):
        if event.type == KEYUP:
            if event.key in (K_KP_ENTER, K_RETURN):
                self.state = WStates.UNACTIVE

    def update_text(self):
        self.texts["content"] = []
        for line in self.output.split("\n"):
            self.texts["content"].append(font.render(line, 1, WHITE))

    def update_user(self):
        try:
            if self.file:
                self.output += str(next(self.file)) + "\n"
        except StopIteration:
            pass
        self.update_text()
