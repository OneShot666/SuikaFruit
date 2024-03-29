# from math import *
# from random import *
# from time import *
from PIL import Image, ImageEnhance
import pygame


# Powers (x5) : pop, sort, smaller, bigger, current
class Power(pygame.sprite.Sprite):
    def __init__(self, name="power", description="", cost=0, level_unlock=0, pos=None):
        super().__init__()
        pos = [0, 0, 0, 0] if pos is None else pos
        self.active = False                                                     # Not really used
        self.name = name
        self.description = description
        self.image = Image.open(f"images/icons/{name}.png")
        filtre = ImageEnhance.Color(self.image)
        self.lock_image = filtre.enhance(0)                                     # Grayscale image
        self.pygame_image = pygame.image.load(f"images/icons/{name}.png")       # Displayable image
        self.pygame_lock_image = pygame.image.fromstring(self.lock_image.tobytes(),
                                 self.lock_image.size, self.lock_image.mode)    # Displayable lock image
        self.cost = cost                                                        # Cost score
        self.level_unlock = level_unlock                                        # When power is unlocked
        self.pos = pos                                                          # In pixel (not used)

    def check_activate(self, condition=True):                                   # ! Not used (yet ?)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if (self.pos[0] <= mouse[0] <= self.pos[0] + self.pos[2] and
                self.pos[1] <= mouse[0] <= self.pos[1] + self.pos[3] and
                click and not self.active and condition):                       # Active power
            self.active = True
        elif click and self.active:                                             # Use power
            self.active = False
            # Spend cost on score in main programm
