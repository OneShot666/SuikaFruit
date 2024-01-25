# from math import *
# from random import *
# from time import *
from PIL import Image
# from data import *
import webcolors
import pygame


class Skin(pygame.sprite.Sprite):                                               # Manage skins
    def __init__(self, name="fruit", color=None, DictNames=None, level_unlock=0):
        super().__init__()
        self.name = name
        self.color = (255, 255, 255) if color is None else color
        self.bg_color = self.get_bg_color(self.color)
        self.DictNames = {"apple": f"apple"} if DictNames is None else DictNames
        self.level_unlock = level_unlock
        self.Images = []
        self.PygameImages = []
        self.set_Images()

    def __str__(self):
        return f"'{self.name}', unlock at level {self.level_unlock}"

    def get_bg_color(self, color, coeff=3.5):                                   # Calculate border color
        if type(color) is str:
            color = self.get_color_value(color)
        if color:
            border = [0, 0, 0]
            for index, rgb in enumerate(color):
                border[index] = rgb + int((255 - rgb) * (coeff - 1) / coeff) \
                                if coeff > 1.0 else int(rgb * coeff)
                border[index] = 255 if border[index] > 255 else border[index]   # Check values
                border[index] = 0 if border[index] < 0 else border[index]
            return tuple(border)
        return color

    @staticmethod
    def get_color_value(color_name: str):                                       # Get rgb from color name
        try: return webcolors.name_to_rgb(color_name)
        except ValueError: return None

    def set_Images(self):                                                       # Load all images in advance
        for fruit, skin in self.DictNames.items():
            image = Image.open(f"images/skins/{self.name}/{skin}.png")
            self.Images.append(image)
            image = pygame.image.load(f"images/skins/{self.name}/{skin}.png")
            self.PygameImages.append(image)
