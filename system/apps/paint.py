from . import Window
from ..utils import *


class Paint(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Paint",
            version=1.0,
            pos=(0, 0),
            size=(500, 500),
            couleur=WHITE
        )
        self.state = WStates.UNACTIVE

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))

    def trigger_user(self, event):
        pass

    def update_user(self):
        pass
