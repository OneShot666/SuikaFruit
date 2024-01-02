from math import sqrt
# from random import *
# from time import *
from PIL import Image
from data import *
import pygame
import pymunk


# Fruits (x11) : cerise, fraise, raisin, clémentine, orange, pomme, pamplemousse, pêche, ananas, melon, pastèque
class Fruit(pygame.sprite.Sprite):
    def __init__(self, name, color, radius=10, weight=1, score=10, fruit_image=False, elasticity=0.4, friction=0.5):
        super().__init__()
        self.name = name
        self.radius = radius
        self.weight = weight
        self.score = score
        self.vel_x = 0
        self.vel_y = 0
        # physics
        self.body = pymunk.Body()
        self.shape = pymunk.shapes.Circle(self.body, self.radius)
        self.create_physics_body(None, elasticity, friction)
        # image
        self.color = color
        self.border_color = self.get_border_color()
        self.reflect_color = self.get_reflect_color()
        self.width = int(self.radius * 0.1)
        self.image = self.set_image(fruit_image)
        # self.rect = self.image.get_rect(center=(0, 0))
        self.pos_x, self.pos_y = self.body.position.x, self.body.position.y
        # data
        self.min_speed = 0.1                                                    # Stop below that speed
        self.max_speed = 10                                                     # Can't go faster
        self.gravity = gravity                                                  # Force that make object fall
        self.resistance = resistance                                            # Force that slow down objects speed
        self.drag_coeff = drag_coeff                                            # Force of drag on objects

    def __str__(self):
        return f"'{self.name}' {self.color} : {self.radius}px {self.weight}g {self.score}pts"

    def present(self):                                                          # Present self
        return f"{int(self.radius * 0.2)} cm  {self.weight} g  {self.score} pts"

    def get_border_color(self):                                                 # Calculate border color
        border = [0, 0, 0]
        if type(self.color) is tuple:
            for index, rgb in enumerate(self.color):
                border[index] = int(rgb * 1.3)
                border[index] = 255 if border[index] > 255 else border[index]
            return tuple(border)
        return self.color

    def get_reflect_color(self):                                                # Calculate reflect color
        reflect = [0, 0, 0]
        if type(self.color) is tuple:
            for index, rgb in enumerate(self.color):
                reflect[index] = int(rgb * 2)
                reflect[index] = 255 if reflect[index] > 255 else reflect[index]
            return tuple(reflect)
        return self.color

    def set_image(self, fruit_image):                                           # (re)set the image
        self.width = int(self.radius * 0.1)
        if fruit_image:
            # self.image = pygame.image.load(f"images/fruits/{self.name}.png")
            # self.image.set_colorkey((255, 255, 255))
            # self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            image = Image.open(f"images/fruits/{self.name}.png")                # For body in space
            self.image = image.resize((self.radius * 2, self.radius * 2))
            self.pos_x, self.pos_y = self.body.position.x, self.body.position.y
        else:
            self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
            pygame.draw.circle(self.image, self.border_color, (self.radius, self.radius), self.radius, self.width)
            reflect = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(reflect, "white", (self.radius * 0.4, self.radius * 0.4,
                                                   self.radius * 0.5, self.radius * 0.25))
            reflect = pygame.transform.rotate(reflect, 45)                      # Rotate reflect surface
            reflect.set_alpha(96)                                               # Make reflect half transparent
            self.image.blit(reflect, (-self.radius * 0.2, -self.radius * 0.7))  # Position reflect correctly
            self.pos_x = self.image.get_rect(center=(0, 0)).x
            self.pos_y = self.image.get_rect(center=(0, 0)).y
        # self.rect = self.image.get_rect(center=(0, 0))
        return self.image

    def create_physics_body(self, pos=None, elasticity=0.4, friction=0.5):      # Used when add to Basket
        self.body = pymunk.Body()
        self.body.position = pos if pos else (0, 0)
        # image = Image.open(f"images/fruits/{self.name}.png")
        # self.image = image.resize((self.radius * 2, self.radius * 2))
        self.shape = pymunk.shapes.Circle(self.body, self.radius)
        self.shape.mass = self.weight
        self.shape.elasticity = elasticity
        self.shape.friction = friction

    def draw(self, surface):                                                    # Draw fruit on screen
        if type(self.image) != pygame.surface.Surface:
            self.image = pygame.image.fromstring(self.image.tobytes(),
                                                 self.image.size, self.image.mode)  # PIL image from pygame image
        # surface.blit(self.image, (self.body.position.x, self.body.position.y))
        surface.blit(self.image, (self.pos_x, self.pos_y))

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
            self.vel_x *= 0.95                                                  # Slow down on ground (test)
            self.vel_x = self.max_speed if self.vel_x > self.max_speed else - self.max_speed \
                if self.vel_x < - self.max_speed else self.vel_x
        # Prevent infinite movement
        self.vel_x = 0 if - self.min_speed < self.vel_x < self.min_speed else self.vel_x
        self.vel_y = 0 if - self.min_speed < self.vel_y < self.min_speed else self.vel_y
        self.vel_x, self.vel_y = round(self.vel_x, 2), round(self.vel_y, 2)     # Round velocity
        # Apply velocity
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

    def collide_circle(self, circle, diff_value):                               # Check if self collide with circle
        distance = sqrt(pow((circle.pos_x + circle.radius) - (self.pos_x + self.radius), 2) +
                        pow((circle.pos_y + circle.radius) - (self.pos_y + self.radius), 2))
        ecart = self.radius + circle.radius + self.min_speed
        gap_coeff = 0.95 if diff_value == 0 else 1

        if distance <= ecart * gap_coeff:                                       # if circles collide
            # vector between circles
            circle_center = (circle.pos_x + circle.radius, circle.pos_y + circle.radius)
            self_center = (self.pos_x + self.radius, self.pos_y + self.radius)
            direction = pygame.math.Vector2(circle_center) - pygame.math.Vector2(self_center)
            try:
                direction.normalize_ip()                                        # if both centers at same place
            except ValueError:
                pass
            dist_max = min(circle.radius, self.radius)
            force = (ecart - distance) / dist_max * self.max_speed              # Function to get repulsion force
            force = self.max_speed if force > self.max_speed else - self.max_speed if force < - self.max_speed else force
            # Make fruit go to opposite direction
            vel_coeff = 1.25 if diff_value == 3 else 1.1 if diff_value == 2 else 1  # Increase vel with diff
            self.vel_x -= round(direction.x * force, 2) * vel_coeff
            vel_y = round(direction.y * force, 2) * vel_coeff                   # Test to vanilla velocity
            self.vel_y -= vel_y * lift if vel_y > 0 else vel_y                  # Increase repulsion force from above

            return True
        return False

    def collide_point(self, dot, percent=1):                                    # Check if dot touch circle
        distance = sqrt(pow((dot[0]) - (self.pos_x + self.radius * percent), 2) +
                        pow((dot[1]) - (self.pos_y + self.radius * percent), 2))
        return distance <= self.radius * percent
