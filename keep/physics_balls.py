import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60

# game variables
wall_thickness = 10
gravity = 0.5                                                                   # Gravity force
bounce_stop = 0.3                                                               # Min force to stop bouncing
Mouse_trajectory = []                                                           # mouse pos : get movement vector


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass=1, retention=0, friction=0, y_speed=0, x_speed=0, id_ball=0):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention                                              # Conservation of rebound force
        self.friction = friction                                                # Slowing down when rolling
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id_ball
        self.circle = ''
        self.selected = False

    def draw(self):                                                             # Draw ball on screen
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def check_gravity(self):                                                    # How world interact with ball
        if not self.selected:
            if self.y_pos < HEIGHT - self.radius - (wall_thickness / 2):        # Fall if not on ground
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:                                  # If can bounce : bounce with retention
                    self.y_speed *= self.retention * -1
                else:                                                           # Else : stop bouncing
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0

            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                    (self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):   # If L or R borders
                self.x_speed *= self.retention * -1
                if abs(self.x_speed) <= bounce_stop:                            # If too slow : stop bouncing
                    self.x_speed = 0

            if self.y_speed == 0 and self.x_speed != 0:                         # When rolling : slow down
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:                                                                   # Follow mouse (with vector)
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed

    def update_pos(self, mouse):                                                # Update position of ball
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

    def check_select(self, pos):                                                # Check if ball selected by mouse
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected


def draw_walls():                                                               # Draw white borders on screen
    left = pygame.draw.line(screen,     'white', (0, 0), (0, HEIGHT),           wall_thickness)
    right = pygame.draw.line(screen,    'white', (WIDTH, 0), (WIDTH, HEIGHT),   wall_thickness)
    top = pygame.draw.line(screen,      'white', (0, 0), (WIDTH, 0),            wall_thickness)
    bottom = pygame.draw.line(screen,   'white', (0, HEIGHT), (WIDTH, HEIGHT),  wall_thickness)
    return [left, right, top, bottom]


def calc_motion_vector():                                                       # Calculate speed and dir of mouse
    x_speed = 0
    y_speed = 0
    if len(Mouse_trajectory) > 10:
        x_speed = (Mouse_trajectory[-1][0] - Mouse_trajectory[0][0]) / len(Mouse_trajectory)
        y_speed = (Mouse_trajectory[-1][1] - Mouse_trajectory[0][1]) / len(Mouse_trajectory)
    return x_speed, y_speed


ball1 = Ball(50, 50, 30,  'blue',   100, .75, 0.02, 0, 0, 1)
ball2 = Ball(500, 50, 50, 'green',  300, .9, 0.03, 0, 0, 2)
ball3 = Ball(200, 50, 40, 'purple', 200, .8, 0.04, 0, 0, 3)
ball4 = Ball(700, 50, 60, 'red',    500, .7, .1, 0, 0, 4)
Balls = [ball4, ball2, ball3, ball1]

# main game loop
run = True
while run:
    screen.fill('black')

    mouse_pos = pygame.mouse.get_pos()
    Mouse_trajectory.append(mouse_pos)
    if len(Mouse_trajectory) > 20:                                              # Save last 20 mouse pos
        Mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    walls = draw_walls()
    for ball in Balls:
        ball.draw()
        ball.update_pos(Mouse_trajectory[-1])
        ball.y_speed = ball.check_gravity()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:                                # Check if click on one of the ball
            if event.button == 1:
                for ball in Balls:
                    ball.check_select(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:                                  # unselect all ball
            if event.button == 1:
                for ball in Balls:
                    ball.check_select((-1000, -1000))

    pygame.display.flip()
    timer.tick(fps)

pygame.quit()
