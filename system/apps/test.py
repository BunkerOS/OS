from . import Window
from ..utils import *
from ..process_manager import ProcessManager


class App(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="FPS",
            version=1.0,
            pos=(50, 80),
            size=(100, 100),
            couleur=WHITE
        )

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))

        fps = font.render(str(int(ProcessManager.clock().get_fps())), 1, BLACK)
        self._content.blit(fps, ((100 - fps.get_width()) // 2, (100 - fps.get_height()) // 2))

    def trigger_user(self, event):
        pass

    def update(self):
        pass
