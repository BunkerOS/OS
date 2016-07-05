from .utils import *


class Window:
    def __init__(self, screen, titre="", version=1.0, pos=(0, 0), size=(0, 0), couleur=(20, 20, 20),
                 contour_couleur=BLACK, couleur_barre=GREY, movable=True, fullscreen=False,
                 cote_c=EPAISSEUR_BARRE // 2):
        self.screen = screen
        self.movable = movable
        self.fullscreen = fullscreen
        self.couleur_barre = couleur_barre
        self.wscreen, self.hscreen = self.screen.get_size()
        self.titre = titre
        self.version = version
        self.fen_name = "[" + self.titre + "]" + " " + str(self.version)
        self.pos = Point(*pos)
        self.size = Point(*size)
        self.couleur = couleur
        self.cote_c = cote_c
        self.state = WStates.ACTIVE
        self.escape_btn = (
            self.size.x - (EPAISSEUR_BARRE - self.cote_c) // 2 - self.cote_c,
            (EPAISSEUR_BARRE - self.cote_c) // 2,
            self.cote_c,
            self.cote_c
        )
        self._content = pygame.Surface(tuple(self.size))
        self.clic_on_barre = False

        self._contour = pygame.Surface((self.size.x + 4, self.size.y + 4 + EPAISSEUR_BARRE))
        pygame.draw.rect(self._contour, contour_couleur, (0, 0) + self._contour.get_size())

        self.id = None

        self._blurw = pygame.Surface(tuple(self.size))
        self._blurw.fill(WHITE)
        self._blurw.convert_alpha()
        self._blurw.set_alpha(225)

        self.widgets = []

    def update(self):
        pass

    def draw_vitals(self):
        # contour
        self.screen.blit(self._contour, (self.pos.x - 2, self.pos.y - 2))
        # barre
        pygame.draw.rect(self.screen, self.couleur_barre, tuple(self.pos) + (self.size.x, EPAISSEUR_BARRE))
        # titre
        self.screen.blit(font.render(self.fen_name, 1, BLACK), (self.pos.x + 2, self.pos.y + 2))
        # croix
        pygame.draw.rect(self.screen, RED, (self.escape_btn[0] + self.pos.x, self.escape_btn[1] + self.pos.y) + self.escape_btn[2:])

    def draw_content(self):
        # fond
        pygame.draw.rect(self._content, self.couleur, (0, 0) + tuple(self.size))

    def draw(self):
        if self.alive():
            if not self.fullscreen:
                self.draw_vitals()
            self.draw_content()
            for wid in self.widgets:
                wid.draw()
            if self.state == WStates.NOT_RESPONDING:
                self._content.blit(self._blurw, (0, 0))
            self.screen.blit(self._content, (self.pos.x, self.pos.y + EPAISSEUR_BARRE if not self.fullscreen else self.pos.y))

    def set_alive(self, value=WStates.ACTIVE):
        self.state = value

    def alive(self):
        return self.state != WStates.UNACTIVE

    def get_title(self):
        return self.fen_name

    def move(self, xd, yd):
        self.pos = Point(self.pos.x + xd, self.pos.y + yd)
        self.escape_btn = (
            self.size.x - (EPAISSEUR_BARRE - self.cote_c) // 2 - self.cote_c,
            (EPAISSEUR_BARRE - self.cote_c) // 2,
            self.cote_c,
            self.cote_c
        )

    def trigger_vitals(self, event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if 0 <= x <= self.size.x and 0 <= y <= EPAISSEUR_BARRE:
                self.clic_on_barre = True
        if event.type == MOUSEMOTION:
            if self.clic_on_barre:
                if self.movable:
                    x, y = event.rel
                    self.move(x, y)
        if event.type == MOUSEBUTTONUP:
            self.clic_on_barre = False
            x, y = event.pos
            if not self.fullscreen and self.escape_btn[0] <= x <= self.escape_btn[0] + self.escape_btn[2] \
                    and self.escape_btn[1] <= y <= self.escape_btn[1] + self.escape_btn[3]:
                self.state = WStates.UNACTIVE

    def trigger_user(self, event):
        pass

    def trigger(self, event):
        self.trigger_vitals(event)
        self.trigger_user(event)
        if event.type in (MOUSEBUTTONUP, MOUSEMOTION, MOUSEBUTTONDOWN):
            event.pos = (event.pos[0], event.pos[1] - EPAISSEUR_BARRE)
        for wid in self.widgets:
            wid.trigger(event)
