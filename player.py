# from math import *
# from random import *
# from time import *
# from data import *
from PIL import Image
import pygame


class Player(pygame.sprite.Sprite):                                             # Manage player level
    def __init__(self):
        super().__init__()
        self.pseudo_is_valid = False
        self.proto_is_valid = False
        self.pseudo = "Player"
        self.size = (100, 100)
        self.avatar = pygame.image.load(f"images/icons/profile.png").convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, self.size)
        self.proto = Image.open("images/icons/profile.png")                     # Proto avatar
        self.skin = None                                                        # For proto
        self.face = None                                                        # For proto
        self.xp = 0
        self.xp_max = 100
        self.level = 1
        self.has_level_up = False

    def __str__(self):
        return f"'{self.pseudo}', lvl {self.level} : {self.xp} / {self.xp_max} xp"

    def set_proto(self):                                                        # When skin (and face) are set
        if self.skin:
            mixed = self.skin.resize(self.proto.size)
            if self.face:
                face_size = int(self.proto.size[0] * 0.6)
                face = self.face.resize((face_size, face_size))
                gap = int((self.proto.size[0] - face_size) / 2)
                mixed.paste(face, (gap, gap), face)
            self.proto = mixed

    def valid_proto(self):                                                      # Create new avatar
        self.avatar = self.proto
        if type(self.avatar) != pygame.surface.Surface:
            self.avatar = self.avatar.resize(self.size)
            self.avatar = pygame.image.fromstring(self.avatar.tobytes(), self.avatar.size, self.avatar.mode)
        else:
            self.avatar = pygame.transform.scale(self.avatar, self.size)
        self.proto_is_valid = True

    def level_up(self):                                                         # Level up player
        if self.xp >= self.xp_max:
            self.level += 1
            self.xp -= self.xp_max
            self.xp_max += 100
            self.has_level_up = True
        else:
            self.has_level_up = False
