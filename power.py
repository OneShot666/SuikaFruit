# from math import *
# from random import *
# from time import *
import pygame


# Powers (x4) : pop, sort, smaller, bigger
class Power(pygame.sprite.Sprite):
    def __init__(self, name="power", description="", cost=0, pos=None):
        super().__init__()
        pos = [0, 0, 0, 0] if pos is None else pos
        self.active = False                                                     # Not really used
        self.name = name
        self.description = description
        self.cost = cost                                                        # Based on score
        self.position = pos                                                     # In pixel

    def check_activate(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if (self.position[0] <= mouse[0] <= self.position[0] + self.position[2] and
                self.position[1] <= mouse[0] <= self.position[1] + self.position[3] and
                click and not self.active):
            self.active = True
        elif click and self.active:
            self.active = False
            # Spend cost on score in main programm
