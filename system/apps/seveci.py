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

    def start(self, file):
        self.file = iter(sh.eval_and_exec(file))

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

    def update(self):
        try:
            if self.file:
                self.output += next(self.file) + "\n"
        except StopIteration:
            pass
        self.texts["content"] = []
        for line in self.output.split("\n"):
            self.texts["content"].append(font.render(line, 1, WHITE))
