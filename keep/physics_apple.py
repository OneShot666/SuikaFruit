from math import degrees
from random import choice
from PIL import Image
import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

width, height = 1000, 800
window = pygame.display.set_mode((width, height))

running = True
clock = pygame.time.Clock()
fps = 60

space = pymunk.Space()
space.gravity = (0, 981)

pymunk.pygame_util.positive_y_is_up = False
draw_options = pymunk.pygame_util.DrawOptions(window)

apple_radius = 30
apple_image = Image.open(f"../images/fruits/pomme.png")
apple_image = apple_image.resize((apple_radius * 2, apple_radius * 2))
police = pygame.font.Font(f"../fonts/Bubble Bobble.ttf", 25)

thick = 3
Rects = [(width * 0.375, height * 0.75, width * 0.25, thick),
         (width * 0.375, height * 0.25, thick, height * 0.5),
         (width * 0.625, height * 0.25, thick, height * 0.5)]
Borders = []
Box = []
Balls = []


def run():
    global running, apple_radius, Borders, Box

    Borders = create_boundaries()
    Box = create_main_box()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    break

                if event.key == pygame.K_UP:
                    change_apple_size(1)
                elif event.key == pygame.K_DOWN:
                    change_apple_size(-1)

                if event.key == pygame.K_t:
                    test = choice(Balls)
                    new_ball = create_ball(int(test[1].radius * 2), test[1].mass, test[0].position)
                    Balls.remove(test)
                    Balls.append(new_ball)

                if event.key == pygame.K_r:
                    reset_space()

            if event.type == pygame.MOUSEBUTTONDOWN:                            # Create ball
                mouse = pygame.mouse.get_pos()
                ball = create_ball(apple_radius, 10, mouse)
                Balls.append(ball)
                apple_radius = choice([i for i in range(5, 51, 5)])

        draw(window, Box, Rects, Balls)  # , space, draw_options)

        pygame.display.update()                                                 # Can specify area

        space.step(1 / fps)
        clock.tick(fps)

    pygame.quit()


def create_boundaries():                                                        # Out of screen
    rects = [
        [(width / 2, height + thick), (width, thick * 2)],
        [(width / 2, - thick), (width, thick * 2)],
        [(- thick, height / 2), (thick * 2, height)],
        [(width + thick, height / 2), (thick * 2, height)]
    ]
    Borders = []

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)
        Borders.append(body)
    return Borders


def create_main_box(elasticity=0.4, friction=0.5):
    Box = []

    for pos in Rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        end = (pos[0] if pos[2] == thick else pos[0] + pos[2],
               pos[1] if pos[3] == thick else pos[1] + pos[3])
        shape = pymunk.Segment(body, (pos[0], pos[1]), end, thick)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.color = (16, 255, 64, 0)
        space.add(body, shape)
        Box.append((body, shape))
    return Box


def create_ball(radius, mass, pos, elasticity=0.9, friction=0.4):
    body = pymunk.Body()
    body.position = pos
    image = Image.open(f"../images/fruits/pomme.png")
    body.image = image.resize((radius * 2, radius * 2))
    shape = pymunk.shapes.Circle(body, radius)
    shape.mass = mass
    shape.color = (0, 0, 255, 0)
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(body, shape)
    return body, shape


def draw(window, Box, rects, Balls, space=None, draw_options=None):
    window.fill("khaki")
    if space and draw_options:
        space.debug_draw(draw_options)                                          # Display shape in space
    for i, border in enumerate(Box):                                            # Display main box (hover Segments)
        pos = (rects[i][0] - thick, rects[i][1] - thick,
               rects[i][2] * 2 if rects[i][2] == thick else rects[i][2] + thick * 2,
               rects[i][3] * 2 if rects[i][3] == thick else rects[i][3] + thick * 2)
        pygame.draw.rect(window, "orange", pos, 0, thick)
    for ball in Balls:                                                          # Display balls (hover Circles)
        orientation = - int(degrees(ball[0].angle) % 360)
        if ball[0].angle != 0:
            print(f"{ball[0].angle} = {degrees(ball[0].angle)} ->  {orientation}")
        pil_image = ball[0].image.rotate(orientation)
        image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)  # PIL image from pygame image
        window.blit(image, (ball[0].position.x - ball[1].radius, ball[0].position.y - ball[1].radius))
    info = police.render(f"Taille : {apple_radius} px", True, "orange")
    window.blit(info, (int(width * 0.85), int(height * 0.05)))


def change_apple_size(change=0):
    global apple_radius, apple_image

    if change != 0:
        apple_radius += 5 * change
        apple_radius = 5 if apple_radius < 5 else abs(apple_radius)
        apple_image = pygame.image.load(f"../images/fruits/pomme.png")
        apple_image = pygame.transform.scale(apple_image, (apple_radius * 2, apple_radius * 2))


def reset_space():
    global space, Borders, Box, Balls

    window.fill("black")
    pygame.display.flip()
    space = pymunk.Space()
    space.gravity = (0, 981)
    Borders = create_boundaries()
    Box = create_main_box(space, Rects)
    Balls = []


if __name__ == "__main__":
    run()
