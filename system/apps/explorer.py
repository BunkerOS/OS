from . import Window
from .. import widgets
from ..utils import *
from ..process_manager import ProcessManager
import os
from glob import glob

BLOC_SIZE = 100


class Explorer(Window):
    def __init__(self, screen):
        Window.__init__(
            self,
            screen,
            titre="Explorer",
            version=1.0,
            pos=(0, screen.get_height() - 4 * BLOC_SIZE),
            size=(6 * BLOC_SIZE, 4 * BLOC_SIZE),
            couleur=WHITE
        )
        self.texts = {}
        self.images = {
            os.path.basename(f).split('.')[0]: pygame.image.load(f).convert_alpha() for f in glob("system/resx/icons/*.png")
        }
        self.offsets = Point(0, 0)
        self.history = []
        self.files = []
        self.hcursor = -1
        self.directory = ""
        self.load_dir("users/%s/" % ProcessManager.session())

    def launch_with(self, path):
        name, ext = os.path.basename(path).split('.')
        if ext == "png":
            ProcessManager.access_window("Picture Viewer", "load_image", path)
        elif ext == "wav":
            print("reading music :p")
        elif ext == "sev":
            ProcessManager.access_window("Seveci Shell", "start", path)
        else:
            # bad, code, py et tous les autres
            ProcessManager.access_window("Text Editor", "open", path)

    def load_dir(self, path, do_not_log=False):
        if not do_not_log:
            self.history.append(path)
        self.directory = path
        self.widgets = []
        self.files = []

        for i, file in enumerate(glob(path + "*")):
            self.files.append(file)

            x, y = (i % 6) * BLOC_SIZE, (i // 6) * BLOC_SIZE + 25

            kind = "fichier"
            name, *ext = os.path.basename(file).split('.')
            if ext == [] and name != "Apps":
                kind = "dossier"
            elif ext == [] and name == "Apps":
                kind = "dossier-app"
            elif ext == ['png']:
                kind = "fichier-img"
            elif ext == ['py']:
                kind = "fichier-app"
            elif ext == ['sev'] or ext == ['code']:
                kind = "fichier-code"
            elif ext == ['bad']:
                kind == "fichier-data"
            elif ext == ['wav']:
                kind = "fichier-son"

            self.widgets.append(widgets.ImageWithAlt(
                self._content, pos=(x, y), size=(BLOC_SIZE, BLOC_SIZE), bg_color=WHITE, fg_color=BLACK,
                image=self.images[kind], mouseover_color=LIGHT_GREY, text=os.path.basename(file), text_centered=True
            ))
            if kind in ("dossier", "dossier-app"):
                self.widgets[-1].register(self.load_dir, file + "/")
            else:
                self.widgets[-1].register(self.launch_with, file)

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, tuple(self.offsets) + tuple(self.size))
        y = 25

        # barre menu
        pygame.draw.rect(self._content, LIGHT_GREY, (0, 0, self.size.x, y))
        self._content.blit(font.render(os.path.join(*os_path_split(self.directory)), 1, BLACK), (0, 0))

    def trigger_user(self, event):
        if event.type == KEYDOWN:
            if event.key in (K_BACKSPACE, K_LEFT):
                try:
                    self.hcursor -= 1
                    self.load_dir(self.history[self.hcursor], True)
                except IndexError:
                    pass
            if event.key == K_RIGHT:
                try:
                    if self.hcursor + 1 < 0:
                        self.hcursor += 1
                    else:
                        raise IndexError
                    self.load_dir(self.history[self.hcursor], True)
                except IndexError:
                    pass
        if event.type == MOUSEBUTTONDOWN:
            if event.button in (4, 5):
                for wid in self.widgets:
                    if isinstance(wid, widgets.ImageWithAlt):
                        if event.button == 4:
                            wid.move(0, -10)
                        else:
                            wid.move(0, +10)

    def update_user(self):
        pass
