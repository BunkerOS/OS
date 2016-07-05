from . import Window
from ..utils import *

class PicViewer(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Picture Viewer",
            version=1.0,
            pos=(50, 50),
            size=(500, 500),
            couleur=WHITE,
        )
        self.image = None
        self.state = WStates.UNACTIVE

    def load_image(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        if self.image.get_width() > self.size.x or self.image.get_height() > self.size.y:
            self.image = pygame.transform.scale(self.image, (self.size.x, int(self.image.get_width() / self.size.x * self.image.get_height())))

    def draw_content(self):
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))
        if self.image:
            self._content.blit(self.image, (0, 0))

    def trigger_user(self, event):
        pass
