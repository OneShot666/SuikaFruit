from math import *
from random import *
from time import *
from data import *
import pygame


class Player(pygame.sprite.Sprite):                                             # Manage player level
    def __init__(self):
        super().__init__()
        self.pseudo = "Player"
        self.image = pygame.image.load(f"images/icons/profile.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.xp = 0
        self.xp_max = 100
        self.level = 1
        self.has_level_up = False

    def level_up(self):                                                         # Level up player
        if self.xp >= self.xp_max:
            self.level += 1
            self.xp -= self.xp_max
            self.xp_max += 100
            self.has_level_up = True
        else:
            self.has_level_up = False
