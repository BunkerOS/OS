from .utils import *

_id = 0

class Widget:
    def __init__(self, screen, pos, size, bg_color, fg_color):
        self.screen = screen
        self.pos = Point(*pos)
        self.size = Point(*size)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self._content = pygame.Surface(tuple(self.size))
        global _id
        self.id = _id
        _id += 1

    def draw_vitals(self):
        pass

    def draw_content(self):
        pass

    def draw(self):
        self.draw_vitals()
        self.draw_content()
        self.screen.blit(self._content, tuple(self.pos))

    def update(self):
        pass

    def trigger_vitals(self, event):
        pass

    def trigger_user(self, event):
        pass

    def trigger(self, event):
        self.trigger_vitals(event)
        self.trigger_user(event)


class Button(Widget):
    def __init__(self, screen, pos=(0, 0), size=(0, 0), bg_color=BLACK, fg_color=WHITE, mouseover_color=GREY, text="", text_centered=False):
        super().__init__(
            screen,
            pos=pos,
            size=size,
            bg_color=bg_color,
            fg_color=fg_color
        )
        self.mouseover_color = mouseover_color
        self.text = [font.render(t, 1, self.fg_color) for t in text.split("\n")]
        self.text_centered = text_centered
        self.clicked = False
        self.mouseover = False
        self.func, fargs = None, []

    def register(self, func, *args):
        self.func = func
        self.fargs = args

    def update(self):
        if self.clicked and self.func:
            self.func(*self.fargs)
            self.called = False
            self.clicked = False

    def draw_vitals(self):
        if not self.mouseover:
            pygame.draw.rect(self._content, self.bg_color, tuple(self.pos) + tuple(self.size))
        else:
            pygame.draw.rect(self._content, self.mouseover_color, tuple(self.pos) + tuple(self.size))
        y = 5
        for i, t in enumerate(self.text):
            if not self.text_centered:
                self._content.blit(t, (5, y))
                y += t.get_height() + 5
            else:
                self._content.blit(t, (self.size.x // 2 - t.get_width() // 2, self.size.y // 2 + (i - len(self.text) // 2 - 1) * t.get_height() // 2))

    def trigger_vitals(self, event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.pos.x <= x <= self.pos.x + self.size.x and self.pos.y <= y <= self.pos.y + self.size.y:
                self.clicked = True
        if event.type in (MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP):
            xp, yp = event.pos
            if self.pos.x <= xp <= self.pos.x + self.size.x and self.pos.y <= yp <= self.pos.y + self.size.y:
                self.mouseover = True
            else:
                self.mouseover = False


class Label(Widget):
    def __init__(self, screen, pos=(0, 0), size=(0, 0), bg_color=BLACK, fg_color=WHITE, text="", text_centered=False):
        super().__init__(
            screen,
            pos=pos,
            size=size,
            bg_color=bg_color,
            fg_color=fg_color
        )
        self.text = [font.render(t, 1, self.fg_color) for t in text.split("\n")]
        self.text_centered = text_centered

    def draw_vitals(self):
        pygame.draw.rect(self._content, self.bg_color, tuple(self.pos) + tuple(self.size))
        y = 5
        for i, t in enumerate(self.text):
            if not self.text_centered:
                self._content.blit(t, (5, y))
                y += t.get_height() + 5
            else:
                self._content.blit(t, (self.size.x // 2 - t.get_width() // 2, self.size.y // 2 + (i - len(self.text) // 2) * t.get_height() // 2))


class CheckBox(Widget):
    def __init__(self, screen, pos=(0, 0), size=(0, 0), bg_color=BLACK, fg_color=WHITE, mouseover_color=GREY, text="", text_centered=False, checkbox_color=BLUE):
        super().__init__(
            screen,
            pos=pos,
            size=size,
            bg_color=bg_color,
            fg_color=fg_color
        )
        self.mouseover_color = mouseover_color
        self.text = [font.render(t, 1, self.fg_color) for t in text.split("\n")]
        self.text_centered = text_centered
        self.checkbox_color = checkbox_color
        self.checked = False
        self.mouseover = False

    def draw_vitals(self):
        if not self.mouseover:
            pygame.draw.rect(self._content, self.bg_color, tuple(self.pos) + tuple(self.size))
        else:
            pygame.draw.rect(self._content, self.mouseover_color, tuple(self.pos) + tuple(self.size))
        pygame.draw.rect(self._content, self.checkbox_color, (self.pos.x, self.pos.y, 10, 10), 2)
        if self.checked:
            pygame.draw.rect(self._content, self.checkbox_color, (self.pos.x + 3, self.pos.y + 3, 4, 4))
        y = 5
        for i, t in enumerate(self.text):
            if not self.text_centered:
                self._content.blit(t, (15, y))
                y += t.get_height() + 5
            else:
                self._content.blit(t, (15 + self.size.x // 2 - t.get_width() // 2, self.size.y // 2 + (i - len(self.text) // 2) * t.get_height() // 2))

    def trigger_vitals(self, event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.pos.x <= x <= self.pos.x + self.size.x and self.pos.y <= y <= self.pos.y + self.size.y:
                self.checked = not self.checked
        if event.type in (MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP):
            xp, yp = event.pos
            if self.pos.x <= xp <= self.pos.x + self.size.x and self.pos.y <= yp <= self.pos.y + self.size.y:
                self.mouseover = True
            else:
                self.mouseover = False


class ImageWithAlt(Widget):
    def __init__(self, screen, pos=(0, 0), size=(0, 0), bg_color=BLACK, fg_color=WHITE, image="", mouseover_color=GREY, text="", text_centered=False):
        super().__init__(
            screen,
            pos=pos,
            size=size,
            bg_color=bg_color,
            fg_color=fg_color
        )
        self.mouseover_color = mouseover_color
        self.text = [font.render(t, 1, self.fg_color) for t in text.split("\n")]
        self.text_centered = text_centered
        self.clicked = False
        self.mouseover = False
        self.image = pygame.image.load(image).convert_alpha()
        self.func, fargs = None, []

    def register(self, func, *args):
        self.func = func
        self.fargs = args

    def update(self):
        if self.clicked and self.func:
            self.func(*self.fargs)
            self.clicked = False

    def draw_vitals(self):
        if not self.mouseover:
            pygame.draw.rect(self._content, self.bg_color, tuple(self.pos) + tuple(self.size))
        else:
            pygame.draw.rect(self._content, self.mouseover_color, tuple(self.pos) + tuple(self.size))
        self._content.blit(self.image, (self._content.get_width() // 2 - self._content.get_width(), 0))
        y = 5 + self.image.get_height()
        for i, t in enumerate(self.text):
            if not self.text_centered:
                self._content.blit(t, (5, y))
                y += t.get_height() + 5
            else:
                self._content.blit(t, (self.size.x // 2 - t.get_width() // 2, self.size.y // 2 + (i - len(self.text) // 2) * t.get_height() // 2 + self.image.get_height()))

    def trigger_vitals(self, event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.pos.x <= x <= self.pos.x + self.size.x and self.pos.y <= y <= self.pos.y + self.size.y:
                self.clicked = True
        if event.type in (MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP):
            xp, yp = event.pos
            if self.pos.x <= xp <= self.pos.x + self.size.x and self.pos.y <= yp <= self.pos.y + self.size.y:
                self.mouseover = True
            else:
                self.mouseover = False
