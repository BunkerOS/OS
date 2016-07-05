import time
import sys
import traceback
from .utils import *

method = None


def info(kind, value, tb):
    print("Démarrage du débogueur")
    output = traceback.format_exception(kind, value, tb)
    screen = pygame.display.get_surface()
    output2 = []
    print("Création de la liste d'erreurs (%i)" % len(output))
    for i, o in enumerate(output):
        if isinstance(o, str):
            output2 += o.split("\n")
    print("Création du contenu de la fenêtre")
    text = [font_petite.render(o, 1, BLACK) for o in output2 if o]
    logo = pygame.image.load("system/resx/logo.png").convert_alpha()
    x = 50
    y = logo.get_height() + 50

    print("Démarrage de l'instance graphique")
    while True:
        ev = pygame.event.poll()
        if ev.type == KEYDOWN:
            break

        pygame.draw.rect(screen, BLUE, (0, 0) + screen.get_size())
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 0))
        for i, o in enumerate(text):
            screen.blit(o, (x, y + i * 25))

        pygame.display.flip()
    print("Redémarrage du système")
    if method:
        sys.excepthook = info
        print("Attendez ...")
        method()
