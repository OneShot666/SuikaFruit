# from math import *
# from random import *
# from time import *
from fruit import Fruit
import pygame

pygame.init()

screen_size = (800, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Vecteurs de vitesse")
clock = pygame.time.Clock()

centre = Fruit('centre', 'purple', 100, 50)
centre.rect.x = screen_size[0] * 0.5 - centre.radius
centre.rect.y = screen_size[1] * 0.5 - centre.radius
souris = Fruit('souris', 'pink', 75, 30)
max_size_arrow = 200


def collide_map_border():
    if centre.rect.left <= 0:
        centre.rect.x += abs(centre.rect.left)
        centre.vel_x = 0
    elif centre.rect.right >= screen_size[0]:
        centre.rect.x -= centre.rect.right - screen_size[0]
        centre.vel_x = 0
    if centre.rect.top <= 0:
        centre.rect.y += abs(centre.rect.top)
        centre.vel_y = 0
    elif centre.rect.bottom >= screen_size[1]:
        centre.rect.y -= centre.rect.bottom - screen_size[1]
        centre.vel_y = 0


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                run = False

    # Draw background
    bg_color = "lightgreen" if centre.collide_circle(souris) else "cyan"
    screen.fill(bg_color)

    # Apply forces to center circle
    centre.update()
    collide_map_border()
    print(f"({centre.vel_x}, {centre.vel_y})")

    # Draw circles
    centre.draw(screen)
    mouse = pygame.mouse.get_pos()
    souris.rect.x = mouse[0] - souris.radius
    souris.rect.y = mouse[1] - souris.radius
    souris.draw(screen)

    # Draw line of velocity force
    middle = centre.rect.center
    pygame.draw.line(screen, "blue", middle, (middle[0] + centre.vel_x, middle[1] + centre.vel_y), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
