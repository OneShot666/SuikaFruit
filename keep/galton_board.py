from random import randrange
from pymunk import pygame_util
import pymunk
import pygame

# Source : https://www.youtube.com/watch?v=-q_Vje2a6eY

# Settings data
pygame_util.positive_y_is_up = False                                            # Reverse Y axe (to be same as pygame)
screen_size = width, height = 1500, 800
fps = 60

# Pygame data
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Pymunk data
draw_options = pygame_util.DrawOptions(screen)
space = pymunk.Space()                                                          # Where all physics is apply
space.gravity = 0, 5000                                                         # Apply gravity on Y axe
segment_thickness = 6
ball_mass, ball_radius = 1, 7
nb_ball = 1000

# Funnel data
a, b, c, d = 10, 100, 18, 40
x1, x2, x3, x4 = a, width // 2 - c, width // 2 + c, width - a
y1, y2, y3, y4, y5 = b, height // 4 - d, height // 4, height // 2 - 1.5 * b, height - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (0, height), (width, height)


# Create balls (dynamic)
def create_ball(space):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)               # Moment of inertia : turning force
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = randrange(x1, x4), randrange(- y1, y1)
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.1                                                       # Coeff of force losing
    ball_shape.friction = 0.1
    space.add(ball_body, ball_shape)
    return ball_body


# Balls data
Balls = [([randrange(256) for _ in range(3)], create_ball(space)) for _ in range(nb_ball)]


# Create walls for balls (static)
def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pygame.color.THECOLORS[color]
    space.add(segment_shape)


# Create pegs (static circles use as obstacles)
def create_peg(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
    circle_shape.color = pygame.color.THECOLORS[color]
    circle_shape.elasticity = 0.1
    circle_shape.friction = 0.5
    space.add(circle_shape)


# Pegs data
peg_y, step = y4, 60
for i in range(10):
    peg_x = - 1.5 * step if i % 2 else - step
    for j in range(width // step + 2):
        create_peg(peg_x, peg_y, space, 'darkslateblue')
        if i == 9:
            create_segment((peg_x, peg_y + 50), (peg_x, height), segment_thickness, space, 'darkslategray')
        peg_x += step
    peg_y += 0.5 * step

"""
# Box data
box_mass, box_size = 1, (60, 40)
for x in range(120, width - 60, box_size[0]):
    for y in range(height // 2, height - 20, box_size[1]):
        box_moment = pymunk.moment_for_box(box_mass, box_size)
        box_body = pymunk.Body(box_mass, box_moment)
        box_body.position = x, y
        box_shape = pymunk.Poly.create_box(box_body, box_size)
        box_shape.elasticity = 0.1
        box_shape.friction = 1
        box_shape.color = [randrange(256) for _ in range(4)]
        space.add(box_body, box_shape)
"""

# Platforms data
platforms = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
for platform in platforms:
    create_segment(*platform, segment_thickness, space, 'darkolivegreen')
create_segment(B1, B2, 20, space, 'darkslategray')

# Main loop
while True:
    screen.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                create_ball(space)

    space.debug_draw(draw_options)                                              # Display space

    [pygame.draw.circle(screen, color, ball.position, ball_radius) for color, ball in Balls]

    space.step(1 / fps)                                                         # Step to apply physics
    pygame.display.flip()
    clock.tick(fps)
