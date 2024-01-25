from math import sqrt, degrees
# from random import *
# from time import *
from PIL import Image, ImageDraw
from data import *
import webcolors
import pygame
import pymunk


# Fruits (x11) : cherry, strawberry, grape, clementine, orange, apple, pear, peach, pineapple, melon, watermelon
class Fruit(pygame.sprite.Sprite):
    def __init__(self, name, color, radius=10, weight=1, score=10, skin_image=None):
        super().__init__()
        self.name = name
        self.radius = radius
        self.weight = weight
        self.score = score
        self.size = (int(self.radius * 2), int(self.radius * 2))
        self.width = int(self.radius * 0.1)
        # physics
        self.body = pymunk.Body()
        self.shape = pymunk.shapes.Circle(self.body, self.radius)
        self.create_physics_body()
        self.pos_x = self.body.position.x - self.radius
        self.pos_y = self.body.position.y - self.radius
        self.vel_x = 0
        self.vel_y = 0
        # image
        self.color = color
        self.border_color = self.get_other_color(self.color)
        self.bg_color = (255, 255, 255, 128)                                    # For bg image
        self.reflect_alpha = 96                                                 # Transparency
        self.image = self.set_image(skin_image)                                 # Circle or modifiable image
        self.pygame_image = self.image if not skin_image else pygame.image.fromstring(
            self.image.tobytes(), self.image.size, self.image.mode)             # Displayable image
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

    def get_other_color(self, color, coeff=1.5):                                # Calculate border color
        if type(color) is str:
            color = self.get_color_value(color)
        if color:
            border = [0, 0, 0]
            for index, rgb in enumerate(color):
                border[index] = rgb + int((255 - rgb) * (coeff - 1) / coeff) \
                                if coeff > 1.0 else int(rgb * coeff)
                border[index] = 255 if border[index] > 255 else border[index]
                border[index] = 0 if border[index] < 0 else border[index]
            return tuple(border)
        return color

    @staticmethod
    def get_color_value(color_name: str):                                       # Get rgb from color name
        try: return webcolors.name_to_rgb(color_name)
        except ValueError: return None

    def set_image(self, skin_image=None, using_bg=False):                       # (re)set the image
        self.size = (int(self.radius * 2), int(self.radius * 2))
        if skin_image:                                                          # Set skin
            skin_image = skin_image.resize(self.size)
            if using_bg:                                                        # Add bg skin
                bg = Image.new('RGBA', self.size)
                draw = ImageDraw.Draw(bg)
                draw.ellipse((0, 0, self.size[0], self.size[1]), self.bg_color) # Draw transparent circle
                bg.paste(skin_image, (0, 0), skin_image)                        # Superimposed skin on circle
                skin_image = bg
            self.image = skin_image
            self.pygame_image = pygame.image.fromstring(self.image.tobytes(),
                                self.image.size, self.image.mode)
        else:                                                                   # Set circle
            self.width = int(self.radius * 0.1)
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
            pygame.draw.circle(self.image, self.border_color, (self.radius, self.radius), self.radius, self.width)
            reflect = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.ellipse(reflect, "white", (self.radius * 0.4, self.radius * 0.4,
                                                   self.radius * 0.5, self.radius * 0.25))
            reflect = pygame.transform.rotate(reflect, 45)                      # Rotate reflect surface
            reflect.set_alpha(self.reflect_alpha)                               # Make reflect half transparent
            self.image.blit(reflect, (-self.radius * 0.2, -self.radius * 0.7))  # Position reflect correctly

        return self.image

    def create_physics_body(self, pos=None, velocity=None, elasticity=None, friction=None):    # Used when add to Basket
        velocity = velocity if velocity else (0, 0)
        e = fruit_elasticity if elasticity is None else elasticity
        f = fruit_friction if friction is None else friction
        self.body = pymunk.Body()
        self.body.position = pos if pos else (0, 0)
        self.body.velocity = velocity
        self.shape = pymunk.shapes.Circle(self.body, self.radius)
        self.shape.mass = self.weight
        self.shape.elasticity = e
        self.shape.friction = f

    def draw(self, surface, change_rotation=False, display_arrow=False):        # Draw fruit on screen
        image = self.image
        if type(self.image) != pygame.surface.Surface:
            if change_rotation:
                orientation = int(- degrees(self.body.angle) % 360)
                image = self.image.rotate(orientation)
            image = image.resize(self.size)
            image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        self.pos_x, self.pos_y = self.body.position.x - self.radius, self.body.position.y - self.radius
        self.vel_x, self.vel_y = self.body.velocity
        surface.blit(image, (self.pos_x, self.pos_y))

        if display_arrow:                                                       # Use only for test
            center_coords = (self.pos_x + self.radius, self.pos_y + self.radius)
            dir_coords = (center_coords[0] + self.vel_x, center_coords[1] + self.vel_y)
            pygame.draw.line(surface, "yellow", center_coords, dir_coords, 3)

    # Not use with new physics
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
            """ Old physics
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
            """

            return True
        return False

    def collide_point(self, dot, percent=1):                                    # Check if dot touch self
        distance = sqrt(pow((dot[0]) - (self.pos_x + self.radius * percent), 2) +
                        pow((dot[1]) - (self.pos_y + self.radius * percent), 2))
        return distance <= self.radius * percent
