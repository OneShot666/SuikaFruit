from math import sqrt
from random import choice
from time import time
from datetime import datetime
from os import getcwd, listdir
from fruit import Fruit
from power import Power
from data import *
import pymunk.pygame_util
import pymunk
import pygame
import sys

""" Documentation
creator : One Shot
name : Suika Fruit
date of creation : November 26th 2023
version : 0.2.3
language : python
purpose : Small game where you can merge fruit to get score. The bigger the fruit, the higher the score.
          Any resemblance to an existing game would be coincidental.
          All arguments are optional.
arguments : (3)
    - difficulty_index : Default value = 1. Informs about the difficulty level of the game.
    - random_music : Default value = True. By default, choose one random music. If False, choose real game music.
    - fruit_image : Default value = False. By default, fruits are circles. If False, fruits are images.
requirements : libraries 'pygame', 'pymunk', 'math', 'random', 'time' and 'sys'.
"""

# ! Finish choose current fruit screen
# ! Adding new physics with pymunk...
#   - fix display lose screen randomly when dropping fruit for some reason...
#   - make fruits roll (rotate image based on space_fruits orientation)
#   - balance size and weight of fruits
#   - balance elasticity and friction of borders and fruits


# [check] : Make window display + caption + icon
# [check] : Display random fruit on screen
# [check] : Forbid fruit from going out window + add gravitation
# [check] : Make collision between fruits + repulsion force
# [check] : Make same fruit fusion and create next fruit
# [check] : Add box and collisions with it + bg
# [check] : Add score and next fruit + current fruit
# [check] : Add player choose where to put fruit + make next fruit coherent
# [check] : Upgrade fruit physics + collisions + add timers (dropping next fruit + merging fruit)
# [check] : Add menu + buttons (start game, restart, go to menu, options, exit)
# [check] : Make buttons work + add project on GitHub
# [check] : Add save scores for scoreboard + screen Fruitopedia
# [check] : Add borders and reflect on fruits and buttons
# [check] : Add condition for losing game + make lose screen
# [check] : Adding more dynamic functions (display_default_box, fruits' size)
# [check] : Add music + lector + volume + mute
# [check] : Add parameters + balance difficulties
# [check] : Add skin for fruits (not used) + bg
# [check] : Add documentations + clean code + add comms
# [check] : Make all parameters work + add can change skin + make gradient bar fluid
# [check] : Can click on buttons + minors changing
# [check] : Add powers (cost score) : pop fruit / sort basket / make fruit smaller and heavier
# [v0.2.4] : Upgrade physics (make fruit more static) + balance score + make score when fruit merge
# [v0.2.5] : Change lost screen if high score beaten and update high score
# [v0.2.6] : On menu, make random fruits roll on the background
# [v0.2.7] : Add level with xp (based on score) + add icon account + player class
# [v0.2.8] : Add rewards for player (get free power if beat high score, unlock skin, powers...)
class Game:                                                                     # Manage all game
    def __init__(self, difficulty_index=1, random_music=True, fruit_image=False):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        # Main data
        self.creator = "One Shot"
        self.version = "v0.2.3"
        self.game_name = "Suika Fruit"
        self.date = datetime(2023, 12, 5)
        self.today = datetime.today()
        # Boolean data
        self.running = True                                                     # A little important
        self.loading = False                                                    # ! [later] For loading screen
        self.pausing = False
        self.helping = False                                                    # For help line
        self.playing = True                                                     # For loading music
        self.shopping = False                                                   # For showing powers
        self.powering = False                                                   # When using power
        self.choosing = False                                                   # Power 5 (choose current)
        self.on_menu = True                                                     # A little important
        self.on_game = False
        self.on_lose = False
        self.on_help = False                                                    # For help note
        self.on_para = False                                                    # For parameters
        self.on_back = False                                                    # Ask for back menu (security)
        self.on_resG = False                                                    # Ask restart game (security)
        self.on_allF = False                                                    # For Fruitopedia
        self.is_mute = False
        # Game data
        self.path = getcwd()                                                    # Get actual position of files
        self.pressed = pygame.key.get_pressed()                                 # Pressed keys
        self.horloge = pygame.time.Clock()                                      # Manage the fps
        self.fps = 60
        # Physics data
        self.Space = None                                                       # Where law of physics applies
        self.space_options = None                                               # Normally not used
        self.space_step = float(1 / self.fps)                                   # Fps of space
        self.SpaceMapBorders = []
        self.SpaceBoxBorders = []
        self.SpacePanier = []
        # Screen data
        self.is_fullscreen = True                                               # A parameter
        self.Fullscreen = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen_width, self.screen_height = self.Fullscreen
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))  # Display window in full screen
        pygame.display.set_caption(self.game_name)                              # Window name
        self.bg_color = "khaki"
        self.bg_image = pygame.Surface((self.screen_width, self.screen_height))
        self.bg_image.fill(self.bg_color)                                       # Create bg image
        pygame.draw.rect(self.bg_image, "sienna", (0, self.screen_height * 0.75,
                                                   self.screen_width * 1.01, self.screen_height * 0.05))
        pygame.draw.rect(self.bg_image, "peru", (0, self.screen_height * 0.8,
                                                 self.screen_width * 1.01, self.screen_height * 0.21))
        # Fruit data
        self.FruitsName = ["cerise", "fraise", "raisin", "clementine", "orange", "pomme",
                           "poire", "peche", "ananas", "melon", "pasteque"]
        self.Fruits = []                                                        # All possible fruits
        self.FruitsChoosable = []                                               # Fruits that can be dropped
        self.Panier = pygame.sprite.Group()                                     # Fruits in bucket during game
        self.fruit_image = fruit_image
        # Screens, some colors and tips data
        self.ask_screen_percent = [0.35, 0.35, 0.3, 0.3]
        self.lose_screen_percent = [0.3, 0.1, 0.4, 0.8]                         # Also used for help screen
        self.all_fruits_screen_percent = [0.1, 0.25, 0.8, 0.5]
        self.choose_screen_percent = [0.25, 0.25, 0.5, 0.5]
        self.screens_color = (250, 250, 200)
        self.button_color = (230, 255, 140)
        self.border_color = (255, 160, 70)
        self.border_ratio = 0.02
        self.Tips = ["Try not to separate large fruits from each other",
                     "You can see the fruit evolution at the bottom left of the screen",
                     "Try to sort fruits by size so they can merge more easily",
                     "If the next fruit is the same as your current fruit, \n"
                     "you can merge them to have the next bigger fruit",
                     "Try to get used to the physics of the game",
                     "If a fruit protrudes from the top of the bag, you lose !",
                     "The heaviest fruits are the lightest"]
        self.tip = None
        # Parameters data
        self.parameters_screen_percent = [0.1, 0.1, 0.8, 0.8]
        self.ParametersPercent = [(0.15, 0.35, 0.11, 0.05), (0.15, 0.4, 0.28, 0.05), (0.15, 0.45, 0.28, 0.05),
                                  (0.15, 0.65, 0.14, 0.05), (0.15, 0.7, 0.14, 0.05), (0.15, 0.75, 0.14, 0.05),
                                  (0.33, 0.65, 0.16, 0.05), (0.33, 0.7, 0.16, 0.05), (0.33, 0.75, 0.16, 0.05),
                                  (0.55, 0.35, 0.33, 0.06), (0.55, 0.45, 0.16, 0.05), (0.55, 0.65, 0.14, 0.05),
                                  (0.55, 0.7, 0.31, 0.05)]        # For parameters
        self.select_param_color = self.border_color                             # ! Change later ?
        self.select_param_index = 0
        self.gamma = 0.5                                                        # Percent gamma (parameter)
        self.restart_game = False                                               # # A parameter
        self.collect_cookies = True                                             # The cookie is a lie
        # Brightness data
        self.brightness = 0.5                                                   # Percent brightness (parameter)
        self.brightness_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.brightness_glass.fill(tuple(int(c * self.brightness) for c in (255, 255, 255)))
        self.brightness_glass.set_alpha(64)
        # Difficulty data
        self.shopping_screen_percent = [0.55, 0.1, 0.35, 0.2]
        self.power_screen_size = [0.1, 0.1]
        self.Difficulties = ["Easy", "Medium", "Hard", "Impossible"]
        self.diff_index = difficulty_index                                      # Level of difficulty
        # Main box data (for fruits)
        self.main_box_percent = [0.33, 0.15, 0.34, 0.8]
        self.box_pos = (self.screen_width * self.main_box_percent[0],
                        self.screen_height * self.main_box_percent[1],
                        self.screen_width * self.main_box_percent[2],
                        self.screen_height * self.main_box_percent[3])
        self.main_box_width = 10                                                # px
        self.main_box_color = (255, 200, 90)
        # Score data
        self.save_score = True                                                  # A parameter
        self.show_scoreboard = True                                             # A parameter
        self.score = 0
        self.highscore = 0
        self.Scoreboard = []
        self.score_box_percent = [0.08, 0.25, 0.15, 0.15]
        self.score_box_color = (255, 200, 90)
        # Evolution of fruit box data
        self.evolution_box_percent = [0.06, 0.53, 0.19, 0.32]
        self.evolution_box_color = (255, 250, 140)
        # Current and next fruit data
        self.show_next_fruit = True                                             # A parameter
        self.current_fruit = None
        self.next_fruit_box_percent = [0.8, 0.21, 0.1, 0.18]
        self.next_fruit_box_color = (255, 250, 140)
        self.next_fruit = None
        # Commands and helping player data
        self.commands_box_percent = [0.775, 0.55, 0.15, 0.3]
        self.commands_box_color = (240, 210, 115)
        self.help_line_color = (255, 255, 220, 160)
        self.help_line_width = 5
        # Powers data (! Make a class ?)
        self.Powers = []
        self.power_index = None
        # Timers data
        self.current_time = time()
        self.click_last_timer = time()                                          # To click on button
        self.click_timer_duration = 0.5
        self.merging_fruit_last_timer = time()                                  # For merging fruit
        self.merging_fruit_timer_duration = 0.1
        self.next_fruit_last_timer = time()                                     # For dropping fruit
        self.next_fruit_timer_duration = 0.25
        # Pause screen data
        self.paused_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.rect(self.paused_glass, (255, 255, 255), self.paused_glass.get_rect())
        self.paused_glass.set_alpha(120)
        # Icon data
        self.icon = pygame.image.load("images/icons/icon.jpg")
        self.icon.set_colorkey((255, 255, 255))                                 # Remove white background
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                      # Game icon
        # Font data
        self.Fonts = [_ for _ in listdir(f"{self.path}/fonts") if _.endswith(".ttf")]  # Get fonts
        self.font_name = choice(self.Fonts)                                     # Choose random font
        self.title_font = pygame.font.Font(f"fonts/{self.font_name}", 100)
        self.small_title_font = pygame.font.Font(f"fonts/{self.font_name}", 50)
        self.button_font = pygame.font.Font(f"fonts/{self.font_name}", 30)
        self.main_font = pygame.font.Font(f"fonts/{self.font_name}", 20)
        self.present_font = pygame.font.Font(f"fonts/{self.font_name}", 16)
        self.commands_font = pygame.font.Font(f"fonts/{self.font_name}", 12)
        self.font_color = (255, 130, 20)
        # Sounds data
        self.Musics = [_ for _ in listdir(f"{self.path}/musics") if _.endswith(".mp3")]
        self.music = f"musics/{choice(self.Musics)}" if random_music else f"musics/main_music.mp3"
        self.repeat = -1                                                        # Endless by default
        self.volume = 0.5
        self.gap = 0.01
        # Main function
        self.run()

    def create_physics_space(self):                                             # Create / reset physics
        self.Space = pymunk.Space()
        self.Space.gravity = (0, int(gravity * 100))

        pymunk.pygame_util.positive_y_is_up = False                             # Make coords as pygame (reverse)
        self.space_options = pymunk.pygame_util.DrawOptions(self.window)        # Not used

        self.SpaceMapBorders = []
        self.SpaceBoxBorders = []
        if self.on_game:
            self.create_space_boundaries()
        self.create_main_box()
        self.SpacePanier = []

    def create_space_boundaries(self):
        thick = int(self.screen_height * self.border_ratio)
        Positions = [
            [(self.screen_width / 2, self.screen_height + thick), (self.screen_width, thick * 2)],
            [(self.screen_width / 2, - thick), (self.screen_width, thick * 2)],
            [(- thick, self.screen_height / 2), (thick * 2, self.screen_height)],
            [(self.screen_width + thick, self.screen_height / 2), (thick * 2, self.screen_height)]
        ]

        for pos, size in Positions:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.2
            shape.friction = 0.5
            self.Space.add(body, shape)
            self.SpaceMapBorders.append(body)

    def create_main_box(self):
        thick = self.main_box_width
        half = int(thick * 0.5)

        if self.on_menu:
            Positions = [(0, self.screen_height * 0.75, self.screen_width * 1.2, 0),
                         (- self.screen_width * 0.5, self.screen_height * 0.65,
                          self.screen_width * 0.5, self.screen_height * 0.1 + thick)]

            for pos in Positions:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                end = (pos[0] + pos[2], pos[1] + pos[3])
                shape = pymunk.Segment(body, (pos[0], pos[1]), end, half)
                shape.elasticity = 0.4
                shape.friction = 0.5
                self.Space.add(body, shape)
                self.SpaceBoxBorders.append((body, shape))
        elif self.on_game:
            Positions = [(self.box_pos[0] + half, self.box_pos[1] + self.box_pos[3] - half, self.box_pos[2] - thick, 0),
                         (self.box_pos[0] + half, self.box_pos[1] - half, 0, self.box_pos[3]),
                         (self.box_pos[0] + self.box_pos[2] - half, self.box_pos[1] - half, 0, self.box_pos[3])]

            for pos in Positions:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                end = (pos[0] + pos[2], pos[1] + pos[3])
                shape = pymunk.Segment(body, (pos[0], pos[1]), end, half)
                shape.elasticity = 0.4
                shape.friction = 0.5
                self.Space.add(body, shape)
                self.SpaceBoxBorders.append((body, shape))

    def create_fruits(self):                                                    # Load fruits
        percent = 55 if self.diff_index == 0 else 50 if self.diff_index == 1 else \
                  45 if self.diff_index == 2 else 40
        size = int(self.screen_width * self.main_box_percent[2] / percent)      # Get fruit size (dynamic)
        cerise =    Fruit(self.FruitsName[0],  (240, 0, 0),     size * 1, 11, 1, self.fruit_image)
        fraise =    Fruit(self.FruitsName[1],  (255, 140, 160), size * 2, 10, 2, self.fruit_image)
        raisin =    Fruit(self.FruitsName[2],  (195, 75, 255),  size * 3,  9, 4, self.fruit_image)
        clement =   Fruit(self.FruitsName[3],  (255, 210, 40),  size * 4,  8, 8, self.fruit_image)
        orange =    Fruit(self.FruitsName[4],  (255, 145, 45),  size * 5,  7, 16, self.fruit_image)
        pomme =     Fruit(self.FruitsName[5],  (250, 20, 20),   size * 6,  6, 32, self.fruit_image)
        poire =     Fruit(self.FruitsName[6],  (255, 240, 105), size * 7,  5, 64, self.fruit_image)
        peche =     Fruit(self.FruitsName[7],  (255, 190, 235), size * 8,  4, 128, self.fruit_image)
        ananas =    Fruit(self.FruitsName[8],  (255, 250, 30),  size * 9,  3, 256, self.fruit_image)
        melon =     Fruit(self.FruitsName[9],  (160, 250, 70),  size * 10, 2, 512, self.fruit_image)
        pasteque =  Fruit(self.FruitsName[10], (60, 210, 25),   size * 11, 1, 1024, self.fruit_image)
        self.Fruits = [cerise, fraise, raisin, clement, orange, pomme, poire, peche, ananas, melon, pasteque]
        nb = 4 if self.diff_index == 3 else 5
        self.FruitsChoosable = self.Fruits[:nb]                                 # Can drop 4 or 5 firsts fruits

        self.Panier.empty()
        self.current_fruit = choice(self.FruitsChoosable)
        self.next_fruit = choice(self.FruitsChoosable)
        self.score = 0

    def create_powers(self):
        pop = Power("pop", "Pop a fruit by clicking on it.", 1000)
        sort = Power("sort", "Sort all fruits in basket.", 2000)
        smaller = Power("smaller", "Make a fruit twice smaller", 250)
        bigger = Power("bigger", "Make a fruit twice bigger.", 250)
        current = Power("current fruit", "Choose current fruit.", 500)
        self.Powers = [pop, sort, smaller, bigger, current]

    def run(self):                                                              # Main fonction of game
        self.loading = True
        self.create_physics_space()
        self.create_fruits()
        self.create_powers()
        self.Load_score()
        self.loading = False

        while self.running:                                                     # Main loop of game
            if self.on_game:
                if not self.pausing:
                    self.Update_Manager()
                    self.Collision_Manager()
                    self.Check_Lose()

            self.Inputs_Manager()

            self.Display_Manager()

            self.Music_Manager()

            pygame.display.update()                                             # Can specify area
            # pygame.display.flip()
            self.horloge.tick(self.fps)
            if not self.pausing:
                self.Space.step(self.space_step)

    def Update_Manager(self):
        self.Panier.update()                                                    # Update all fruits

    def Collision_Manager(self):                                                # Manage collisions
        for fruit in self.Panier.sprites():
            for other in self.Panier.sprites():                                 # Provide fruits to collide each other
                # If fruit merge
                if fruit != other and fruit.collide_circle(other, self.diff_index) and fruit.name == other.name:
                    if self.current_time - self.merging_fruit_last_timer >= self.merging_fruit_timer_duration:
                        pos = int(self.FruitsName.index(fruit.name) + 1)
                        self.score += fruit.score                               # Add fruit score
                        if pos > len(self.Fruits) - 1:                          # If bigger fruit merge
                            self.Panier.remove(fruit)
                            self.Panier.remove(other)
                        else:                                                   # Normally merging same fruit
                            coords = [(fruit.pos_x + other.pos_x) / 2, (fruit.pos_y + other.pos_y) / 2]
                            vel = [(fruit.vel_x + other.vel_x) / 2, (fruit.vel_y + other.vel_y) / 2]
                            self.Panier.remove(fruit)
                            self.Panier.remove(other)

                            next_f = self.Fruits[pos]                           # Make spawn bigger fruit
                            bigger = Fruit(next_f.name, next_f.color, next_f.radius,
                                           next_f.weight, next_f.score, self.fruit_image)
                            bigger.pos_x, bigger.pos_y = coords
                            bigger.vel_x, bigger.vel_y = vel
                            self.Panier.add(bigger)
                        self.merging_fruit_last_timer = time()

            # Prevent fruits to exit box
            if fruit.pos_x <= self.box_pos[0] + self.main_box_width:
                fruit.pos_x = self.box_pos[0] + self.main_box_width
                fruit.vel_x *= -1 * bounce                                      # Make bounce against box borders
            elif fruit.pos_x + fruit.radius * 2 >= self.box_pos[0] + self.box_pos[2] - self.main_box_width:
                fruit.pos_x = self.box_pos[0] + self.box_pos[2] - self.main_box_width - fruit.radius * 2
                fruit.vel_x *= -1 * bounce                                      # //
            if fruit.pos_y + fruit.radius * 2 >= self.box_pos[1] + self.box_pos[3] - self.main_box_width:
                fruit.pos_y = self.box_pos[1] + self.box_pos[3] - self.main_box_width - fruit.radius * 2
                fruit.vel_y = 0

            # Prevents fruits to exit box (possible ?)
            if fruit.pos_x <= 0:
                fruit.pos_x = 0
                fruit.vel_x *= -1 * bounce                                      # Make bounce against screen borders
            elif fruit.pos_x + fruit.radius >= self.screen_width:
                fruit.pos_x = self.screen_width
                fruit.vel_x *= -1 * bounce                                      # //
            if fruit.pos_y < 0:                                                 # If fruit exit window, player lose
                self.on_lose = True
            if fruit.pos_y + fruit.radius * 2 >= self.screen_height:
                fruit.pos_y = self.screen_height - fruit.radius * 2
                fruit.vel_y = 0

    def Check_Lose(self):                                                       # Check if fruit out main box
        for fruit in self.Panier.sprites():
            if fruit.pos_y + fruit.radius < self.box_pos[1] and fruit.vel_y < 0:   # If lose, save score
                self.on_lose = True
                self.Scoreboard.append(self.score)
                self.Scoreboard.sort()
                self.Scoreboard.reverse()
                if self.score > self.highscore:
                    self.highscore = self.score
                break
        if self.score < 0:                                                      # If score error
            self.start_new_game()

    def Inputs_Manager(self):                                                   # Manage all inputs
        mouse = pygame.mouse.get_pos()
        self.current_time = time()
        self.pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Close_Game()

            if self.on_menu:                                                    # If on menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.on_para:       # Start new game
                        self.start_new_game()

                    if not self.on_para and event.key == pygame.K_h:            # For help note
                        self.on_help = not self.on_help

            elif self.on_game:                                                  # If on game
                if self.on_lose:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and not self.on_para:   # Go to menu
                            self.go_to_menu()

                        if event.key == pygame.K_SPACE:                         # Restart a game
                            self.start_new_game()
                elif self.on_back:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:                             # Go back to menu
                            self.go_to_menu()
                        elif event.key == pygame.K_n:                           # Continue game
                            self.on_back = False
                elif self.on_resG:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:                             # Restart new game
                            self.start_new_game()
                        elif event.key == pygame.K_n:                           # Continue game
                            self.on_resG = False
                else:
                    width = self.main_box_width * 5
                    on_main_box = (self.box_pos[0] - width <= mouse[0] <=
                                   self.box_pos[0] + self.box_pos[2] + width
                                   and self.box_pos[1] - width <= mouse[1] <=
                                   self.box_pos[1] + self.box_pos[3] + width)
                    if (not self.pausing and not self.on_allF and on_main_box
                        and not self.shopping and event.type == pygame.MOUSEBUTTONDOWN):
                        if self.powering:                                       # If using power
                            self.use_power()
                        else:
                            self.drop_fruit()                                   # Drop current fruit

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP1:                           # Use powers
                            self.activate_power(value=0)
                        elif event.key == pygame.K_KP2:
                            self.activate_power(value=1)
                        elif event.key == pygame.K_KP3:
                            self.activate_power(value=2)
                        elif event.key == pygame.K_KP4:
                            self.activate_power(value=3)
                        elif event.key == pygame.K_KP5:
                            self.activate_power(value=4)

                        if event.key == pygame.K_SPACE:                         # For pause
                            self.pausing = not self.pausing

                        if event.key == pygame.K_h and not self.pausing:        # For help line
                            self.helping = not self.helping

                        if event.key == pygame.K_f and not self.pausing:        # For fruitopedia
                            self.on_allF = not self.on_allF

                        if event.key == pygame.K_r and self.pausing:            # Restart game
                            if len(self.Panier.sprites()) > 0:                  # If game started, ask first
                                self.on_resG = True
                                self.pausing = False
                            else:
                                self.start_new_game()

                        if event.key == pygame.K_RETURN and not self.on_para:  # Want to quit game
                            if len(self.Panier.sprites()) > 0:                  # If game started, ask first
                                self.on_back = True
                                self.pausing = False
                            else:
                                self.go_to_menu()                               # Exit current game

            if event.type == pygame.KEYDOWN:                                    # Work anytime
                if event.key == pygame.K_m:                                     # (un)mute music
                    self.is_mute = not self.is_mute

                if not self.on_help and event.key == pygame.K_p:                # For parameters
                    self.on_para = not self.on_para

                if self.on_para:
                    if event.key == pygame.K_TAB:                               # Change selected param
                        self.select_param_index += -1 if self.pressed[pygame.K_LSHIFT] else 1
                        if self.select_param_index >= len(self.ParametersPercent):
                            self.select_param_index = 0
                        elif self.select_param_index < 0:
                            self.select_param_index = len(self.ParametersPercent) - 1

                    if event.key == pygame.K_RETURN:
                        self.Modify_checkbox_parameter()

                    if self.select_param_index == 9:                            # Difficulties
                        if event.key == pygame.K_LEFT:
                            if len(self.Panier.sprites()) > 0:                  # If game started, ask first
                                self.on_resG = True
                            else:
                                self.Modify_gradient_parameter(-1)
                        elif event.key == pygame.K_RIGHT:
                            if len(self.Panier.sprites()) > 0:                  # If game started, ask first
                                self.on_resG = True
                            else:
                                self.Modify_gradient_parameter(1)

                    if event.key == pygame.K_s:                                 # Save params (do it anyway)
                        self.on_para = False

        if self.on_para and self.select_param_index != 9:                       # Exception : difficulties
            if self.pressed[pygame.K_LEFT]:
                self.Modify_gradient_parameter(-1)
            elif self.pressed[pygame.K_RIGHT]:
                self.Modify_gradient_parameter(1)

        if self.pressed[pygame.K_UP]:                                           # Change volume music
            self.volume += self.gap
        elif self.pressed[pygame.K_DOWN]:
            self.volume -= self.gap

        if self.pressed[pygame.K_q] or self.pressed[pygame.K_ESCAPE]:           # Quit programm
            self.Close_Game()

    def Modify_checkbox_parameter(self):
        if self.select_param_index == 0:                                        # Fullscreen
            self.is_fullscreen = not self.is_fullscreen
            self.change_screen_size()
        elif self.select_param_index == 3:
            self.save_score = not self.save_score
        elif self.select_param_index == 4:
            self.restart_game = not self.restart_game
        elif self.select_param_index == 5:
            self.collect_cookies = True
        elif self.select_param_index == 6:
            self.show_scoreboard = not self.show_scoreboard
        elif self.select_param_index == 7:
            self.show_next_fruit = not self.show_next_fruit
        elif self.select_param_index == 8:                                      # Help line
            self.helping = not self.helping
        elif self.select_param_index == 10:                                     # Fruit or image
            self.fruit_image = not self.fruit_image
            self.create_fruits()
        elif self.select_param_index == 11:                                     # Endless music
            self.repeat = 0 if self.repeat == -1 else -1

    def change_screen_size(self):
        percent = 1 if self.is_fullscreen else 0.66
        self.screen_width = int(self.Fullscreen[0] * percent)
        self.screen_height = int(self.Fullscreen[1] * percent)
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.create_fruits()

    def Modify_gradient_parameter(self, direction=0):
        if self.select_param_index == 1:                                        # Brightness
            self.brightness += self.gap * direction
            self.brightness = 0 if self.brightness < 0 else 1 if self.brightness > 1 else self.brightness
        elif self.select_param_index == 2:                                      # Gamma
            self.gamma += self.gap * direction
            self.gamma = 0 if self.gamma < 0 else 1 if self.gamma > 1 else self.gamma
            self.set_gamma()
        elif self.select_param_index == 9:                                      # Difficulties
            self.diff_index += direction
            self.diff_index = 0 if self.diff_index >= len(self.Difficulties) else \
                              len(self.Difficulties) - 1 if self.diff_index < 0 else self.diff_index
            self.create_fruits()
        elif self.select_param_index == 12:                                     # Volume
            self.volume += self.gap * direction
            self.volume = 0 if self.volume < 0 else 1 if self.volume > 1 else self.volume

    def set_gamma(self):                                                        # Useless...
        # pixel = Sequence[int(255 * self.gamma)]
        # pygame.display.set_gamma_ramp(pixel, pixel, pixel)
        print(f"Gamma : {int(self.gamma * 100)}%")

    def use_power(self):                                                        # Use current power
        if self.powering and self.score >= self.Powers[self.power_index].cost:  # If using power and enough score
            if self.power_index == 4:                                           # Choose current fruit
                self.choosing = True
                self.powering = False
            elif self.power_index != 1:
                mouse = pygame.mouse.get_pos()
                for fruit in self.Panier.sprites():
                    if fruit.collide_point(mouse):
                        if self.power_index == 0:                               # Pop fruit
                            self.Panier.remove(fruit)
                        elif self.power_index == 2:                             # Make fruit smaller
                            new_radius = round(sqrt(2 * pow(fruit.radius, 2)), 2)
                            fruit.radius = new_radius
                            fruit.image = fruit.set_image(self.fruit_image)
                        elif self.power_index == 3:                             # Make fruit bigger
                            new_radius = round(sqrt(2 * pow(fruit.radius, 2)), 2)
                            fruit.radius = new_radius
                            fruit.image = fruit.set_image(self.fruit_image)
                        self.powering = False
            else:                                                               # Sort basket
                self.sort_basket()
                self.powering = False
            if not self.powering:                                               # If used power
                self.score -= self.Powers[self.power_index].cost
                self.Powers[self.power_index].active = False
                self.power_index = None

    def sort_basket(self):                                                      # Sort all fruits in basket
        pos = [self.screen_width * self.main_box_percent[0], self.screen_height * self.main_box_percent[1],
               self.screen_width * self.main_box_percent[2], self.screen_height * self.main_box_percent[3]]
        while self.check_fruit_in_double():
            for fruit in self.Panier.sprites():
                for other in self.Panier.sprites():
                    if fruit != other and fruit.name == other.name:             # If two same fruits
                        index = self.FruitsName.index(fruit.name)
                        self.score += fruit.score                               # Add score
                        if index == len(self.Fruits) - 1:
                            self.Panier.remove(fruit)
                            self.Panier.remove(other)
                        else:
                            next_fruit = self.Fruits[index + 1]
                            new_fruit = Fruit(next_fruit.name, next_fruit.color, next_fruit.radius,
                                              next_fruit.weight, next_fruit.score, self.fruit_image)
                            new_fruit.pos_x = pos[0] + pos[2] * 0.5 - new_fruit.radius
                            new_fruit.pos_y = pos[1] + pos[3] * 0.5 - new_fruit.radius
                            self.Panier.add(new_fruit)
                            self.Panier.remove(fruit)
                            self.Panier.remove(other)
                        break

    def check_fruit_in_double(self):
        double = False
        Names = []
        for fruit in self.Panier.sprites():
            if fruit.name in Names:
                double = True
                break
            Names.append(fruit.name)
        return double

    def drop_fruit(self):                                                       # Drop current fruit
        if self.current_time - self.next_fruit_last_timer >= self.next_fruit_timer_duration:
            fruit = Fruit(self.current_fruit.name, self.current_fruit.color, self.current_fruit.radius,
                          self.current_fruit.weight, self.current_fruit.score, self.fruit_image)
            fruit.pos_x = self.current_fruit.pos_x                              # Place fruit
            fruit.pos_y = self.current_fruit.pos_y
            fruit.create_physics_body((fruit.pos_x + fruit.radius, fruit.pos_y + fruit.radius))
            self.Space.add(fruit.body, fruit.shape)
            self.Panier.add(fruit)
            self.current_fruit = self.next_fruit                                # Replace current fruit
            self.next_fruit = choice(self.FruitsChoosable)                      # Change next fruit
            self.next_fruit_last_timer = time()

    def activate_power(self, value=None, key=None, name=None):                  # Have several ways to activate power
        if name:
            for power in self.Powers:
                if power.name == name:
                    self.power_index = self.Powers.index(power)
                    self.powering = True
                    break
        elif key:
            if key == pygame.K_KP1:
                self.powering = True
                self.power_index = 0
            elif key == pygame.K_KP2:
                self.powering = True
                self.power_index = 1
            elif key == pygame.K_KP3:
                self.powering = True
                self.power_index = 2
            elif key == pygame.K_KP4:
                self.powering = True
                self.power_index = 3
        else:
            if self.power_index != value:
                self.powering = True
                self.power_index = value
            else:
                self.powering = False
                self.power_index = None

    def Display_Manager(self):                                                  # Manage all things to draw
        if self.on_menu:
            self.Display_Menu()
        elif self.on_game:
            self.Display_Game()
        self.Space.debug_draw(self.space_options)                           # !! Move then make it comment
        self.Display_Volume()
        self.Display_brightness_glass()                                         # Manage luminosity

    def Display_Menu(self):                                                     # Display main menu
        # self.window.fill(self.bg_color)
        self.window.blit(self.bg_image, (0, 0))

        self.display_title()

        # Display main buttons
        condition = not self.on_help and not self.on_para                       # If not open
        if self.display_button("Play", (int(self.screen_width * 0.425), int(self.screen_height * 0.4),
                int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "RETURN", condition):
            self.start_new_game()
        if self.display_button("Help", (int(self.screen_width * 0.425), int(self.screen_height * 0.51),
                 int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "H", condition):
            self.on_help = not self.on_help
        if self.display_button("Parameters", (int(self.screen_width * 0.425), int(self.screen_height * 0.62),
               int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "P", condition):
            self.on_para = not self.on_para
        if self.display_button("Quit", (int(self.screen_width * 0.425), int(self.screen_height * 0.73),
             int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "Q", condition):
            self.Close_Game()

        # Display creator name and version
        name_text = self.button_font.render(f"{self.creator}", True, self.bg_color)
        text_size = name_text.get_size()
        self.window.blit(name_text, (int(self.screen_width * 0.05 - text_size[0] * 0.5),
                                     int(self.screen_height * 0.95 - text_size[1] * 0.5)))
        name_text = self.button_font.render(f"{self.version}", True, self.bg_color)
        text_size = name_text.get_size()
        self.window.blit(name_text, (int(self.screen_width * 0.95 - text_size[0] * 0.5),
                                     int(self.screen_height * 0.95 - text_size[1] * 0.5)))

        if self.on_help:
            self.Display_Help()
        if self.on_para:
            self.Display_Parameters()

        # pygame.mouse.set_cursor(pygame.cursors.diamond)                       # ! Change cursor

    def display_title(self):                                                    # Display game name (menu)
        title = self.title_font.render(f"{self.game_name}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(self.screen_width * 0.5 - title_size[0] * 0.5),
                                 int(self.screen_height * 0.2 - title_size[1] * 0.5)))

    def display_button(self, name, pos, command="", condition=True):            # Display all button in programm
        # Display button background
        pygame.draw.rect(self.window, self.button_color, pos, 0, pos[3])
        width = int(min(pos[2], pos[3]) * self.border_ratio * 3)
        pygame.draw.rect(self.window, self.border_color, pos, width, pos[3])
        # Display button name
        name_text = self.button_font.render(f"{name}", True, self.font_color)
        text_size = name_text.get_size()
        self.window.blit(name_text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                     int(pos[1] + pos[3] * 0.5 - text_size[1] * 0.5)))
        # Display command to activate (optional)
        if command != "":
            command_text = self.commands_font.render(f"[{command}]", True, self.font_color)
            command_size = command_text.get_size()
            self.window.blit(command_text, (int(pos[0] + pos[2] * 0.5 - command_size[0] * 0.5),
                                            int(pos[1] + pos[3] * 0.8 - command_size[1] * 0.5)))

        # Check if click on button
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        on_butt = pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3]
        on_time = True
        if self.current_time - self.click_last_timer < self.click_timer_duration:   # Waiting
            on_time = False
        else:                                                                   # If timer end
            if click and on_butt and condition:                                 # If click on button
                self.click_last_timer = time()
                on_time = True
        return on_butt and click and on_time and condition

    def Display_Help(self):                                                     # Display help note
        # Display help background
        pos = self.display_default_box(self.lose_screen_percent)
        # Display help title
        title = self.small_title_font.render(f"Rules", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display help text
        text = self.button_font.render(f"Goal", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.25 - text_size[1] * 0.5)))
        to_write = (f"Get the highest score by merging identical fruits.\nThere is 11 fruits in all.\n"
                    f"If one of them protrudes a little too far from the basket, you lose.\n"
                    f"But what will happened if you merge two biggest fruit together ?")
        text = self.main_font.render(to_write, True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.37 - text_size[1] * 0.5)))
        text = self.button_font.render(f"How to play ?", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.55 - text_size[1] * 0.5)))
        to_write = (f"Move the mouse to choose where to drop the current fruit.\n"
                    f"Click left to drop it in the basket.\n"
                    f"Look closely how they evolve with the evolution box (left bottom).")
        text = self.main_font.render(to_write, True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.67 - text_size[1] * 0.5)))
        # Display buttons
        if self.display_button("Menu", (int(pos[0] + pos[2] * 0.4), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "H"):
            self.on_help = not self.on_help

    def Display_Parameters(self):                                               # Display parameters screen
        # Display parameters background
        pos = self.display_default_box(self.parameters_screen_percent)
        # Display parameters title
        Percent = self.ParametersPercent
        title = self.small_title_font.render(f"Parameters", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display commands
        commands = self.main_font.render(f"Next parameter - Tab", True, self.font_color)
        commands.set_alpha(128)
        self.window.blit(commands, (int(pos[0] + pos[2] * 0.72), int(pos[1] + pos[3] * 0.05)))
        commands = self.main_font.render(f"Previous parameter - Maj + Tab", True, self.font_color)
        commands.set_alpha(128)
        self.window.blit(commands, (int(pos[0] + pos[2] * 0.72), int(pos[1] + pos[3] * 0.08)))
        commands = self.main_font.render(f"Modify checkbox - RETURN", True, self.font_color)
        commands.set_alpha(128)
        self.window.blit(commands, (int(pos[0] + pos[2] * 0.72), int(pos[1] + pos[3] * 0.11)))
        commands = self.main_font.render(f"Modify gradient - LEFT / RIGHT ARROW", True, self.font_color)
        commands.set_alpha(128)
        self.window.blit(commands, (int(pos[0] + pos[2] * 0.72), int(pos[1] + pos[3] * 0.14)))
        # Display parameters text
        screen = self.button_font.render(f"Screen : ", True, self.font_color)
        self.window.blit(screen, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.25)))
        screen_1 = self.main_font.render(f"Fullscreen", True, self.font_color)
        self.window.blit(screen_1, (int(pos[0] + pos[2] * Percent[0][0]), int(pos[1] + pos[3] * Percent[0][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.23), int(pos[1] + pos[3] * 0.35)), self.is_fullscreen)
        screen_2 = self.main_font.render(f"Luminosité", True, self.font_color)
        self.window.blit(screen_2, (int(pos[0] + pos[2] * Percent[1][0]), int(pos[1] + pos[3] * Percent[1][1])))
        self.display_gradient_bar((pos[0] + pos[2] * 0.23, pos[1] + pos[3] * 0.42), percent=self.brightness)
        screen_3 = self.main_font.render(f"Gamma", True, self.font_color)
        self.window.blit(screen_3, (int(pos[0] + pos[2] * Percent[2][0]), int(pos[1] + pos[3] * Percent[2][1])))
        self.display_gradient_bar((pos[0] + pos[2] * 0.23, pos[1] + pos[3] * 0.47), percent=self.gamma)

        sound = self.button_font.render(f"Gameplay : ", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.55)))
        sound = self.main_font.render(f"Save score", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * Percent[3][0]), int(pos[1] + pos[3] * Percent[3][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.26), int(pos[1] + pos[3] * 0.65)), self.save_score)
        sound = self.main_font.render(f"Restart game", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * Percent[4][0]), int(pos[1] + pos[3] * Percent[4][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.26), int(pos[1] + pos[3] * 0.7)), self.restart_game)
        sound = self.main_font.render(f"Collect cookies", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * Percent[5][0]), int(pos[1] + pos[3] * Percent[5][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.26), int(pos[1] + pos[3] * 0.75)), self.collect_cookies)
        sound = self.main_font.render(f"Show scoreboard", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * Percent[6][0]), int(pos[1] + pos[3] * Percent[6][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.46), int(pos[1] + pos[3] * 0.65)), self.show_scoreboard)
        sound = self.main_font.render(f"Show next fruit", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * Percent[7][0]), int(pos[1] + pos[3] * Percent[7][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.46), int(pos[1] + pos[3] * 0.7)), self.show_next_fruit)
        sound = self.main_font.render(f"Show help line", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * Percent[8][0]), int(pos[1] + pos[3] * Percent[8][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.46), int(pos[1] + pos[3] * 0.75)), self.helping)  # Checkbox

        diff = self.button_font.render(f"Difficulty : ", True, self.font_color)
        self.window.blit(diff, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.25)))
        for i, diff in enumerate(self.Difficulties):
            diff_text = self.main_font.render(f"{diff}", True, self.font_color)
            diff_coords = (int(pos[0] + pos[2] * (Percent[9][0] + i * 0.08)), int(pos[1] + pos[3] * Percent[9][1]))
            self.window.blit(diff_text, diff_coords)
            if self.diff_index == i:
                diff_size = diff_text.get_size()
                select_pos = (int(diff_coords[0] - diff_size[0] * 0.15), int(diff_coords[1] - diff_size[1] * 0.1),
                              int(diff_size[0] * 1.3), int(diff_size[1] * 1.3))
                pygame.draw.rect(self.window, self.font_color, select_pos, 3, 5)
        skin = "image" if self.fruit_image else "circle"
        music = self.main_font.render(f"Fruit skin ({skin})", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * Percent[10][0]), int(pos[1] + pos[3] * Percent[10][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.68), int(pos[1] + pos[3] * 0.45)), self.fruit_image)

        music = self.button_font.render(f"Musics & Sounds : ", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.55)))
        music = self.main_font.render(f"Endless music", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * Percent[11][0]), int(pos[1] + pos[3] * Percent[11][1])))
        endless = True if self.repeat == -1 else False
        self.display_checkbox((int(pos[0] + pos[2] * 0.66), int(pos[1] + pos[3] * 0.65)), endless)
        music = self.main_font.render(f"Volume", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * Percent[12][0]), int(pos[1] + pos[3] * Percent[12][1])))
        self.display_gradient_bar((pos[0] + pos[2] * 0.66, pos[1] + pos[3] * 0.72),
                                  gradient=11, percent=self.volume)
        # Display selected parameter [en cours]
        current = self.ParametersPercent[self.select_param_index]
        gap = 5 if self.select_param_index != 9 else 10
        pos_param = (pos[0] + pos[2] * current[0] - gap, pos[1] + pos[3] * current[1] - gap,
                     pos[2] * current[2] + gap, pos[3] * current[3] + gap)
        pygame.draw.rect(self.window, self.select_param_color, pos_param, 2, int(pos[3] * current[3] * 0.2))
        # Display buttons
        if self.display_button("Save", (int(pos[0] + pos[2] * 0.2), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "S"):
            self.on_para = not self.on_para
        if self.display_button("Close", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "P"):
            self.on_para = not self.on_para

    def display_checkbox(self, coords, is_check=False, size=None):              # For parameters
        size = int(self.screen_width * 0.02) if size is None else size
        pos = (coords[0], coords[1], size, size)
        width = int(size * 0.1)
        pygame.draw.rect(self.window, self.font_color, pos, width)
        if is_check:                                                            # Display cross
            pygame.draw.line(self.window, self.font_color, (pos[0] + width, pos[1] + width),
                                                           (pos[0] + pos[2] - width, pos[1] + pos[3] - width), width)
            pygame.draw.line(self.window, self.font_color, (pos[0] + width, pos[1] + pos[3] - width),
                                                           (pos[0] + pos[2] - width, pos[1] + width), width)

    def display_gradient_bar(self, coords, lenght=0, gradient=5, percent=0.5):  # For parameters
        lenght = int(self.screen_width * 0.15) if lenght == 0 else lenght
        width = int(self.screen_height * 0.003)
        pygame.draw.line(self.window, self.font_color, coords, (coords[0] + lenght, coords[1]), width)
        height = self.screen_height * 0.01
        for i in range(gradient):                                               # Display gradient
            size = i / (gradient - 1) * lenght
            pygame.draw.line(self.window, self.font_color, (int(coords[0] + size), int(coords[1] - height * 0.5)),
                             (int(coords[0] + size), int(coords[1] + height * 0.5)), width)
        points = [(int(coords[0] + lenght * percent), int(coords[1] - height * 1.2)),
                  (int(coords[0] + lenght * percent + height * 1.2), int(coords[1])),
                  (int(coords[0] + lenght * percent), int(coords[1] + height * 1.2)),
                  (int(coords[0] + lenght * percent - height * 1.2), int(coords[1]))]
        pygame.draw.polygon(self.window, self.font_color, points, width)

    def Display_Game(self):                                                     # Display game
        # self.window.fill(self.bg_color)
        self.window.blit(self.bg_image, (0, 0))

        self.display_small_title()

        self.display_main_box()                                                 # Main box for fruits
        self.display_evolution()
        self.display_next_fruit()
        self.display_commands()

        mouse = pygame.mouse.get_pos()
        if not self.pausing:                                                    # Draw current fruit (on mouse position)
            self.current_fruit.pos_x = mouse[0] - self.current_fruit.radius
            min_b = self.screen_width * self.main_box_percent[0] + self.main_box_width
            max_b = (min_b + self.screen_width * self.main_box_percent[2] -
                     (self.main_box_width + self.current_fruit.radius) * 2)
            self.current_fruit.pos_x = min_b if self.current_fruit.pos_x < min_b else max_b \
                if self.current_fruit.pos_x > max_b else self.current_fruit.pos_x
        self.current_fruit.pos_y = self.screen_height * 0.1 - self.current_fruit.radius
        self.current_fruit.draw(self.window)

        if self.helping:                                                        # Help line draw beyond fruits
            self.display_help_line()

        # self.Panier.draw(self.window)                                           # Display all fruits
        for fruit in self.Panier:
            fruit.pos_x, fruit.pos_y = fruit.body.position.x - fruit.radius, fruit.body.position.y - fruit.radius
            fruit.draw(self.window)

        # Placed here for scoreboard to be in front of help line
        self.display_highscore()

        self.Display_Icons()

        if self.shopping:                                                        # Display Shopping
            self.Display_Shopping()

        if self.powering:
            name = self.Powers[self.power_index].name.capitalize()
            text = self.button_font.render(f"Left click to activate power '{name}'.", True, self.font_color)
            text_size = text.get_size()
            self.window.blit(text, (int(self.screen_width * 0.5 - text_size[0] * 0.5),
                                    int(self.screen_height * 0.5 - text_size[1] * 0.5)))

        if self.choosing:
            self.Display_Choose_Fruit()

        if self.on_allF:
            self.Display_Fruitopedia()

        if self.on_lose:
            if self.restart_game:                                               # Check if auto restart game
                self.start_new_game()
            else:
                self.Display_Lose()

        if self.pausing:                                                        # Pause screen on foreground
            self.Display_pause_screen()

        if self.on_para:                                                        # Parameters
            self.Display_Parameters()

        if self.on_back:                                                        # Ask to go back to menu
            self.ask_back_menu()

        if self.on_resG:                                                        # Ask restart game
            self.ask_restart_game()

    def display_small_title(self):                                              # Display small game name
        title = self.small_title_font.render(f"{self.game_name}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(self.screen_width * 0.5 - title_size[0] * 0.5),
                                 int(self.screen_height * 0.1 - title_size[1] * 0.5)))

    def display_main_box(self):                                                 # Display main box for fruits
        self.box_pos = (self.screen_width * self.main_box_percent[0], self.screen_height * self.main_box_percent[1],
                        self.screen_width * self.main_box_percent[2], self.screen_height * self.main_box_percent[3])
        pygame.draw.rect(self.window, self.next_fruit_box_color, self.box_pos, 0, self.main_box_width * 2)
        pygame.draw.rect(self.window, self.main_box_color, self.box_pos, self.main_box_width, self.main_box_width * 2)

    def display_evolution(self):                                                # Display evolution of fruits
        # Display evolution background
        pos = self.display_default_box(self.evolution_box_percent, self.evolution_box_color)
        # Display text
        evolution = self.main_font.render(f"Evolution : ", True, self.font_color)
        evolution_size = evolution.get_size()
        self.window.blit(evolution, (int(pos[0] + pos[2] * 0.5 - evolution_size[0] * 0.5),
                                     int(pos[1] + pos[3] * 0.1 - evolution_size[1] * 0.5)))
        # Display fruits around invisible circle
        percent = 0.33
        percent *= 1.1 if self.diff_index == 0 else 1 if self.diff_index == 1 else \
                   0.9 if self.diff_index == 2 else 0.8                         # Offset fruit size (based on diff)
        # pygame.draw.circle(self.window, "black", (pos[0] + pos[2] * 0.5, pos[1] + pos[3] * 0.55), 90, 2)
        self.draw_reduced_fruit(self.Fruits[0], (pos[0] + pos[2] * 0.49, pos[1] + pos[3] * 0.216), percent)
        self.draw_reduced_fruit(self.Fruits[1], (pos[0] + pos[2] * 0.54, pos[1] + pos[3] * 0.21), percent)
        self.draw_reduced_fruit(self.Fruits[2], (pos[0] + pos[2] * 0.6, pos[1] + pos[3] * 0.22), percent)
        self.draw_reduced_fruit(self.Fruits[3], (pos[0] + pos[2] * 0.675, pos[1] + pos[3] * 0.275), percent)
        self.draw_reduced_fruit(self.Fruits[4], (pos[0] + pos[2] * 0.73, pos[1] + pos[3] * 0.38), percent)
        self.draw_reduced_fruit(self.Fruits[5], (pos[0] + pos[2] * 0.72, pos[1] + pos[3] * 0.53), percent)
        self.draw_reduced_fruit(self.Fruits[6], (pos[0] + pos[2] * 0.63, pos[1] + pos[3] * 0.69), percent)
        self.draw_reduced_fruit(self.Fruits[7], (pos[0] + pos[2] * 0.44, pos[1] + pos[3] * 0.76), percent)
        self.draw_reduced_fruit(self.Fruits[8], (pos[0] + pos[2] * 0.21, pos[1] + pos[3] * 0.68), percent)
        self.draw_reduced_fruit(self.Fruits[9], (pos[0] + pos[2] * 0.09, pos[1] + pos[3] * 0.43), percent)
        self.draw_reduced_fruit(self.Fruits[10], (pos[0] + pos[2] * 0.21, pos[1] + pos[3] * 0.17), percent)

    def draw_reduced_fruit(self, fruit, pos, percent=1 / 3):                    # Use to draw one reduced fruit
        radius = int(fruit.radius * percent * 2)
        copy = fruit.image
        if self.fruit_image and type(copy) != pygame.surface.Surface:
            copy = fruit.image.resize((radius, radius))
            copy = pygame.image.fromstring(copy.tobytes(), copy.size, copy.mode)  # PIL image from pygame image
        else:
            copy = pygame.transform.scale(copy, (radius, radius))
        self.window.blit(copy, pos)

    def display_next_fruit(self):                                               # Display next fruit box
        # Display next fruit background
        pos = self.display_default_box(self.next_fruit_box_percent, self.next_fruit_box_color, width_ratio=1.5)
        # Display text
        fruit_text = self.main_font.render(f"Next fruit : ", True, self.font_color)
        fruit_text_size = fruit_text.get_size()
        self.window.blit(fruit_text, (int(pos[0] + pos[2] * 0.5 - fruit_text_size[0] * 0.5),
                                      int(pos[1] + fruit_text_size[1] * 0.3)))
        # Display next fruit
        if self.show_next_fruit:
            image = self.next_fruit.image
            if type(image) != pygame.surface.Surface:
                image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)  # PIL image from pygame image
            fruit_size = image.get_size()
            self.window.blit(image, (int(pos[0] + pos[2] * 0.5 - fruit_size[0] * 0.5),
                                     int(pos[1] + pos[3] * 0.5 - fruit_size[1] * 0.4)))

    def display_commands(self):                                                 # Display commands box
        # Display commands background
        pos = self.display_default_box(self.commands_box_percent, self.commands_box_color)
        # Display commands
        command_text = self.main_font.render(f"Commands : ", True, self.font_color)
        command_text_size = command_text.get_size()
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.5 - command_text_size[0] * 0.5),
                                        int(pos[1] + pos[3] * 0.1 - command_text_size[1] * 0.5)))
        command_text = self.main_font.render(f"Left click - Drop fruit", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.25)))
        text = "Show" if not self.helping else "Hide"
        command_text = self.main_font.render(f"H - {text} line", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.35)))
        command_text = self.main_font.render(f"F - Fruitopedia", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.45)))
        command_text = self.main_font.render(f"Space - Pause game", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.55)))
        command_text = self.main_font.render(f"P - Parameters", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.65)))
        command_text = self.main_font.render(f"Return - Back to menu", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.75)))
        command_text = self.main_font.render(f"Q / Escape - Quit game", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.85)))

    def display_help_line(self):                                                # Display help line
        coord_x = int(self.current_fruit.pos_x - self.help_line_width * 0.5)
        up = self.current_fruit.pos_y + self.current_fruit.radius
        down = self.box_pos[1] + self.box_pos[3] - self.main_box_width
        surface = pygame.Surface((self.help_line_width, down - up)).convert_alpha()
        surface.fill(self.help_line_color)
        self.window.blit(surface, (coord_x, up))

    def display_highscore(self):                                                # Display scoreboard
        # Display score background
        pos = self.display_default_box(self.score_box_percent, self.score_box_color, width_ratio=2.0)
        # Display high score
        highscore = self.main_font.render(f"High score : {self.highscore} pts", True, self.font_color)
        highscore_size = highscore.get_size()
        self.window.blit(highscore, (int(pos[0] + pos[2] * 0.5 - highscore_size[0] * 0.5),
                                     int(pos[1] + pos[3] * 0.33 - highscore_size[1] * 0.5)))
        # Display score
        score = self.main_font.render(f"Score : {self.score} pts", True, self.font_color)
        score_size = score.get_size()
        self.window.blit(score, (int(pos[0] + pos[2] * 0.5 - score_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.67 - score_size[1] * 0.5)))

        mouse = pygame.mouse.get_pos()                                          # Display scoreboard
        if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3] and self.show_scoreboard:
            height = 20 * (len(self.Scoreboard) + 3)
            pygame.draw.rect(self.window, self.commands_box_color, (mouse[0], mouse[1], pos[2], height), 0, int(pos[3] * 0.1))
            width = int(min(pos[2], pos[3]) * self.border_ratio * 2)
            pygame.draw.rect(self.window, self.border_color, (mouse[0], mouse[1], pos[2], height), width, int(pos[3] * 0.1))
            # Display title
            title = self.main_font.render(f"Scoreboard : ", True, self.font_color)
            title_size = title.get_size()
            self.window.blit(title, (int(mouse[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                     int(mouse[1] + 20 - title_size[1] * 0.5)))
            # Display all scores
            for i, score in enumerate(self.Scoreboard):
                score_text = self.main_font.render(f"{i + 1} - {score} pts", True, self.font_color)
                score_size = score_text.get_size()
                self.window.blit(score_text, (int(mouse[0] + pos[2] * 0.3),
                                              int(mouse[1] + 20 * (i + 3) - score_size[1] * 0.5)))

    def Display_Icons(self):                                                    # Display icons
        icon_size = self.screen_height * 0.06
        # For shopping
        pos = (self.screen_width * 0.88, self.screen_height * 0.06, icon_size, icon_size)
        mouse = pygame.mouse.get_pos()
        percent = self.shopping_screen_percent
        shop_pos = (self.screen_width * percent[0], self.screen_height * percent[1],
                    self.screen_width * percent[2], self.screen_height * percent[3])
        if self.display_icon("shop.png", pos, True):
            self.shopping = True
        elif (self.shopping and shop_pos[0] <= mouse[0] <= shop_pos[0] + shop_pos[2] and
              shop_pos[1] <= mouse[1] <= shop_pos[1] + shop_pos[3]):            # Keep if mouse on it
            self.shopping = True
        else:
            self.shopping = False
        # For parameters
        pos = (self.screen_width * 0.94, self.screen_height * 0.06, icon_size, icon_size)
        if self.display_icon("settings.png", pos):
            self.on_para = not self.on_para
        # For sound
        sound = "loud.png" if self.volume > 0.75 else "medium.png" if 0.75 >= self.volume > 0.5 else \
                "small.png" if 0.5 >= self.volume > 0.25 else "mini.png" if 0.25 >= self.volume > 0 else "mute.png"
        pos = (self.screen_width * 0.94, self.screen_height * 0.4, icon_size, icon_size)
        self.display_icon(sound, pos)

    def display_icon(self, image_name, pos, hover=False):                       # Display icon
        icon = pygame.image.load(f"images/icons/{image_name}").convert_alpha()
        icon = pygame.transform.scale(icon, (pos[2], pos[3]))
        self.window.blit(icon, (pos[0], pos[1]))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        on_butt = pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3]
        on_time = True
        if self.current_time - self.click_last_timer < self.click_timer_duration:   # Waiting
            on_time = False
        else:                                                                   # If timer end
            if click and on_butt:                                               # If click on button
                self.click_last_timer = time()
                on_time = True
        condition = on_butt if hover else on_butt and click and on_time         # Check if click or hover
        return condition

    def Display_Shopping(self):                                                 # ! Working...
        # Display ask background
        pos = self.display_default_box(self.shopping_screen_percent)
        # Display ask title
        title = self.button_font.render(f"Shopping", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display powers
        size = pos[3] * 0.3
        click = pygame.mouse.get_pressed()[0]
        power_value = None
        if self.display_icon("pop.png", (pos[0] + pos[2] * 0.11, pos[1] + pos[3] * 0.35, size, size), True):
            power_value = 0
        if self.display_icon("sort.png", (pos[0] + pos[2] * 0.28, pos[1] + pos[3] * 0.35, size, size), True):
            power_value = 1
        if self.display_icon("smaller.png", (pos[0] + pos[2] * 0.45, pos[1] + pos[3] * 0.35, size, size), True):
            power_value = 2
        if self.display_icon("bigger.png", (pos[0] + pos[2] * 0.62, pos[1] + pos[3] * 0.35, size, size), True):
            power_value = 3
        if self.display_icon("current.png", (pos[0] + pos[2] * 0.79, pos[1] + pos[3] * 0.35, size, size), True):
            power_value = 4
        # Display keys
        number = self.main_font.render(f"1", True, self.font_color)
        number_size = number.get_size()
        self.window.blit(number, (int(pos[0] + pos[2] * 0.16 - number_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.8 - number_size[1] * 0.5)))
        number = self.main_font.render(f"2", True, self.font_color)
        number_size = number.get_size()
        self.window.blit(number, (int(pos[0] + pos[2] * 0.33 - number_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.8 - number_size[1] * 0.5)))
        number = self.main_font.render(f"3", True, self.font_color)
        number_size = number.get_size()
        self.window.blit(number, (int(pos[0] + pos[2] * 0.5 - number_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.8 - number_size[1] * 0.5)))
        number = self.main_font.render(f"4", True, self.font_color)
        number_size = number.get_size()
        self.window.blit(number, (int(pos[0] + pos[2] * 0.67 - number_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.8 - number_size[1] * 0.5)))
        number = self.main_font.render(f"5", True, self.font_color)
        number_size = number.get_size()
        self.window.blit(number, (int(pos[0] + pos[2] * 0.84 - number_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.8 - number_size[1] * 0.5)))
        # Display name and description of power (if mouse hover it)
        if power_value is not None:
            mouse = pygame.mouse.get_pos()
            x = float(format(mouse[0] / self.screen_width, '.5f'))
            y = float(format(mouse[1] / self.screen_height, '.5f'))
            percent = [x - self.power_screen_size[0], y, self.power_screen_size[0], self.power_screen_size[1]]
            pos_power = self.display_default_box(percent)
            name = self.main_font.render(f"{self.Powers[power_value].name.capitalize()}", True, self.font_color)
            power_size = name.get_size()
            self.window.blit(name, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                     int(pos_power[1] + pos_power[3] * 0.2 - power_size[1] * 0.5)))
            descr = self.commands_font.render(f"{self.Powers[power_value].description}", True, self.font_color)
            power_size = descr.get_size()
            self.window.blit(descr, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                     int(pos_power[1] + pos_power[3] * 0.5 - power_size[1] * 0.5)))
            cost = self.present_font.render(f"{self.Powers[power_value].cost} pts", True, self.font_color)
            power_size = cost.get_size()
            self.window.blit(cost, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                    int(pos_power[1] + pos_power[3] * 0.8 - power_size[1] * 0.5)))
        # Check if want to activate power
        if click and power_value is not None:
            self.power_index = power_value
            current_power = self.Powers[self.power_index]
            if self.score < current_power.cost:                                 # Check if have enough score
                check = self.button_font.render(f"You don't have enough score !", True, self.font_color)
                check_size = check.get_size()
                middle = (int(self.screen_width * 0.5 - check_size[0] * 0.5),
                          int(self.screen_height * 0.4 - check_size[1] * 0.5))
                self.window.blit(check, middle)
                for power in self.Powers:
                    power.active = False
            else:
                check = self.button_font.render(f"Power '{current_power.name}' activate !", True, self.font_color)
                check_size = check.get_size()
                middle = (int(self.screen_width * 0.5 - check_size[0] * 0.5),
                          int(self.screen_height * 0.4 - check_size[1] * 0.5))
                self.window.blit(check, middle)
                self.Powers[self.power_index].active = True
                self.powering = True

    def Display_Choose_Fruit(self):
        # Display ask background
        pos = self.display_default_box(self.choose_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Choose current fruit", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))

    def Display_Fruitopedia(self):                                              # Display screen with fruits data
        # Display ask background
        pos = self.display_default_box(self.all_fruits_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Fruitopedia", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        percent = 0.6
        percent *= 1.1 if self.diff_index == 0 else 1 if self.diff_index == 1 else \
                   0.9 if self.diff_index == 2 else 0.8                         # Offset fruit size (based on diff)
        for i, fruit in enumerate(self.Fruits):                                 # Display all fruits (dynamic)
            equation = i ** 1.5 / (len(self.Fruits) ** 1.5) + 0.05 if i > 0 else 0.05               # Function
            fruit.pos_x = pos[0] + pos[2] * equation - fruit.radius * percent
            fruit.pos_y = pos[1] + pos[3] * 0.5 - fruit.radius * percent
            self.draw_reduced_fruit(fruit, (fruit.pos_x, fruit.pos_y), percent)
            mouse = pygame.mouse.get_pos()
            if fruit.collide_point(mouse, percent):                             # Check if fruit collide
                name = self.present_font.render(f"{fruit.name.capitalize()}", True, self.font_color)
                name_size = name.get_size()
                self.window.blit(name, (int(pos[0] + pos[2] * equation - name_size[0] * 0.5),
                                        int(pos[1] + pos[3] * 0.7)))
                name = self.present_font.render(f"{fruit.present()}", True, self.font_color)
                name_size = name.get_size()
                self.window.blit(name, (int(pos[0] + pos[2] * equation - name_size[0] * 0.5),
                                        int(pos[1] + pos[3] * 0.75)))
        # Display buttons
        if self.display_button("Close", (int(pos[0] + pos[2] * 0.45), int(pos[1] + pos[3] * 0.82),
                                         int(pos[2] * 0.1), int(pos[3] * 0.15)), "F"):
            self.on_allF = not self.on_allF

    def Display_Lose(self):                                                     # Display lose screen
        # Display lose background
        pos = self.display_default_box(self.lose_screen_percent)
        # Display lose title
        title = self.small_title_font.render(f"You lose !", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display lose text
        text = self.main_font.render(f"Your fruit has protruded from the top of the bag.", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.2 - text_size[1] * 0.5)))
        text = self.main_font.render(f"SCORE", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.35 - text_size[1] * 0.5)))
        text = self.button_font.render(f"{self.score} PTS", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.4 - text_size[1] * 0.5)))
        text = self.main_font.render(f"High score", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.5 - text_size[1] * 0.5)))
        text = self.button_font.render(f"{self.highscore} PTS", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.55 - text_size[1] * 0.5)))
        if self.tip is None:                                                    # To avoid constant changing
            self.tip = choice(self.Tips)
        text = self.main_font.render(f"Tips : {self.tip}", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.7 - text_size[1] * 0.5)))
        text = self.main_font.render(f"Would you like to play again ?", True, self.font_color)
        text_size = text.get_size()
        self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                int(pos[1] + pos[3] * 0.8 - text_size[1] * 0.5)))
        # Display buttons
        if self.display_button("Restart", (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.85),
                                        int(pos[2] * 0.2), int(pos[3] * 0.1)), "SPACE"):
            self.start_new_game()
        if self.display_button("Menu", (int(pos[0] + pos[2] * 0.65), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "RETURN"):
            self.go_to_menu()

    def ask_back_menu(self):                                                    # If player want to quit during game
        # Display ask background
        pos = self.display_default_box(self.ask_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Back to menu ?", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        title = self.main_font.render(f"Your current game won't be saved.", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.4 - title_size[1] * 0.5)))
        # Display buttons
        if self.display_button("Yes", (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.7),
                                        int(pos[2] * 0.3), int(pos[3] * 0.25)), "Y"):
            self.go_to_menu()
        if self.display_button("No", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.7),
                                     int(pos[2] * 0.3), int(pos[3] * 0.25)), "N"):
            self.on_back = not self.on_back

    def ask_restart_game(self):
        # Display ask background
        pos = self.display_default_box(self.ask_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Restart game ?", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        title = self.main_font.render(f"You'll lose all your fruits'.", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.4 - title_size[1] * 0.5)))
        # Display buttons
        if self.display_button("Yes", (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.7),
                                        int(pos[2] * 0.3), int(pos[3] * 0.25)), "Y"):
            self.start_new_game()
        if self.display_button("No", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.7),
                                     int(pos[2] * 0.3), int(pos[3] * 0.25)), "N"):
            self.on_resG = not self.on_resG

    def Display_pause_screen(self):                                             # Display pause screen
        self.window.blit(self.paused_glass, (0, 0))                             # Semi-transparent background
        # Display pause text
        size = (self.screen_width, self.screen_height)
        pause_text = self.title_font.render(f"Pause", True, self.font_color)
        pause_size = pause_text.get_size()
        self.window.blit(pause_text, (int(size[0] * 0.5 - pause_size[0] * 0.5),
                                      int(size[1] * 0.25 - pause_size[1] * 0.5)))
        # Display button
        if self.display_button("Continue", (int(size[0] * 0.45), int(size[1] * 0.44),
                                            int(size[0] * 0.1), int(size[1] * 0.08)), "SPACE"):
            self.pausing = not self.pausing
        if self.display_button("Restart", (int(size[0] * 0.45), int(size[1] * 0.53),
                                           int(size[0] * 0.1), int(size[1] * 0.08)), "R"):
            self.start_new_game()
        if self.display_button("Parameters", (int(size[0] * 0.45), int(size[1] * 0.62),
                                              int(size[0] * 0.1), int(size[1] * 0.08)), "P"):
            self.on_para = not self.on_para
        if self.display_button("Menu", (int(size[0] * 0.45), int(size[1] * 0.71),
                                        int(size[0] * 0.1), int(size[1] * 0.08)), "RETURN"):
            self.go_to_menu()
        if self.display_button("Quit", (int(size[0] * 0.45), int(size[1] * 0.8),
                                        int(size[0] * 0.1), int(size[1] * 0.08)), "Q"):
            self.Close_Game()

    def display_default_box(self, size, color=None, border_color=None, width_ratio=1.0):    # Used for screens and boxes
        color = self.screens_color if color is None else color
        border_color = self.border_color if border_color is None else border_color

        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        short = min(pos[2], pos[3])
        pygame.draw.rect(self.window, color, pos, 0, int(short * 0.1))
        width = int(short * self.border_ratio * width_ratio)
        pygame.draw.rect(self.window, border_color, pos, width, int(short * 0.1))

        return pos                                                              # Needed for rest of the box

    def Display_Volume(self):                                                   # Display volume bar
        volume = 0 if self.is_mute else self.volume
        pos = [self.screen_width * 0.95, self.screen_height * 0.2, self.screen_height * 0.01, self.screen_height * 0.2]
        pygame.draw.rect(self.window, "orange", pos, 0, int(pos[2]))
        pos[1] = pos[1] + (1 - volume) * pos[3]
        pos[3] = pos[3] * volume
        pygame.draw.rect(self.window, "gold", pos, 0, int(pos[2]))

    def Display_brightness_glass(self):
        self.brightness_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.brightness_glass.fill(tuple(int(c * self.brightness) for c in (255, 255, 255)))
        self.brightness_glass.set_alpha(64)
        self.window.blit(self.brightness_glass, (0, 0))

    def Music_Manager(self):                                                    # Manage music
        if self.playing:
            pygame.mixer.music.load(self.music)                                 # Load music (once)
            pygame.mixer.music.play(self.repeat)                                # Play endlessly : -1
            self.playing = False
        self.volume = 0 if self.volume < 0 else 1.0 if self.volume > 1.0 else self.volume
        volume = 0 if self.is_mute else self.volume
        pygame.mixer.music.set_volume(volume)                                   # Set volume

    def start_new_game(self):                                                   # Reset game
        self.pausing = False
        self.helping = False
        self.on_menu = False
        self.on_game = True
        self.on_lose = False
        self.on_back = False
        self.on_resG = False
        self.on_allF = False

        self.score = 0
        self.Panier.empty()
        self.current_fruit = choice(self.FruitsChoosable)
        self.next_fruit = choice(self.FruitsChoosable)
        self.create_physics_space()
        self.tip = None

    def go_to_menu(self):                                                       # Change bools to go back to menu
        self.on_menu = True
        self.on_game = False
        self.on_lose = False
        self.on_help = False
        self.on_para = False                                                    # For parameters
        self.on_back = False
        self.on_resG = False
        self.on_allF = False
        self.create_physics_space()

    def Get_score(self):                                                        # ! Doesn't count merged last fruit
        score = 0
        for fruit in self.Panier.sprites():
            score += fruit.score
        return score

    @staticmethod
    def Reset_saved_scores():                                                    # Crush all saved scores
        print(f"Saved score reset !")
        file = open("scores/save.txt", "w")
        file.write(str(0))
        file.close()

    def Save_scores(self):                                                      # Save current score
        if self.score > 0 and self.score not in self.Scoreboard:
            self.Scoreboard.append(self.score)
        self.Scoreboard = list(set(self.Scoreboard))                            # Remove duplicates
        self.Scoreboard.sort()
        self.Scoreboard.reverse()
        while len(self.Scoreboard) > 20:                                        # If too much score, delete lowest
            self.Scoreboard.pop(-1)
        if self.score > self.highscore:                                         # ! Keep for congrats player
            print(f"Saving new high score... [{self.score} pts]")
        elif self.score > 0:
            print(f"High score not beaten : {self.highscore} pts")
        file = open("scores/save.txt", "w")
        for score in self.Scoreboard:                                           # Save all not null score
            if score > 0:
                file.write(f"{score}\n")
        file.close()

    def Load_score(self):                                                       # Load current score
        print("Loading last high score...")
        file = open("scores/save.txt", "r")
        lines = file.readlines()
        if lines:
            for line in lines:                                                  # Get all scores in Scoreboard
                self.Scoreboard.append(int(line))
            self.Scoreboard.sort()
            self.Scoreboard.reverse()
            self.highscore = max(self.Scoreboard)
        file.close()

    def Close_Game(self):                                                       # Close game
        if self.save_score:
            self.Save_scores()
        print("Closing game...")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    jeu = Game(random_music=True)
