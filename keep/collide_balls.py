from math import sqrt
from random import randint
import pygame
import sys

pygame.init()
pausing = True
largeur_ecran, hauteur_ecran = 800, 600
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Cercles interagissants")
clock = pygame.time.Clock()


class Cercle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, vel_x, vel_y):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.collide_border()
        self.debugger()

    def collide_border(self):                                                   # Rebondir sur les bords de l'écran
        if self.rect.left < 0 or self.rect.right > largeur_ecran:
            self.vel_x *= -1
        if self.rect.top < 0 or self.rect.bottom > hauteur_ecran:
            self.vel_y *= -1

    def collide_circle(self, circle):
        if (sqrt(pow(circle.rect.x - self.rect.x, 2) + pow(circle.rect.y - self.rect.y, 2))
                < (self.radius + circle.radius)):
            if self.rect.x < circle.rect.x and self.vel_x > 0 or circle.rect.x < self.rect.x and self.vel_x < 0:
                self.vel_x *= -1
            if self.rect.y < circle.rect.y and self.vel_y > 0 or circle.rect.y < self.rect.y and self.vel_y < 0:
                self.vel_y *= -1

    def debugger(self):
        if self.rect.left < -1 and self.vel_x < 0 or self.rect.right > largeur_ecran + 1 and self.vel_x > 0:
            self.vel_x *= -1
            print(f"x : {self.color} ! ({self.vel_x})")
            return True
        if self.rect.top < -1 and self.vel_y < 0 or self.rect.bottom > hauteur_ecran + 1 and self.vel_y > 0:
            self.vel_y *= -1
            print(f"y : {self.color} ! ({self.vel_y})")
            return True

        return False


Colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "white"]
Cercles = pygame.sprite.Group()
size = 20

# Créer des sprites
for color in Colors:
    cercle = Cercle(randint(0, largeur_ecran - size), randint(0, hauteur_ecran - size), size, color, randint(-5, 5), randint(-5, 5))
    Cercles.add(cercle)

mouse = pygame.mouse.get_pos()
cercle = Cercle(mouse[0] - size, mouse[1] - size, size, "black", 0, 0)
Cercles.add(cercle)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                pausing = not pausing

    ecran.fill((200, 200, 255))

    mouse = pygame.mouse.get_pos()
    Cercles.sprites()[-1].rect.x = mouse[0] - size
    Cercles.sprites()[-1].rect.y = mouse[1] - size

    # Mise à jour des sprites
    if not pausing:
        Cercles.update()

    # Détection de collision
    for circle in Cercles.sprites():
        for other in Cercles.sprites():
            if circle != other:
                circle.collide_circle(other)

    # Dessiner les sprites
    Cercles.draw(ecran)

    pygame.display.flip()
    clock.tick(60)
