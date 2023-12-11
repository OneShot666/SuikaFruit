from math import sqrt
# from random import *
# from time import *
from data import *
import pygame


# Fruits (x11) : cerise, fraise, raisin, clémentine, orange, pomme, pamplemousse, pêche, ananas, melon, pastèque
class Fruit(pygame.sprite.Sprite):
    def __init__(self, name, color, radius=10, weight=1, score=10):
        super().__init__()
        self.name = name
        self.color = color
        self.border_color = self.get_border_color()
        self.radius = radius
        self.width = int(self.radius * 0.1)
        self.weight = weight
        self.score = score
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, self.border_color, (self.radius, self.radius), self.radius, self.width)
        self.rect = self.image.get_rect(center=(0, 0))
        self.vel_x = 0
        self.vel_y = 0
        # data
        self.gravity = gravity                                                  # Force that make object fall
        self.min_speed = 0.1                                                    # Stop below that speed
        self.max_speed = 10                                                     # Can't go faster
        self.resistance = resistance                                            # Force that slow down objects speed
        self.drag_coeff = drag_coeff                                            # Force of drag on objects

    def __str__(self):
        return f"'{self.name}' {self.color} : {self.radius}px {self.weight}g {self.score}pts"

    def present(self):
        return f"{int(self.radius * 0.2)} cm  {self.weight} g  {self.score} pts"

    def get_border_color(self):
        border = [0, 0, 0]
        if type(self.color) == tuple:
            for index, rgb in enumerate(self.color):
                border[index] = int(rgb * 1.3)
                border[index] = 255 if border[index] > 255 else border[index]
            return tuple(border)
        return self.color

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):                                                           # Apply forces and update position
        # Apply force of gravity
        coeff = (- 10 / (self.weight + 5)) + 2 + self.resistance                # Math function based on fruit weights
        self.vel_y += round(self.gravity * 0.1 * coeff, 2)
        self.vel_y += self.resistance if self.vel_y < 0 else - self.resistance if self.vel_y > 0 else 0
        self.vel_y = self.max_speed if self.vel_y > self.max_speed else - self.max_speed \
            if self.vel_y < - self.max_speed else self.vel_y

        # Apply air resistance
        if self.vel_x != 0:
            # self.vel_x = round(1/2 * self.drag_coeff * self.resistance * pi * (self.radius / 100) ** 2 * self.vel_x, 2)
            self.vel_x *= 0.95                                                   # Test for slow down on ground
            self.vel_x = self.max_speed if self.vel_x > self.max_speed else - self.max_speed \
                if self.vel_x < - self.max_speed else self.vel_x

        # Prevent infinite movement
        self.vel_x = 0 if - self.min_speed < self.vel_x < self.min_speed else self.vel_x
        self.vel_y = 0 if - self.min_speed < self.vel_y < self.min_speed else self.vel_y
        self.vel_x, self.vel_y = round(self.vel_x, 2), round(self.vel_y, 2)     # Round velocity

        # Apply velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def collide_circle(self, circle):                                           # Check if self collide with circle
        distance = sqrt(pow((circle.rect.x + circle.radius) - (self.rect.x + self.radius), 2) +
                    pow((circle.rect.y + circle.radius) - (self.rect.y + self.radius), 2))
        ecart = self.radius + circle.radius + self.min_speed

        if distance <= ecart:                                                   # if circles collide
            # vector between circles
            direction = pygame.math.Vector2(circle.rect.center) - pygame.math.Vector2(self.rect.center)
            try: direction.normalize_ip()                                       # if both centers at same place
            except ValueError: pass
            dist_max = min(circle.radius, self.radius)
            force = (ecart - distance) / dist_max * self.max_speed              # Function to get repulsion force
            force = self.max_speed if force > self.max_speed else - self.max_speed if force < - self.max_speed else force
            # Make fruit go to opposite direction
            self.vel_x -= round(direction.x * force, 2)
            vel_y = round(direction.y * force, 2)                               # Test to vanilla velocity
            self.vel_y -= vel_y * lift if vel_y > 0 else vel_y                  # Increase repulsion force from above

            return True
        return False

    def collide_point(self, dot, percent=1):                                    # Check if dot touch circle
        distance = sqrt(pow((dot[0]) - (self.rect.x + self.radius * percent), 2) +
                        pow((dot[1]) - (self.rect.y + self.radius * percent), 2))
        return distance <= self.radius * percent
