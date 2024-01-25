import os.path
from math import sqrt, degrees
from random import random, randint, choice
from time import time
from datetime import datetime
from os import getcwd, listdir
from string import ascii_letters
from copy import deepcopy
from PIL import Image, ImageDraw, ImageEnhance
from player import Player
from fruit import Fruit
from skin import Skin
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
version : 0.2.6
language : python
purpose : Small game where you can merge fruit to get score. The bigger the fruit, the higher the score.
          Any resemblance to an existing game would be coincidental.
          All arguments are optional.
arguments : (3)
    - difficulty_index : Default value = 1. Informs about the difficulty level of the game.
                         More informations about difficulties in data file.
    - random_music : Default value = True. By default, choose a random music (Outer Wilds OST). 
                     If False, choose real game music.
    - using_skin : Default value = False. By default, fruit are circles. If False, fruit are images.
                   Doesn't affect physics.
requirements : libraries 'pygame', 'pymunk', 'math', 'random', 'time', 'string', 'os' and 'sys'.
"""

# ! Display what level has unlocked + play sounds
# ! Add music and palette for each skin (locked by player level)
# ! Add animation when gain xp in xp bar
# ! Add banner for profile (adding images) ?
# ! Rename dir when player changes pseudo


# [check] : Make window display + caption + icon
# [check] : Display random fruit on screen
# [check] : Forbid fruit from going out window + add gravitation
# [check] : Make collision between fruit + repulsion force
# [check] : Make same fruit fusion and create next fruit
# [check] : Add box and collisions with it + bg
# [check] : Add score and next fruit + current fruit
# [check] : Add player choose where to put fruit + make next fruit coherent
# [check] : Upgrade fruit physics + collisions + add timers (dropping next fruit + merging fruit)
# [check] : Add menu + buttons (start game, restart, go to menu, options, exit)
# [check] : Make buttons work + add project on GitHub
# [check] : Add save scores for scoreboard + screen Fruitopedia
# [check] : Add borders and reflect on fruit and buttons
# [check] : Add condition for losing game + make lose screen
# [check] : Adding more dynamic functions (display_default_box, fruit' size)
# [check] : Add music + lector + volume + mute
# [check] : Add parameters + balance difficulties
# [check] : Add skin for fruit (not used) + bg
# [check] : Add documentations + clean code + add comms
# [check] : Make all parameters work + add can change skin + make gradient bar fluid
# [check] : Can click on buttons + minors changing
# [check] : Add powers (cost score) : pop fruit / sort basket / make fruit smaller and heavier
# [check] : Upgrade physics (using pymunk) + balance score + make score when fruit merge
# [check] : Update lost screen when high score beaten + add sounds
# [check] : Add rolling fruit on menu (timer add) + add skins screen + add skin bg
# [check] : Add level with xp (based on score) + add icon account + player class
# [v0.2.8] : Add rewards (beat high score) + banners + palettes + animations
# [v0.2.9] : Change color palette / music based on day in calendar (valentine, halloween, christmas, ...)
# [v0.3.0] : Add credits + make the game in .exe + add update screen ?
# [v0.3.1] : Add notif when unlock objects (fruit images on level 1) -> append in Waiting_messages
class Game:                                                                     # Manage all game
    def __init__(self, difficulty_index=1, random_music=True, using_skin=False):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        # Main data
        self.creator = "One Shot"
        self.creator_pseudo = "OneShot"
        self.version = "v0.2.7"
        self.game_name = "Suika Fruit"
        self.date_of_creation = datetime(2023, 11, 23)
        self.today = datetime.today()                                           # ! [later] For color palette
        # Boolean data
        self.running = True                                                     # A little important
        self.loading = False                                                    # ! [later] For loading screen
        self.pausing = False                                                    # If game paused
        self.helping = False                                                    # Show help line
        self.playing = True                                                     # For loading music
        self.skining = False                                                    # Show skins
        self.profile = False                                                    # Show profile screen
        self.setProto = False                                                   # When player set avatar
        self.shopping = False                                                   # Show shopping
        self.powering = False                                                   # When using power
        self.choosing = False                                                   # Power 5 (choose current)
        self.beating = False                                                    # When beat high score
        self.on_menu = True                                                     # A little important
        self.on_game = False                                                    # During game
        self.on_keys = False                                                    # If editing player pseudo
        self.on_lose = False                                                    # If player loses
        self.on_help = False                                                    # For help note
        self.on_para = False                                                    # For parameters
        self.on_back = False                                                    # Ask for back menu (security)
        self.on_resG = False                                                    # Ask restart game (security)
        self.on_allF = False                                                    # For Fruitopedia
        self.as_gain = False                                                    # If player has gain xp
        self.is_mute = False                                                    # If music mute
        # Game data
        self.path = getcwd()                                                    # Get current position of programm
        self.Alphabet = ascii_letters                                           # All letters
        self.Numbers = [i for i in range(0, 10)]
        self.AuthorizedChars = ["_", "-", "ç", "à", "é", "è", "ê", "ù"]
        self.pressed = pygame.key.get_pressed()                                 # Pressed keys
        self.click = pygame.mouse.get_pressed()[0]                              # If left click
        self.mouse = pygame.mouse.get_pos()                                     # Get mouse coords
        self.clock = pygame.time.Clock()                                        # Manage the fps
        self.fps = 60
        # Physics data
        self.Space = None                                                       # Where law of physics applies
        self.space_options = None                                               # Normally not used
        self.space_step = float(1 / self.fps)                                   # Fps of space
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
        self.FruitsName = ["cherry", "strawberry", "grape", "clementine", "orange", "apple",
                           "pear", "peach", "pineapple", "melon", "watermelon"]
        self.FruitsColors = [(240, 0, 0), (255, 140, 160), (195, 75, 255), (255, 210, 40),
                             (255, 145, 45), (250, 20, 20), (255, 240, 105), (255, 190, 235),
                             (255, 250, 30), (160, 250, 70), (60, 210, 25)]
        self.Fruits = []                                                        # All possible fruit
        self.FruitsChoosable = []                                               # Fruits that can be dropped
        self.Panier = pygame.sprite.Group()                                     # Fruits in bucket during game
        self.using_skin = using_skin                                            # If using skin
        self.using_bg = False                                                   # If draw bg behind fruits image
        # Screens, some colors and tips data
        self.ask_screen_percent = [0.35, 0.35, 0.3, 0.3]
        self.help_screen_percent = [0.3, 0.1, 0.4, 0.8]
        self.lose_screen_percent = [0.4, 0.075, 0.4, 0.85]                      # Draw next to gain screen
        self.fruitopedia_screen_percent = [0.1, 0.25, 0.8, 0.5]
        self.choose_screen_percent = [0.25, 0.25, 0.5, 0.5]
        self.screen_color = (250, 250, 200)
        self.button_color = (230, 255, 140)
        self.border_color = (255, 160, 70)
        self.border_ratio = 0.02
        self.Waiting_messages = {}                                              # Don't know where to put it
        self.Tips = ["Try not to separate large fruit from each other",
                     "You can see the fruit evolution at the bottom left of the screen",
                     "Try to sort fruit by size so they can merge more easily",
                     "If the next fruit is the same as your current fruit, \n"
                     "you can merge them to have the next bigger fruit",
                     "If the skin make it difficult to see the fruit shape, \n"
                     "active 'Draw bg behind skin' in parameters'",
                     "If a fruit protrudes from the top of the bag, you lose !",
                     "The heaviest fruit are the lightest"]
        self.tip = None
        # Parameters data
        self.parameters_screen_percent = [0.1, 0.1, 0.8, 0.8]
        self.ParametersPercent = [(0.15, 0.35, 0.11, 0.05), (0.15, 0.4, 0.28, 0.05), (0.15, 0.45, 0.28, 0.05),
                                  (0.15, 0.65, 0.14, 0.05), (0.15, 0.7, 0.14, 0.05), (0.15, 0.75, 0.14, 0.05),
                                  (0.33, 0.65, 0.16, 0.05), (0.33, 0.7, 0.16, 0.05), (0.33, 0.75, 0.16, 0.05),
                                  (0.55, 0.35, 0.33, 0.06), (0.55, 0.45, 0.18, 0.05), (0.55, 0.65, 0.14, 0.05),
                                  (0.55, 0.7, 0.31, 0.05), (0.55, 0.75, 0.31, 0.05)]    # For parameters
        self.select_param_color = self.border_color
        self.select_param_index = 0
        self.gamma = 0.5                                                        # Percent gamma (false parameter)
        self.restart_game = False                                               # A parameter
        self.collect_cookies = True                                             # The cookie is a lie
        # Brightness data
        self.brightness = 0.5                                                   # Percent brightness (parameter)
        self.brightness_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.brightness_glass.fill(tuple(int(c * self.brightness) for c in (255, 255, 255)))
        self.brightness_glass.set_alpha(64)
        # Difficulty data
        self.Difficulties = ["Easy", "Medium", "Hard", "Impossible"]
        self.diff_index = difficulty_index                                      # Level of difficulty
        # Main box data (for fruit)
        self.main_box_percent = [0.33, 0.15, 0.34, 0.8]
        self.box_pos = (self.screen_width * self.main_box_percent[0],
                        self.screen_height * self.main_box_percent[1],
                        self.screen_width * self.main_box_percent[2],
                        self.screen_height * self.main_box_percent[3])
        self.main_box_width = 10                                                # In pixels
        self.main_box_color = (255, 200, 90)
        # Score data
        self.save_score = True                                                  # A parameter
        self.show_scoreboard = True                                             # A parameter
        self.score = 0
        self.highscore = 0
        self.Scoreboard = []
        self.nb_score_saved_max = 20
        self.score_box_percent = [0.08, 0.25, 0.15, 0.15]
        self.score_box_color = (255, 200, 90)
        # Player data
        self.player = Player()
        self.gap_avatar_screen = 0.05
        self.profile_screen_percent = [0.58, 0.1, 0.2, 0.5]                     # for profile screen
        self.gain_screen_percent = [0.12, 0.25, 0.2, 0.5]                       # Draw next to lose screen
        self.xp_bar_color = (255, 210, 45)
        self.set_avatar_screen_percent = [0.05, 0.1, 0.9, 0.8]                  # To set player avatar
        self.avatar_screen_size = [0.25, 0.5]
        self.face_bg_color = "lightyellow"
        self.lock_color = "grey"
        self.Faces = []
        self.pseudo_lenght_min = 3
        self.pseudo_lenght_max = 20
        self.key_index = 0
        # Skins data
        self.skins_screen_percent = [0.09, 0.1, 0.75, 0.75]
        self.skin_screen_size = [0.08, 0.22]
        self.SkinsNames = [_ for _ in listdir(f"{self.path}/images/skins")]
        self.SkinsLevel = [4, 5, 8, 2, 6, 9, 7, 3]
        self.SkinsDict = SkinsDict                                              # Import from data
        self.SkinsColors = {"ball": "chartreuse", "cake": "chocolate", "candy": "deeppink", "fruit": "darkorange",
                            "organ": "orangered", "planet": "blue", "shell": "aqua", "vegetable": "limegreen"}
        self.Skins = []
        self.skin_index = self.SkinsNames.index("fruit") if self.using_skin else None
        # Evolution of fruit box data
        self.evolution_box_percent = [0.06, 0.53, 0.19, 0.32]
        self.evolution_box_color = (255, 250, 140)
        # Current and next fruit data
        self.show_next_fruit = True                                             # A parameter
        self.current_fruit = None
        self.next_fruit_box_percent = [0.8, 0.21, 0.1, 0.18]
        self.next_fruit_box_color = (255, 250, 140)
        self.next_fruit = None
        # Commands and helping line data
        self.commands_box_percent = [0.775, 0.55, 0.15, 0.3]
        self.commands_box_color = (240, 210, 115)
        self.help_line_color = (255, 255, 220, 160)                             # Half transparent
        self.help_line_width = 5
        # Powers data
        self.shopping_screen_percent = [0.55, 0.1, 0.35, 0.2]
        self.power_screen_size = [0.1, 0.15]
        self.Powers = []
        self.power_index = None
        # Timers data
        self.current_time = time()
        self.rolling_last_timer = time()                                        # Fruit rolling on menu
        self.rolling_timer_duration = 0                                         # Make first one spawn faster
        self.click_last_timer = time()                                          # When player click (button or else)
        self.click_timer_duration = 0.5
        self.merging_fruit_last_timer = time()                                  # For merging fruit
        self.merging_fruit_timer_duration = 0.1
        self.next_fruit_last_timer = time()                                     # For dropping fruit
        self.next_fruit_timer_duration = 0.4
        self.message_last_timer = time()                                        # For display waiting messages
        self.message_timer_duration = 2
        # Pause screen data
        self.paused_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.rect(self.paused_glass, (255, 255, 255), self.paused_glass.get_rect())
        self.paused_glass.set_alpha(120)
        # Icon data
        self.icon = pygame.image.load("images/icons/icon.png")
        self.icon.set_colorkey((255, 255, 255))                                 # Remove white background
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                      # Game icon
        # Font data
        self.Fonts = [_ for _ in listdir(f"{self.path}/fonts") if _.endswith(".ttf")]  # Get fonts
        self.font_name = choice(self.Fonts)                                     # Choose random font
        self.title_font = pygame.font.Font(f"fonts/{self.font_name}", 100)
        self.small_title_font = pygame.font.Font(f"fonts/{self.font_name}", 50)
        self.button_font = pygame.font.Font(f"fonts/{self.font_name}", 30)      # Also use for screen's title
        self.main_font = pygame.font.Font(f"fonts/{self.font_name}", 20)
        self.present_font = pygame.font.Font(f"fonts/{self.font_name}", 16)
        self.commands_font = pygame.font.Font(f"fonts/{self.font_name}", 12)
        self.font_color = (255, 130, 20)
        # Music data
        self.Musics = [_ for _ in listdir(f"{self.path}/musics") if _.endswith(".mp3")]
        self.music = f"musics/{choice(self.Musics)}" if random_music else f"musics/main_music.mp3"
        self.repeat = -1                                                        # Endless by default
        self.volume = 0.5
        self.gap = 0.01
        # Sounds data
        self.volume_sound = 0.2
        self.drop_fruit_sound = pygame.mixer.Sound(f"sounds/drop_fruit.wav")
        self.Merge_sounds = [pygame.mixer.Sound(f"sounds/{_}") for _ in listdir(f"{self.path}/sounds")
                             if _.startswith("merge_fruit") and _.endswith(".wav")]
        self.high_score_sound = pygame.mixer.Sound(f"sounds/high_score_beaten.wav")
        self.level_up_sound = pygame.mixer.Sound(f"sounds/level_up.wav")
        self.unlock_sound = pygame.mixer.Sound(f"sounds/unlock_skins.wav")
        # Main function
        self.run()

    def set_sounds_volume(self):
        self.drop_fruit_sound.set_volume(self.volume_sound)
        for sound in self.Merge_sounds:
            sound.set_volume(self.volume_sound)
        self.high_score_sound.set_volume(self.volume_sound)
        self.level_up_sound.set_volume(self.volume_sound)
        self.unlock_sound.set_volume(self.volume_sound)

    def create_physics_space(self):                                             # Create / reset physics
        self.Space = pymunk.Space()
        self.Space.gravity = (0, int(gravity * 100))

        pymunk.pygame_util.positive_y_is_up = False                             # Make coords as pygame (reverse)
        self.space_options = pymunk.pygame_util.DrawOptions(self.window)        # Not used (unless for test)

        if self.on_game:
            self.create_space_boundaries()
        self.create_main_box()

    def create_space_boundaries(self):                                          # Make walls around window
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
            shape.elasticity = walls_elasticity
            shape.friction = walls_friction
            self.Space.add(body, shape)

    def create_main_box(self):                                                  # Create main box walls
        Positions = []
        thick = self.main_box_width
        half = int(thick * 0.5)

        if self.on_menu:
            Positions = [(- thick, self.screen_height * 0.75 + half, self.screen_width * 1.1, 0),
                         (- self.screen_width * 0.5, self.screen_height * 0.65,
                          self.screen_width * 0.5, self.screen_height * 0.1 + thick)]
        elif self.on_game:
            Positions = [(self.box_pos[0] + half, self.box_pos[1] + self.box_pos[3] - half, self.box_pos[2] - thick, 0),
                         (self.box_pos[0] + half, self.box_pos[1] - half, 0, self.box_pos[3]),
                         (self.box_pos[0] + self.box_pos[2] - half, self.box_pos[1] - half, 0, self.box_pos[3])]

        for pos in Positions:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            end = (pos[0] + pos[2], pos[1] + pos[3])
            shape = pymunk.Segment(body, (pos[0], pos[1]), end, half)
            shape.elasticity = walls_elasticity
            shape.friction = walls_friction
            self.Space.add(body, shape)

    def create_fruits(self):                                                    # Load fruit
        percent = 55 if self.diff_index == 0 else 50 if self.diff_index == 1 else \
                  45 if self.diff_index == 2 else 40
        size = int(self.screen_width * self.main_box_percent[2] / percent)      # Get fruit size (dynamic)
        self.Fruits = []
        for i, name in enumerate(self.FruitsName):
            # skin_image = self.Skins[self.skin_index].Images[i] if self.using_skin else None
            fruit = Fruit(name, self.FruitsColors[i], size * (i + 1), 10 * (i + 1), 2 ** i)
            self.Fruits.append(fruit)
        nb = 4 if self.diff_index == 3 else 5
        self.FruitsChoosable = self.Fruits[:nb]                                 # Can drop 4 or 5 firsts fruit

        self.next_fruit_timer_duration = 0.4 if self.diff_index == 0 else \
                                         0.5 if self.diff_index == 1 else \
                                         0.6 if self.diff_index == 2 else 0.7

        self.Panier.empty()
        self.current_fruit = choice(self.FruitsChoosable)
        self.next_fruit = choice(self.FruitsChoosable)
        self.score = 0

    def create_faces(self):                                                     # Create faces for player avatar
        height = round(1 - self.set_avatar_screen_percent[1] * 2 -
                       self.avatar_screen_size[1] - self.gap_avatar_screen, 2)
        face_size = int(self.screen_height * height * 0.8 / 6)
        for _ in listdir(f"{self.path}/images/profiles"):
            if not _.startswith("face"):
                image = Image.open(f"images/profiles/{_}")
                image = image.resize((face_size, face_size))
                self.Faces.append(image)

    def create_skins(self):                                                     # Create skins (dynamic ish)
        for i, name in enumerate(self.SkinsNames):
            skin = Skin(name, self.SkinsColors[name], self.SkinsDict[name], self.SkinsLevel[i])
            self.Skins.append(skin)

    def create_powers(self):                                                    # Create powers
        pop =     Power("pop", "Pop a fruit by clicking on it.", 500, 4)
        sort =    Power("sort", "Sort all fruit in basket.", 1000, 5)
        smaller = Power("smaller", "Make a fruit twice smaller", 250, 3)
        bigger =  Power("bigger", "Make a fruit twice bigger.", 250, 3)
        current = Power("current", "Choose current fruit.", 100, 2)
        self.Powers = [pop, sort, smaller, bigger, current]

    def run(self):                                                              # Main fonction of game
        self.loading = True
        self.set_sounds_volume()
        self.create_physics_space()
        self.create_fruits()
        self.create_faces()
        self.create_skins()
        self.create_powers()
        self.Load_scores()
        self.loading = False

        while self.running:                                                     # Main loop of game
            if not self.setProto:
                if self.on_menu:
                    self.Rolling_Fruits()
                    self.Collision_Manager()
                if self.on_game:
                    if not self.pausing:
                        # self.Update_Manager()                                     # Not used with new physics
                        self.Collision_Manager()
                    self.Check_Lose()

            self.Inputs_Manager()

            self.Display_Manager()

            self.Music_Manager()

            pygame.display.update()                                             # Can specify area
            # pygame.display.flip()
            self.clock.tick(self.fps)
            if not self.pausing:                                                # Kept here for menu physics
                self.Space.step(self.space_step)

    def Rolling_Fruits(self):                                                   # Add fruit to roll in bg
        if self.current_time - self.rolling_last_timer >= self.rolling_timer_duration:
            # Adding fruit
            fruit = choice(self.Fruits)
            skin_image = None
            nb = randint(0, len(self.Skins))
            if nb != len(self.Skins):                                           # Choose random skin
                skin = choice(self.Skins)
                place = self.FruitsName.index(fruit.name)
                skin_image = skin.Images[place]
            new_fruit = Fruit(fruit.name, fruit.color, fruit.radius,
                              fruit.weight, fruit.score, skin_image)
            # if self.using_bg:
            new_fruit.set_image(skin_image, self.using_bg)
            pos = (randint(- int(self.screen_width * 0.5), - int(self.screen_width * 0.1)),
                   self.screen_height * 0.3)                                    # Random pos make random speed
            new_fruit.create_physics_body(pos)
            self.Panier.add(new_fruit)
            self.Space.add(new_fruit.body, new_fruit.shape)
            # Reset timer
            self.rolling_timer_duration = randint(1, 5)                         # Time between dropping fruit random
            self.rolling_last_timer = time()

        for fruit in self.Panier.sprites():                                     # Remove fallen fruit
            if self.screen_height < fruit.pos_y:
                self.Panier.remove(fruit)
                self.Space.remove(fruit.body, fruit.shape)

    def Update_Manager(self):
        self.Panier.update()                                                    # Applied physics on fruit

    def Collision_Manager(self):                                                # Manage collisions
        for fruit in self.Panier.sprites():
            for other in self.Panier.sprites():                                 # Provide fruit to collide each other
                on_time = self.current_time - self.merging_fruit_last_timer >= self.merging_fruit_timer_duration
                if (fruit != other and fruit.collide_circle(other, self.diff_index)
                        and fruit.name == other.name and on_time):              # If fruit merge
                    choice(self.Merge_sounds).play()
                    pos = int(self.FruitsName.index(fruit.name) + 1)
                    self.score += fruit.score                                   # Add fruit score
                    if pos > len(self.Fruits) - 1:                              # If bigger fruit merge
                        self.Panier.remove(fruit, other)
                        self.Space.remove(fruit.body, fruit.shape)
                        self.Space.remove(other.body, other.shape)
                    else:                                                       # Normally merging same fruit
                        self.Panier.remove(fruit, other)
                        self.Space.remove(fruit.body, fruit.shape)
                        self.Space.remove(other.body, other.shape)

                        next_f = self.Fruits[pos]                               # Make spawn bigger fruit
                        skin_image = None
                        if self.using_skin:                                     # If using skin
                            place = self.FruitsName.index(next_f.name)
                            skin_image = self.Skins[self.skin_index].Images[place]
                        bigger = Fruit(next_f.name, next_f.color, next_f.radius,
                                       next_f.weight, next_f.score, skin_image)
                        bigger.set_image(skin_image, self.using_bg)
                        coords = [(fruit.pos_x + fruit.radius + other.pos_x + other.radius) / 2,
                                  (fruit.pos_y + fruit.radius + other.pos_y + other.radius) / 2]
                        new_vel = ((fruit.vel_x + other.vel_x) / 2, (fruit.vel_y + other.vel_y) / 2)
                        bigger.create_physics_body(coords, new_vel)
                        new_angle = int((- degrees(fruit.body.angle) % 360
                                         - degrees(other.body.angle) % 360) / 2)
                        bigger.body.angle = new_angle
                        self.Panier.add(bigger)
                        self.Space.add(bigger.body, bigger.shape)
                    self.merging_fruit_last_timer = time()

            """ Old physics
            # Prevent fruit to exit box
            if fruit.pos_x <= self.box_pos[0] + self.main_box_width:
                fruit.pos_x = self.box_pos[0] + self.main_box_width
                fruit.vel_x *= -1 * bounce                                      # Make bounce against box borders
            elif fruit.pos_x + fruit.radius * 2 >= self.box_pos[0] + self.box_pos[2] - self.main_box_width:
                fruit.pos_x = self.box_pos[0] + self.box_pos[2] - self.main_box_width - fruit.radius * 2
                fruit.vel_x *= -1 * bounce                                      # //
            if fruit.pos_y + fruit.radius * 2 >= self.box_pos[1] + self.box_pos[3] - self.main_box_width:
                fruit.pos_y = self.box_pos[1] + self.box_pos[3] - self.main_box_width - fruit.radius * 2
                fruit.vel_y = 0

            # Prevents fruit to exit box (possible ?)
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
            """

    def Check_Lose(self):                                                       # Check if fruit out of main box
        for fruit in self.Panier.sprites():
            on_time = self.current_time - self.next_fruit_last_timer > self.next_fruit_timer_duration
            if (fruit.pos_x != 0 and fruit.pos_y != 0 and fruit.pos_y + fruit.radius * 2 <
                    self.box_pos[1] and fruit.vel_y < 0 and on_time):           # If lose, save score
                self.on_lose = True
                self.Scoreboard = list(set(self.Scoreboard))                    # Remove duplicates
                if (len(self.Scoreboard) < self.nb_score_saved_max and
                        self.score not in self.Scoreboard):
                    self.Scoreboard.append(self.score)
                    self.Scoreboard.sort()
                    self.Scoreboard.reverse()
                break
        if self.score < 0:                                                      # If score error
            self.start_new_game()

    def Inputs_Manager(self):                                                   # Manage all inputs
        self.current_time = time()
        self.pressed = pygame.key.get_pressed()
        self.click = pygame.mouse.get_pressed()[0]
        self.mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Close_Game()

            if self.on_keys:                                                    # If player setting pseudo
                if event.type == pygame.KEYDOWN:
                    self.Keyboard_Manager(event)
            elif self.setProto:                                                 # If player setting avatar
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:                                 # Save player avatar
                        if self.player.pseudo_is_valid:
                            self.player.valid_proto()
                            self.Load_player_data()
                            self.setProto = False
                        else:
                            if len(self.player.pseudo) < self.pseudo_lenght_min:
                                self.add_message(f"Pseudonyme must have at least a length of "
                                                 f"{self.pseudo_lenght_min} characters !")
                            else:
                                self.add_message(f"'{self.player.pseudo}' isn't a valid pseudonyme !")
                    if event.key == pygame.K_RETURN:                            # Quit without update avatar, save proto
                        self.setProto = False
            else:
                if self.on_menu:                                                # If on menu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and not self.on_para:
                            if self.player.proto_is_valid:                            # If player avatar is set
                                self.start_new_game()                           # Start new game
                            else:
                                self.setProto = True

                        if not self.on_help and not self.on_para and event.key == pygame.K_a:  # For profile
                            self.profile = not self.profile

                        if not self.on_para and event.key == pygame.K_h:        # For help note
                            self.on_help = not self.on_help

                elif self.on_game:                                              # If on game
                    if self.on_lose:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN and not self.on_para:   # Go to menu
                                self.go_to_menu()

                            if event.key == pygame.K_SPACE:                     # Restart a game
                                self.start_new_game()
                    elif self.on_back:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:                         # Go back to menu
                                self.go_to_menu()
                            elif event.key == pygame.K_n:                       # Continue game
                                self.on_back = False
                    elif self.on_resG:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:                         # Restart new game
                                self.start_new_game()
                            elif event.key == pygame.K_n:                       # Continue game
                                self.on_resG = False
                    else:
                        width = self.main_box_width * 5
                        on_main_box = (self.box_pos[0] - width <= self.mouse[0] <= self.box_pos[0] +
                                       self.box_pos[2] + width and self.box_pos[1] - width <=
                                       self.mouse[1] <= self.box_pos[1] + self.box_pos[3] + width)
                        if (not self.pausing and not self.on_allF and on_main_box and not self.on_para
                                and not self.shopping and not self.choosing and not self.skining
                                and not self.profile and event.type == pygame.MOUSEBUTTONDOWN):
                            if self.powering:                                   # If using power
                                self.use_power()
                            else:
                                self.drop_fruit()                               # Drop current fruit

                        if event.type == pygame.KEYDOWN:
                            self.activate_power(key=event.key)

                            if event.key == pygame.K_SPACE:                     # For pause
                                self.pausing = not self.pausing

                            if event.key == pygame.K_h and not self.pausing:    # For help line
                                self.helping = not self.helping

                            if event.key == pygame.K_f and not self.pausing:    # For fruitopedia
                                self.on_allF = not self.on_allF

                            if event.key == pygame.K_r and self.pausing:        # Restart game
                                if len(self.Panier.sprites()) > 0:              # If game started, ask first
                                    self.on_resG = True
                                    self.pausing = False
                                else:
                                    self.start_new_game()

                            if event.key == pygame.K_RETURN and not self.on_para:   # Want to quit game
                                if len(self.Panier.sprites()) > 0:              # If game started, ask first
                                    self.on_back = True
                                    self.pausing = False
                                else:
                                    self.go_to_menu()                           # Exit current game

            if event.type == pygame.KEYDOWN and not self.on_keys:               # Almost always active
                if event.key == pygame.K_m:                                     # (un)mute music
                    self.is_mute = not self.is_mute
                    if self.is_mute:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                if not self.setProto:
                    if not self.profile and not self.on_help and event.key == pygame.K_p:   # For parameters
                        self.on_para = not self.on_para

                    if self.on_para:
                        if event.key == pygame.K_TAB:                           # Change selected param
                            self.select_param_index += -1 if self.pressed[pygame.K_LSHIFT] else 1
                            if self.select_param_index >= len(self.ParametersPercent):
                                self.select_param_index = 0
                            elif self.select_param_index < 0:
                                self.select_param_index = len(self.ParametersPercent) - 1

                        if event.key == pygame.K_RETURN:
                            self.Modify_checkbox_parameter()

                        if self.select_param_index == 9:                        # Difficulties
                            if event.key == pygame.K_LEFT:
                                if len(self.Panier.sprites()) > 0:              # If game started, ask first
                                    self.on_resG = True
                                else:
                                    self.Modify_gradient_parameter(-1)
                            elif event.key == pygame.K_RIGHT:
                                if len(self.Panier.sprites()) > 0:              # If game started, ask first
                                    self.on_resG = True
                                else:
                                    self.Modify_gradient_parameter(1)

                        if event.key == pygame.K_s:                             # Save params (do it anyway)
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

        if (self.pressed[pygame.K_q] or self.pressed[pygame.K_ESCAPE]) and not self.on_keys:    # Quit programm
            self.Close_Game()

    def Modify_checkbox_parameter(self):
        if self.select_param_index == 0:                                        # Fullscreen
            self.is_fullscreen = not self.is_fullscreen
            self.change_screen_size()
        elif self.select_param_index == 3:                                      # Auto save score
            self.save_score = not self.save_score
        elif self.select_param_index == 4:                                      # Auto restart game
            self.restart_game = not self.restart_game
        elif self.select_param_index == 5:                                      # The cookie is a lie
            self.collect_cookies = True
        elif self.select_param_index == 6:                                      # Show scoreboard
            self.show_scoreboard = not self.show_scoreboard
        elif self.select_param_index == 7:                                      # Show next fruit
            self.show_next_fruit = not self.show_next_fruit
        elif self.select_param_index == 8:                                      # Help line
            self.helping = not self.helping
        elif self.select_param_index == 10:                                     # Fruits skin bg
            if self.player.level >= min(self.SkinsLevel):                       # If unlocked
                self.using_bg = not self.using_bg
                if self.on_game:                                                # Don't apply on menu
                    self.change_skin()
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
            if len(self.Panier.sprites()) > 0:                                  # If game started, ask first
                self.on_resG = True
            else:
                self.diff_index += direction
                self.diff_index = 0 if self.diff_index >= len(self.Difficulties) else \
                                  len(self.Difficulties) - 1 if self.diff_index < 0 else self.diff_index
                self.create_fruits()
        elif self.select_param_index == 12:                                     # Music
            self.volume += self.gap * direction
            self.volume = 0 if self.volume < 0 else 1 if self.volume > 1 else self.volume
        elif self.select_param_index == 13:                                     # Sounds
            self.volume_sound += self.gap * direction
            self.volume_sound = 0 if self.volume_sound < 0 else 1 \
                                if self.volume_sound > 1 else self.volume_sound
            self.set_sounds_volume()

    def set_gamma(self):                                                        # Useless...
        # pixel = Sequence[int(255 * self.gamma)]
        # pygame.display.set_gamma_ramp(pixel, pixel, pixel)
        pass

    def use_power(self):                                                        # Use current power
        if self.powering and self.score >= self.Powers[self.power_index].cost:  # If using power and enough score
            if self.power_index == 4:                                           # Choose current fruit
                self.choosing = True
                self.powering = False
            elif self.power_index != 1:                                         # If not sorting
                for fruit in self.Panier.sprites():
                    if fruit.collide_point(self.mouse):                         # If click on fruit
                        skin_image = None
                        if self.using_skin:                                     # If using skin
                            place = self.FruitsName.index(fruit.name)
                            skin_image = self.Skins[self.skin_index].Images[place]

                        if self.power_index == 0:                               # Pop fruit
                            self.Panier.remove(fruit)
                            self.Space.remove(fruit.body, fruit.shape)
                        elif self.power_index == 2:                             # Make fruit smaller
                            old_angle = fruit.body.angle
                            self.Space.remove(fruit.body, fruit.shape)
                            fruit.radius = int(sqrt(pow(fruit.radius, 2) * 0.5))
                            fruit.image = fruit.set_image(skin_image, self.using_bg)
                            pos = (fruit.pos_x + fruit.radius, fruit.pos_y + fruit.radius)
                            fruit.create_physics_body(pos)
                            fruit.body.angle = old_angle
                            if fruit.body not in self.Space.bodies:
                                self.Space.add(fruit.body, fruit.shape)
                        elif self.power_index == 3:                             # Make fruit bigger
                            old_angle = fruit.body.angle
                            self.Space.remove(fruit.body, fruit.shape)
                            fruit.radius = int(sqrt(pow(fruit.radius, 2) * 2))
                            fruit.image = fruit.set_image(skin_image, self.using_bg)
                            pos = (fruit.pos_x + fruit.radius, fruit.pos_y + fruit.radius)
                            fruit.create_physics_body(pos)
                            fruit.body.angle = old_angle
                            if fruit.body not in self.Space.bodies:
                                self.Space.add(fruit.body, fruit.shape)
                        self.powering = False
                        break
            else:                                                               # Sort basket
                self.sort_basket()
                self.powering = False
            if not self.powering:                                               # If used power
                self.score -= self.Powers[self.power_index].cost
                self.Powers[self.power_index].active = False
                self.power_index = None

    def sort_basket(self):                                                      # Sort all fruit in basket (power)
        New_basket = self.sorted_basket_names()                                 # Get final basket (all fruit merged)

        self.Panier.empty()                                                     # Empty basket to refill it
        for body in self.Space.bodies:                                          # Empty space (keep walls)
            if body.body_type == pymunk.Body.DYNAMIC:
                self.Space.remove(body)
        for shape in self.Space.shapes:
            if shape.body.body_type == pymunk.Body.DYNAMIC:
                self.Space.remove(shape)

        for i, name in enumerate(New_basket):                                   # Adding fruit, bodies and shapes
            index = self.FruitsName.index(name)
            fruit = self.Fruits[index]                                          # Get actual fruit (with class)
            skin_image = None if not self.using_skin else self.Skins[self.skin_index].Images[index]
            new_fruit = Fruit(fruit.name, fruit.color, fruit.radius, fruit.weight, fruit.score, skin_image)
            if self.using_skin:
                new_fruit.set_image(skin_image, self.using_bg)
            # Calculate position based of number of fruits (can be upgrade)
            x_percent = 0.5 if len(New_basket) < 8 else 0.33 if i < int(len(New_basket) / 2) else 0.67
            y_percent = round(0.9 - (i % int(len(New_basket) / 2)) * 0.1, 2)
            new_fruit.pos_x = self.box_pos[0] + self.box_pos[2] * x_percent - new_fruit.radius
            new_fruit.pos_y = self.box_pos[1] + self.box_pos[3] * y_percent - new_fruit.radius
            pos = (new_fruit.pos_x + new_fruit.radius, new_fruit.pos_y + new_fruit.radius)
            new_fruit.create_physics_body(pos)                                  # Update position
            self.Panier.add(new_fruit)
            self.Space.add(new_fruit.body, new_fruit.shape)

    def sorted_basket_names(self):                                              # Return a dict
        Names = [fruit.name for fruit in self.Panier.sprites()]
        Names.sort()                                                            # Sort dict
        while self.check_fruit_in_double(Names):
            for name in Names:
                if Names.count(name) >= 2:
                    if self.diff_index == 0:                                    # If easy mode
                        fruit = self.Fruits[self.FruitsName.index(name)]        # Get fruit score
                        self.score += fruit.score                               # Add score from merging
                    Names.remove(name)                                          # Remove fruit in double
        Names.sort()                                                            # Sort dict
        return Names

    def check_fruit_in_double(self, List=None):
        Names = []
        if List is None:
            for fruit in self.Panier.sprites():
                if fruit.name in Names:
                    return True
                Names.append(fruit.name)
        else:
            for fruit in List:
                if fruit in Names:
                    return True
                Names.append(fruit)
        return False

    def drop_fruit(self):                                                       # Drop current fruit
        if self.current_time - self.next_fruit_last_timer >= self.next_fruit_timer_duration:
            self.drop_fruit_sound.play()
            skin_image = None
            if self.using_skin:                                                 # If using skin
                place = self.FruitsName.index(self.current_fruit.name)
                skin_image = self.Skins[self.skin_index].Images[place]
            fruit = Fruit(self.current_fruit.name, self.current_fruit.color, self.current_fruit.radius,
                          self.current_fruit.weight, self.current_fruit.score, skin_image)
            fruit.set_image(skin_image, self.using_bg)
            fruit.pos_x = self.current_fruit.pos_x                              # Place fruit
            fruit.pos_y = self.current_fruit.pos_y
            fruit.create_physics_body((fruit.pos_x + fruit.radius, fruit.pos_y + fruit.radius))
            self.Panier.add(fruit)
            self.Space.add(fruit.body, fruit.shape)
            self.current_fruit = self.next_fruit                                # Replace current fruit
            self.next_fruit = choice(self.FruitsChoosable)                      # Change next fruit
            self.next_fruit_last_timer = time()

    def activate_power(self, value=None, key=None, name=None):                  # Have several ways to activate power
        if name:
            for power in self.Powers:
                if power.name == name:
                    self.power_index = self.Powers.index(power)
                    break
            else:
                self.power_index = None
        elif key:
            if key == pygame.K_KP1:
                self.power_index = 0 if self.power_index != 0 else None
            elif key == pygame.K_KP2:
                self.power_index = 1 if self.power_index != 1 else None
            elif key == pygame.K_KP3:
                self.power_index = 2 if self.power_index != 2 else None
            elif key == pygame.K_KP4:
                self.power_index = 3 if self.power_index != 3 else None
            elif key == pygame.K_KP5:
                self.power_index = 4 if self.power_index != 4 else None
        else:
            if self.power_index != value:                                       # To unselect power
                self.power_index = value
            else:
                self.power_index = None
        if self.power_index is not None:                                        # If one power selected
            for i, power in enumerate(self.Powers):
                if self.power_index == i:
                    if self.score >= power.cost:                                # If enough score
                        power.active = True
                        self.powering = True
                    else:
                        self.power_index = None
                        power.active = False
                        self.add_message("You don't have enough score !")
                    break
        if self.power_index is None:
            self.powering = False

    def Display_Manager(self):                                                  # Manage all things to draw
        if self.setProto:
            self.Display_Set_Avatar()
            self.Display_Waiting_messages()
        else:
            if self.on_menu:
                self.Display_Menu()
            elif self.on_game:
                self.Display_Game()
        self.Display_Volume()
        self.Display_brightness_glass()                                         # Manage luminosity (keep last)

    def Display_Menu(self):                                                     # Display main menu
        # self.window.fill(self.bg_color)
        self.window.blit(self.bg_image, (0, 0))

        for fruit in self.Panier:                                               # Display all fruit
            fruit.draw(self.window, True)

        self.display_title()

        # self.Space.debug_draw(self.space_options)                             # Show walls

        # Display main buttons
        gap = 0.11
        button_size = [int(self.screen_width * 0.15), int(self.screen_height * 0.09)]
        condition = not self.profile and not self.on_help and not self.on_para  # If nothing open
        if self.display_button("Play", (int(self.screen_width * 0.425),
                int(self.screen_height * 0.4), *button_size), "RETURN", condition):
            if self.player.proto_is_valid:                                            # If player avatar is set
                self.start_new_game()                                           # Start new game
            else:
                self.setProto = True
        if self.display_button("Profile", (int(self.screen_width * 0.425),
                   int(self.screen_height * (0.4 + gap * 1)), *button_size), "A", condition):
            self.profile = not self.profile
        if self.display_button("Help", (int(self.screen_width * 0.425),
                int(self.screen_height * (0.4 + gap * 2)), *button_size), "H", condition):
            self.on_help = not self.on_help
        if self.display_button("Parameters", (int(self.screen_width * 0.425),
                      int(self.screen_height * (0.4 + gap * 3)), *button_size), "P", condition):
            self.on_para = not self.on_para
        if self.display_button("Quit", (int(self.screen_width * 0.425),
                int(self.screen_height * (0.4 + gap * 4)), *button_size), "Q", condition):
            self.Close_Game()

        # Display creator name and version
        creator_text = self.button_font.render(f"{self.creator}", True, self.bg_color)
        creator_pos = creator_text.get_rect(center=(self.screen_width * 0.05, self.screen_height * 0.95))
        self.window.blit(creator_text, creator_pos)
        version_text = self.button_font.render(f"{self.version}", True, self.bg_color)
        version_pos = version_text.get_rect(center=(self.screen_width * 0.95, self.screen_height * 0.95))
        self.window.blit(version_text, version_pos)

        if self.profile:
            self.Display_Profile(menu=True)
        if self.on_help:
            self.Display_Help()
        if self.on_para:
            self.Display_Parameters()

        # pygame.mouse.set_cursor(pygame.cursors.diamond)                       # ! Change cursor

    def display_title(self):                                                    # Display game name (menu)
        title = self.title_font.render(f"{self.game_name}", True, self.font_color)
        title_pos = title.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.2))
        self.window.blit(title, title_pos)

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
        on_butt = pos[0] <= self.mouse[0] <= pos[0] + pos[2] and pos[1] <= self.mouse[1] <= pos[1] + pos[3]
        on_time = True
        if self.current_time - self.click_last_timer < self.click_timer_duration:   # Waiting
            on_time = False
        else:                                                                   # If timer end
            if self.click and on_butt and condition:                            # If click on button
                self.click_last_timer = time()
                on_time = True
        return self.click and on_butt and on_time and condition

    def Display_Help(self):                                                     # Display help note
        # Display help background
        pos = self.display_default_box(self.help_screen_percent)
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
        to_write = (f"Get the highest score by merging identical fruit.\nThere is 11 fruit in all.\n"
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

        gameplay = self.button_font.render(f"Gameplay : ", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.55)))
        gameplay = self.main_font.render(f"Save score", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * Percent[3][0]), int(pos[1] + pos[3] * Percent[3][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.26), int(pos[1] + pos[3] * 0.65)), self.save_score)
        gameplay = self.main_font.render(f"Restart game", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * Percent[4][0]), int(pos[1] + pos[3] * Percent[4][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.26), int(pos[1] + pos[3] * 0.7)), self.restart_game)
        gameplay = self.main_font.render(f"Collect cookies", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * Percent[5][0]), int(pos[1] + pos[3] * Percent[5][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.26), int(pos[1] + pos[3] * 0.75)), self.collect_cookies)
        gameplay = self.main_font.render(f"Show scoreboard", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * Percent[6][0]), int(pos[1] + pos[3] * Percent[6][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.46), int(pos[1] + pos[3] * 0.65)), self.show_scoreboard)
        gameplay = self.main_font.render(f"Show next fruit", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * Percent[7][0]), int(pos[1] + pos[3] * Percent[7][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.46), int(pos[1] + pos[3] * 0.7)), self.show_next_fruit)
        gameplay = self.main_font.render(f"Show help line", True, self.font_color)
        self.window.blit(gameplay, (int(pos[0] + pos[2] * Percent[8][0]), int(pos[1] + pos[3] * Percent[8][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.46), int(pos[1] + pos[3] * 0.75)), self.helping)

        diff = self.button_font.render(f"Difficulty : ", True, self.font_color)
        self.window.blit(diff, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.25)))
        for i, diff in enumerate(self.Difficulties):
            diff_text = self.main_font.render(f"{diff}", True, self.font_color)
            diff_coords = (int(pos[0] + pos[2] * (Percent[9][0] + i * 0.08)), int(pos[1] + pos[3] * Percent[9][1]))
            self.window.blit(diff_text, diff_coords)
            if self.diff_index == i:                                            # Frame current difficulties
                diff_size = diff_text.get_size()
                select_pos = (int(diff_coords[0] - diff_size[0] * 0.15), int(diff_coords[1] - diff_size[1] * 0.1),
                              int(diff_size[0] * 1.3), int(diff_size[1] * 1.3))
                pygame.draw.rect(self.window, self.font_color, select_pos, 3, 5)
        font_color = self.lock_color if self.player.level < min(self.SkinsLevel) else self.font_color
        diff = self.main_font.render(f"Draw bg behind skin", True, font_color)
        self.window.blit(diff, (int(pos[0] + pos[2] * Percent[10][0]), int(pos[1] + pos[3] * Percent[10][1])))
        self.display_checkbox((int(pos[0] + pos[2] * 0.7), int(pos[1] + pos[3] * 0.45)), self.using_bg)
        if self.player.level < min(self.SkinsLevel):
            size = diff.get_size()
            self.display_icon("lock.png", (int(pos[0] + pos[2] * Percent[10][0] + size[0] * 0.5),
                              int(pos[1] + pos[3] * Percent[10][1]) - size[1] * 0.5, size[1] * 2, size[1] * 2))

        music = self.button_font.render(f"Musics & Sounds : ", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.55)))
        music = self.main_font.render(f"Endless music", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * Percent[11][0]), int(pos[1] + pos[3] * Percent[11][1])))
        endless = True if self.repeat == -1 else False
        self.display_checkbox((int(pos[0] + pos[2] * 0.66), int(pos[1] + pos[3] * 0.65)), endless)
        music = self.main_font.render(f"Music", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * Percent[12][0]), int(pos[1] + pos[3] * Percent[12][1])))
        self.display_gradient_bar((pos[0] + pos[2] * 0.66, pos[1] + pos[3] * 0.72),
                                  gradient=11, percent=self.volume)
        music = self.main_font.render(f"Sounds", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * Percent[13][0]), int(pos[1] + pos[3] * Percent[13][1])))
        self.display_gradient_bar((pos[0] + pos[2] * 0.66, pos[1] + pos[3] * 0.77),
                                  gradient=11, percent=self.volume_sound)
        # Display selected parameter
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

        self.display_main_box()                                                 # Main box for fruit
        self.display_evolution()
        self.display_next_fruit()
        self.display_commands()

        self.display_current_fruit()

        if self.helping:                                                        # Help line draw beyond fruit
            self.display_help_line()

        # self.Space.debug_draw(self.space_options)                             # Show walls

        for fruit in self.Panier:                                               # Display all fruit
            fruit.draw(self.window, self.using_skin)

        # Placed here for scoreboard to be in front of help line
        self.display_highscore()

        self.Display_Icons()

        if self.shopping:                                                       # Display Shopping
            self.Display_Shopping()

        if self.skining:
            self.Display_Skins()

        if self.profile:
            self.Display_Profile()

        if self.powering:                                                       # Warn player using power
            name = self.Powers[self.power_index].name.capitalize()
            text = self.button_font.render(f"Left click to activate power '{name}'.", True, self.font_color)
            text_pos = text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.5))
            self.window.blit(text, text_pos)

        self.Display_Waiting_messages()

        if self.choosing:
            self.Display_Choose_Fruit()

        if self.on_allF:
            self.Display_Fruitopedia()

        if self.on_lose:
            if self.restart_game:                                               # Check if auto restart game
                self.start_new_game()
            else:
                self.Display_Gain_XP()                                          # Gain xp when lose
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
        title_pos = title.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.1))
        self.window.blit(title, title_pos)

    def display_main_box(self):                                                 # Display main box for fruit
        self.box_pos = (self.screen_width * self.main_box_percent[0], self.screen_height * self.main_box_percent[1],
                        self.screen_width * self.main_box_percent[2], self.screen_height * self.main_box_percent[3])
        pygame.draw.rect(self.window, self.next_fruit_box_color, self.box_pos, 0, self.main_box_width * 2)
        pygame.draw.rect(self.window, self.main_box_color, self.box_pos, self.main_box_width, self.main_box_width * 2)

    def display_evolution(self):                                                # Display evolution of fruit
        # Display evolution background
        pos = self.display_default_box(self.evolution_box_percent, self.evolution_box_color)
        # Display text
        evolution = self.main_font.render(f"Evolution : ", True, self.font_color)
        evolution_size = evolution.get_size()
        self.window.blit(evolution, (int(pos[0] + pos[2] * 0.5 - evolution_size[0] * 0.5),
                                     int(pos[1] + pos[3] * 0.1 - evolution_size[1] * 0.5)))
        # Display fruit around invisible circle
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

    def draw_reduced_fruit(self, fruit, pos, percent=1 / 3):                    # Use to draw a smaller fruit image
        place = self.FruitsName.index(fruit.name)
        skin_image = None if not self.using_skin else self.Skins[self.skin_index].Images[place]
        copy = fruit.set_image(skin_image, False)
        if self.using_skin and type(copy) != pygame.surface.Surface:
            copy = pygame.image.fromstring(copy.tobytes(), copy.size, copy.mode)
        size = int(fruit.radius * percent * 2)
        copy = pygame.transform.scale(copy, (size, size))
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
            fruit_size = self.next_fruit.pygame_image.get_size()
            self.window.blit(self.next_fruit.pygame_image, (int(pos[0] + pos[2] * 0.5 - fruit_size[0] * 0.5),
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
        command_text = self.main_font.render(f"H - {text} help line", True, self.font_color)
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

    def display_current_fruit(self):
        if not self.pausing:                                                    # Draw current fruit (on mouse position)
            self.current_fruit.pos_x = self.mouse[0] - self.current_fruit.radius
            min_b = self.screen_width * self.main_box_percent[0] + self.main_box_width
            max_b = (min_b + self.screen_width * self.main_box_percent[2] -
                     (self.main_box_width + self.current_fruit.radius) * 2)
            self.current_fruit.pos_x = min_b if self.current_fruit.pos_x < min_b else max_b \
                if self.current_fruit.pos_x > max_b else self.current_fruit.pos_x
        self.current_fruit.pos_y = self.screen_height * 0.1 - self.current_fruit.radius

        # Use once for each choosable fruit
        if self.using_skin:                                                     # Update skin and bg
            self.current_fruit.set_image(self.current_fruit.image, self.using_bg)
        self.window.blit(self.current_fruit.pygame_image, (self.current_fruit.pos_x, self.current_fruit.pos_y))

    def display_help_line(self):                                                # Display help line
        radius = self.current_fruit.radius
        down = self.box_pos[1] + self.box_pos[3] - self.main_box_width
        up = self.current_fruit.pos_y + radius * 2
        surface = pygame.Surface((self.help_line_width, down - up)).convert_alpha()
        surface.fill(self.help_line_color)
        coord_x = int(self.current_fruit.pos_x + radius - self.help_line_width * 0.5)
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

        # Display scoreboard
        if pos[0] <= self.mouse[0] <= pos[0] + pos[2] and pos[1] <= self.mouse[1] <= pos[1] + pos[3] and self.show_scoreboard:
            height = 20 * (len(self.Scoreboard) + 3)
            pygame.draw.rect(self.window, self.commands_box_color, (self.mouse[0], self.mouse[1],
                                                                    pos[2], height), 0, int(pos[3] * 0.1))
            width = int(min(pos[2], pos[3]) * self.border_ratio * 2)
            pygame.draw.rect(self.window, self.border_color, (self.mouse[0], self.mouse[1],
                                                              pos[2], height), width, int(pos[3] * 0.1))
            # Display title
            title = self.main_font.render(f"Scoreboard : ", True, self.font_color)
            title_size = title.get_size()
            self.window.blit(title, (int(self.mouse[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                     int(self.mouse[1] + 20 - title_size[1] * 0.5)))
            # Display all scores
            for i, score in enumerate(self.Scoreboard):
                score_text = self.main_font.render(f"{i + 1} - {score} pts", True, self.font_color)
                score_size = score_text.get_size()
                self.window.blit(score_text, (int(self.mouse[0] + pos[2] * 0.3),
                                              int(self.mouse[1] + 20 * (i + 3) - score_size[1] * 0.5)))

    def Display_Icons(self):                                                    # Display icons
        gap = self.screen_width * 0.06
        icon_size = self.screen_height * 0.06
        # For profile
        pos = (self.screen_width - gap * 4, icon_size, icon_size, icon_size)
        percent = self.profile_screen_percent
        profile_pos = (self.screen_width * percent[0], self.screen_height * percent[1],
                    self.screen_width * percent[2], self.screen_height * percent[3])
        if self.display_icon("profile.png", pos, True):
            self.profile = True
        elif (self.profile and profile_pos[0] <= self.mouse[0] <= profile_pos[0] + profile_pos[2] and
              profile_pos[1] <= self.mouse[1] <= profile_pos[1] + profile_pos[3]):  # Keep if mouse on it
            self.profile = True
        else:
            self.profile = False
        # For skins
        pos = (self.screen_width - gap * 3, icon_size, icon_size, icon_size)
        percent = self.skins_screen_percent
        skins_pos = (self.screen_width * percent[0], self.screen_height * percent[1],
                    self.screen_width * percent[2], self.screen_height * percent[3])
        if self.display_icon("skins.png", pos, True):
            self.skining = True
        elif (self.skining and skins_pos[0] <= self.mouse[0] <= skins_pos[0] + skins_pos[2] and
              skins_pos[1] <= self.mouse[1] <= skins_pos[1] + skins_pos[3]):    # Keep if mouse on it
            self.skining = True
        else:
            self.skining = False
        # For shopping
        pos = (self.screen_width - gap * 2, icon_size, icon_size, icon_size)
        percent = self.shopping_screen_percent
        shop_pos = (self.screen_width * percent[0], self.screen_height * percent[1],
                    self.screen_width * percent[2], self.screen_height * percent[3])
        if self.display_icon("shop.png", pos, True):                            # If mouse on shopping
            self.shopping = True
        elif (self.shopping and shop_pos[0] <= self.mouse[0] <= shop_pos[0] + shop_pos[2] and
              shop_pos[1] <= self.mouse[1] <= shop_pos[1] + shop_pos[3]):       # Keep if mouse on it
            self.shopping = True
        else:
            self.shopping = False
        # For parameters
        pos = (self.screen_width - gap, icon_size, icon_size, icon_size)
        if self.display_icon("settings.png", pos):
            self.on_para = not self.on_para
        # For sound (under sound bar)
        sound = "loud.png" if self.volume > 0.75 else "medium.png" if 0.75 >= self.volume > 0.5 else \
            "small.png" if 0.5 >= self.volume > 0.25 else "mini.png" if 0.25 >= self.volume > 0 else "mute.png"
        pos = (self.screen_width * 0.94, self.screen_height * 0.4, icon_size, icon_size)
        self.display_icon(sound, pos)

    def display_icon(self, image_name, pos, hover=False):                       # Display icon
        icon = pygame.image.load(f"images/icons/{image_name}").convert_alpha() \
               if type(image_name) == str else image_name
        icon = pygame.transform.scale(icon, (pos[2], pos[3]))
        self.window.blit(icon, (pos[0], pos[1]))
        on_butt = pos[0] <= self.mouse[0] <= pos[0] + pos[2] and pos[1] <= self.mouse[1] <= pos[1] + pos[3]
        on_time = True
        if self.current_time - self.click_last_timer < self.click_timer_duration:   # Waiting
            on_time = False
        else:                                                                   # If timer end
            if self.click and on_butt:                                          # If click on button
                self.click_last_timer = time()
                on_time = True
        condition = on_butt if hover else on_butt and self.click and on_time    # Check if click or hover
        return condition

    def Display_Shopping(self):                                                 # Display shopping
        # Display shop background
        pos = self.display_default_box(self.shopping_screen_percent)
        # Display shop title
        title = self.button_font.render(f"Shopping", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.2 - title_size[1] * 0.5)))
        # Display powers and keys (dynamic)
        gap = 0.17
        size = pos[3] * 0.3
        power_value = None
        for i, power in enumerate(self.Powers):
            locked = self.player.level < power.level_unlock
            image = power.pygame_lock_image if locked else power.pygame_image
            if self.display_icon(image, (pos[0] + pos[2] * (0.11 + gap * i),
                                         pos[1] + pos[3] * 0.35, size, size), True):
                power_value = i
            font_color = self.lock_color if locked else self.font_color
            number = self.main_font.render(f"[{i + 1}]", True, font_color)
            number_size = number.get_size()
            self.window.blit(number, (int(pos[0] + pos[2] * (0.16 + gap * i) - number_size[0] * 0.5),
                                      int(pos[1] + pos[3] * 0.8 - number_size[1] * 0.5)))
            if locked:                                                          # If power locked
                self.display_icon("lock.png", (pos[0] + pos[2] * (0.11 + gap * i),
                                               pos[1] + pos[3] * 0.35, size, size))
        # Display power informations (if mouse hover it)
        if power_value is not None:
            x = float(format(self.mouse[0] / self.screen_width, '.5f'))
            y = float(format(self.mouse[1] / self.screen_height, '.5f'))
            percent = [x - self.power_screen_size[0], y, self.power_screen_size[0], self.power_screen_size[1]]
            pos_power = self.display_default_box(percent)
            power = self.Powers[power_value]
            font_color = self.lock_color if self.player.level < power.level_unlock else self.font_color
            name = self.main_font.render(f"{power.name.capitalize()}", True, font_color)
            power_size = name.get_size()
            self.window.blit(name, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                     int(pos_power[1] + pos_power[3] * 0.2 - power_size[1] * 0.5)))
            ed = "ed" if self.player.level >= power.level_unlock else ""
            descr = self.commands_font.render(f"Unlock{ed} at level {power.level_unlock}", True, font_color)
            power_size = descr.get_size()
            self.window.blit(descr, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                     int(pos_power[1] + pos_power[3] * 0.35 - power_size[1] * 0.5)))
            descr = self.commands_font.render(f"{power.description}", True, font_color)
            power_size = descr.get_size()
            self.window.blit(descr, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                     int(pos_power[1] + pos_power[3] * 0.55 - power_size[1] * 0.5)))
            cost = self.present_font.render(f"{power.cost} pts", True, font_color)
            power_size = cost.get_size()
            self.window.blit(cost, (int(pos_power[0] + pos_power[2] * 0.5 - power_size[0] * 0.5),
                                    int(pos_power[1] + pos_power[3] * 0.8 - power_size[1] * 0.5)))
        # Check if want to activate power
        if self.click and power_value is not None:
            self.power_index = power_value
            current_power = self.Powers[self.power_index]
            locked = self.player.level < current_power.level_unlock
            if locked:                                                          # If power locked
                self.add_message("You can't use that power yet !")
            elif self.score < current_power.cost:                               # If not enough score
                for power in self.Powers:
                    power.active = False
                self.add_message("You don't have enough score !")
            else:
                self.Powers[self.power_index].active = True
                self.powering = True
                self.add_message(f"Power '{current_power.name}' activate !")

    def Display_Skins(self):                                                    # Display skins
        # Display skins background
        pos = self.display_default_box(self.skins_screen_percent, width_ratio=0.5)
        # Display skins title
        title = self.button_font.render(f"Skins", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.07 - title_size[1] * 0.5)))
        # Display skins help
        des = "des" if self.using_skin else ""
        current = "current" if self.using_skin else "any"
        help_text = self.main_font.render(f"Left click on {current} skin to {des}activate it", True, self.font_color)
        help_text.set_alpha(128)
        help_size = help_text.get_size()
        self.window.blit(help_text, (int(pos[0] + pos[2] * 0.95 - help_size[0]), int(pos[1] + pos[3] * 0.05)))
        # Display skins (dynamic)
        by_column = 3
        by_line = 3
        if not (by_column <= 0 or by_line <= 0 or len(self.Skins) <= 0):
            x, y = 0, 0
            index_i, index_j = 0, 0
            block_gap = int(pos[2] * 0.03)                                      # Distance between block (x and y)
            size_x = int((pos[2] - block_gap * (by_column + 1)) / by_column)    # width of block
            size_y = int((pos[3] * 0.85 - block_gap * (by_line + 1)) / by_line) # height of block
            font_height = self.button_font.get_height()
            icon_gap = int(font_height / 2)
            icon_size = int((size_y - font_height - icon_gap * 2) / 2)          # 2 lines of skin per block

            for i, skin in enumerate(self.Skins):
                if i >= by_column * by_line:                                    # Avoid display outside screen
                    break
                block_x = block_gap * (i % by_column + 1) + size_x * (i % by_column)
                block_y = pos[3] * 0.1 + block_gap * int(i / by_column + 1) + size_y * int(i / by_column)
                block_pos = [pos[0] + block_x, pos[1] + block_y, size_x, size_y]
                width = int(min(block_pos[2], block_pos[3]) * (self.border_ratio * 5))
                block_pos[3] += width
                locked = self.player.level < skin.level_unlock                          # Check if locked
                bg_color = skin.get_bg_color(self.lock_color, 6) if locked else skin.bg_color
                pygame.draw.rect(self.window, bg_color, block_pos, 0, width)            # Draw bg
                if self.using_skin and self.skin_index == i:                            # If skin is current skin
                    pygame.draw.rect(self.window, skin.color, block_pos, 3, width)      # Draw borders
                font_color = self.lock_color if locked else skin.color
                title = self.button_font.render(f"{skin.name.capitalize()}", True, font_color)
                self.window.blit(title, (int(pos[0] + block_x + width), int(pos[1] + block_y)))

                if self.click and block_pos[0] <= self.mouse[0] <= block_pos[2] + block_pos[0] and \
                        block_pos[1] <= self.mouse[1] <= block_pos[3] + block_pos[1]:   # If click on skin
                    if locked:
                        self.add_message("You can't use that skin yet !")
                    else:                                                               # (Un)select skin
                        if self.current_time - self.click_last_timer >= self.click_timer_duration:
                            self.using_skin = False if self.skin_index == i else True
                            self.skin_index = None if self.skin_index == i else i
                            self.change_skin()
                            self.click_last_timer = time()

                for j, image in enumerate(skin.Images):                                 # Draw skins
                    nb = j - int(len(skin.Images) / 2) - 1 if j > len(skin.Images) / 2 else j
                    icon_x = block_x + nb * icon_size + nb * icon_gap
                    plus = icon_size + icon_gap if j > len(skin.Images) / 2 else 0      # For second line
                    icon_y = block_y + font_height + icon_gap + plus
                    picture = image
                    if locked:                                                          # Draw gray image
                        filtre = ImageEnhance.Color(picture)
                        picture = filtre.enhance(0)
                    picture = pygame.image.fromstring(picture.tobytes(), picture.size, picture.mode)
                    picture = pygame.transform.scale(picture, (icon_size, icon_size))
                    self.window.blit(picture, (int(pos[0] + icon_x + width), int(pos[1] + icon_y)))
                    if (int(pos[0] + icon_x + width) <= self.mouse[0] <= int(pos[0] + icon_x + width + icon_size) and
                        int(pos[1] + icon_y) <= self.mouse[1] <= int(pos[1] + icon_y + icon_size)):  # Active skin info
                        x = float(format(self.mouse[0] / self.screen_width, '.5f'))
                        y = float(format(self.mouse[1] / self.screen_height, '.5f'))
                        index_i, index_j = i, j

                if locked:                                                      # If skin locked
                    lock_size = int(min(size_x, size_y) * 0.5)
                    block_pos = [block_pos[0] + size_x * 0.5 - lock_size * 0.5,
                                 block_pos[1] + size_y * 0.5 - lock_size * 0.5, lock_size, lock_size]
                    self.display_icon("lock.png", block_pos)

            if x != 0 and y != 0:                                               # Draw skin info behind all skins
                skin = self.Skins[index_i]
                image = skin.PygameImages[index_j]
                percent = [x - self.skin_screen_size[0] * 0.5, y,
                           self.skin_screen_size[0], self.skin_screen_size[1]]
                skin_pos = self.display_default_box(percent)
                photo = pygame.transform.scale(image, (int(skin_pos[2] * 0.8), int(skin_pos[2] * 0.8)))
                self.window.blit(photo, (int(skin_pos[0] + skin_pos[2] * 0.1),
                                         int(skin_pos[1] + skin_pos[3] * 0.1)))
                locked = self.player.level < skin.level_unlock                  # Check if locked
                font_color = self.lock_color if locked else skin.color
                skin_name = skin.DictNames[self.FruitsName[index_j]].capitalize()
                name = self.main_font.render(f"{skin_name}", True, font_color)
                name_size = name.get_size()
                self.window.blit(name, (skin_pos[0] + skin_pos[2] * 0.5 - name_size[0] * 0.5,
                                        skin_pos[1] + skin_pos[3] * 0.7 - name_size[1] * 0.5))
                skin_class = self.present_font.render(f"{skin.name.capitalize()}", True, font_color)
                class_size = skin_class.get_size()
                self.window.blit(skin_class, (skin_pos[0] + skin_pos[2] * 0.5 - class_size[0] * 0.5,
                                              skin_pos[1] + skin_pos[3] * 0.8 - class_size[1] * 0.5))
                ed = "ed" if not locked else ""
                skin_level = self.commands_font.render(f"Unlock{ed} at level {skin.level_unlock}", True, font_color)
                level_size = skin_level.get_size()
                self.window.blit(skin_level, (skin_pos[0] + skin_pos[2] * 0.5 - level_size[0] * 0.5,
                                              skin_pos[1] + skin_pos[3] * 0.9 - level_size[1] * 0.5))

    def Display_Profile(self, menu=False):                                      # Display profile
        percent = deepcopy(self.profile_screen_percent)
        if menu:                                                                # Display on center of screen
            percent[0] = round((1 - percent[2]) / 2, 2)
            percent[1] = round((1 - percent[3]) / 2, 2)
        # Display profile background
        pos = self.display_default_box(percent)
        # Display profile title
        title = self.button_font.render(f"Profile", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display player image
        image = self.player.avatar
        image_size = int(pos[3] * 0.3)
        image_coords = (int(pos[0] + pos[2] * 0.5 - image_size * 0.5),
                     int(pos[1] + pos[3] * 0.3 - image_size * 0.5))
        image = pygame.transform.scale(image, (image_size, image_size))
        self.window.blit(image, image_coords)
        if image_coords[0] <= self.mouse[0] <= image_coords[0] + image_size and \
                image_coords[1] <= self.mouse[1] <= image_coords[1] + image_size:
            info = self.main_font.render(f"Left click to set avatar", True, self.font_color)
            info_size = info.get_size()
            info_pos = (self.mouse[0] + 10, self.mouse[1] + 10, *info_size)
            pygame.draw.rect(self.window, "lightgrey", info_pos, border_radius=int(info_pos[3] * 0.25))
            self.window.blit(info, info_pos)
            if self.click:
                self.profile = False
                self.setProto = True
        # Display player data
        pseudo = self.main_font.render(f"{self.player.pseudo}", True, self.font_color)
        pseudo_size = pseudo.get_size()
        self.window.blit(pseudo, (int(pos[0] + pos[2] * 0.5 - pseudo_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.5 - pseudo_size[1] * 0.5)))
        level = self.main_font.render(f"level {self.player.level}", True, self.font_color)
        level_size = level.get_size()
        self.window.blit(level, (int(pos[0] + pos[2] * 0.5 - level_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.7 - level_size[1] * 0.5)))
        xp = self.main_font.render(f"{self.player.xp}", True, self.font_color)
        xp_size = xp.get_size()
        self.window.blit(xp, (int(pos[0] + pos[2] * 0.2 - xp_size[0] * 0.5),
                              int(pos[1] + pos[3] * 0.8 - xp_size[1] * 0.5)))
        xp_max = self.main_font.render(f"{self.player.xp_max}", True, self.font_color)
        xp_max_size = xp_max.get_size()
        self.window.blit(xp_max, (int(pos[0] + pos[2] * 0.8 - xp_max_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.8 - xp_max_size[1] * 0.5)))
        # Display xp bar
        rect = [int(pos[0] + pos[2] * 0.25), int(pos[1] + pos[3] * 0.78),
                int(pos[2] * 0.5), int(pos[3] * 0.04)]
        pygame.draw.rect(self.window, self.bg_color, rect, 0, rect[3])
        rect[2] = int(self.player.xp / self.player.xp_max * rect[2])
        pygame.draw.rect(self.window, self.xp_bar_color, rect, 0, rect[3])
        if menu:
            button_pos = (int(pos[0] + pos[2] * 0.3), int(pos[1] + pos[3] * 0.85),
                          int(pos[2] * 0.4), int(pos[3] * 0.12))
            if self.display_button("Close", button_pos, "A"):
                self.profile = not self.profile

    def Display_Waiting_messages(self):                                         # Display waiting messages
        if len(self.Waiting_messages) > 0:
            for i, item in enumerate(self.Waiting_messages.items()):
                temps, message = item
                message_text = self.button_font.render(f"{message}", True, self.font_color)
                percent = round(1 - (self.current_time - temps) / self.message_timer_duration, 2)
                pos = message_text.get_rect(center=(self.screen_width * 0.5,
                                                    self.screen_height * 0.4 * percent))
                message_text.set_alpha(255 * (pos[1] / (self.screen_height * 0.4)) * 2)
                self.window.blit(message_text, pos)
            if self.current_time - self.message_last_timer >= self.message_timer_duration:
                self.Waiting_messages.pop(list(self.Waiting_messages.keys())[0])    # Remove first item
                self.message_last_timer = time()

    def add_message(self, message=""):                                          # Add message in Waiting messages
        self.Waiting_messages[self.current_time] = message

    def Display_Choose_Fruit(self):                                             # Choose current fruit (power)
        # Display ask background
        pos = self.display_default_box(self.choose_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Choose current fruit", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        # Display choosable fruit
        for i, fruit in enumerate(self.FruitsChoosable):
            equation = (i + 1) / (len(self.FruitsChoosable) + 1)
            fruit.pos_x = pos[0] + pos[2] * equation - fruit.radius
            fruit.pos_y = pos[1] + pos[3] * 0.5 - fruit.radius
            self.draw_reduced_fruit(fruit, (fruit.pos_x, fruit.pos_y), 1)
            if fruit.collide_point(self.mouse):                                 # If mouse on fruit
                # Display presentation of fruit
                name = self.present_font.render(f"{fruit.name.capitalize()}", True, self.font_color)
                name_size = name.get_size()
                self.window.blit(name, (int(pos[0] + pos[2] * equation - name_size[0] * 0.5),
                                        int(pos[1] + pos[3] * 0.7)))
                present = self.present_font.render(f"{fruit.present()}", True, self.font_color)
                present_size = present.get_size()
                self.window.blit(present, (int(pos[0] + pos[2] * equation - present_size[0] * 0.5),
                                           int(pos[1] + pos[3] * 0.75)))
                if self.click:                                                  # If click on fruit
                    self.current_fruit = fruit
                    self.choosing = False
            fruit.pos_x, fruit.pos_y = 0, 0                                     # Reset fruit position
        # Display command
        title = self.main_font.render(f"Left click to choose current fruit", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.9 - title_size[1] * 0.5)))

    def Display_Fruitopedia(self):                                              # Display screen with fruit data
        # Display ask background
        pos = self.display_default_box(self.fruitopedia_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Fruitopedia", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        # Display all fruit (dynamic)
        percent = 0.6
        percent *= 1.1 if self.diff_index == 0 else 1 if self.diff_index == 1 else \
            0.9 if self.diff_index == 2 else 0.8                                # Offset fruit size (based on diff)
        for i, fruit in enumerate(self.Fruits):
            equation = i ** 1.5 / (len(self.Fruits) ** 1.5) + 0.05 if i > 0 else 0.05   # Function
            fruit.pos_x = pos[0] + pos[2] * equation - fruit.radius * percent
            fruit.pos_y = pos[1] + pos[3] * 0.5 - fruit.radius * percent
            self.draw_reduced_fruit(fruit, (fruit.pos_x, fruit.pos_y), percent)
            if fruit.collide_point(self.mouse, percent):                        # Check if fruit collide
                name_text = self.SkinsDict[self.SkinsNames[self.skin_index]][fruit.name] \
                            if self.using_skin else fruit.name
                name = self.present_font.render(f"{name_text.capitalize()}", True, self.font_color)
                name_size = name.get_size()
                self.window.blit(name, (int(pos[0] + pos[2] * equation - name_size[0] * 0.5),
                                        int(pos[1] + pos[3] * 0.7)))
                present = self.present_font.render(f"{fruit.present()}", True, self.font_color)
                present_size = present.get_size()
                self.window.blit(present, (int(pos[0] + pos[2] * equation - present_size[0] * 0.5),
                                           int(pos[1] + pos[3] * 0.75)))
            fruit.pos_x, fruit.pos_y = 0, 0
        # Display buttons
        if self.display_button("Close", (int(pos[0] + pos[2] * 0.45), int(pos[1] + pos[3] * 0.82),
                                         int(pos[2] * 0.1), int(pos[3] * 0.15)), "F"):
            self.on_allF = not self.on_allF

    def Display_Gain_XP(self):
        gain = int(self.score / 100)
        if not self.as_gain:                                                    # Player gain xp (once)
            self.player.xp += gain
            self.player.level_up()
            if self.player.has_level_up:
                self.level_up_sound.play()
            self.as_gain = True
        # Display profile background
        pos = self.display_default_box(self.gain_screen_percent)
        # Display profile title
        text = "New level !" if self.player.has_level_up else "Profile"
        title = self.button_font.render(f"{text}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display player image
        image_size = self.player.avatar.get_size()
        self.window.blit(self.player.avatar, (int(pos[0] + pos[2] * 0.5 - image_size[0] * 0.5),
                                              int(pos[1] + pos[3] * 0.3 - image_size[1] * 0.5)))
        # Display player data
        pseudo = self.main_font.render(f"{self.player.pseudo}", True, self.font_color)
        pseudo_size = pseudo.get_size()
        self.window.blit(pseudo, (int(pos[0] + pos[2] * 0.5 - pseudo_size[0] * 0.5),
                                  int(pos[1] + pos[3] * 0.5 - pseudo_size[1] * 0.5)))
        level = self.main_font.render(f"level {self.player.level}", True, self.font_color)
        level_size = level.get_size()
        self.window.blit(level, (int(pos[0] + pos[2] * 0.5 - level_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.65 - level_size[1] * 0.5)))
        xp = self.main_font.render(f"+{gain} xp", True, self.font_color)
        xp_size = xp.get_size()
        self.window.blit(xp, (int(pos[0] + pos[2] * 0.5 - xp_size[0] * 0.5),
                              int(pos[1] + pos[3] * 0.75 - xp_size[1] * 0.5)))
        xp = self.main_font.render(f"{self.player.xp}", True, self.font_color)
        xp_size = xp.get_size()
        self.window.blit(xp, (int(pos[0] + pos[2] * 0.2 - xp_size[0] * 0.5),
                              int(pos[1] + pos[3] * 0.8 - xp_size[1] * 0.5)))
        xp_max = self.main_font.render(f"{self.player.xp_max}", True, self.font_color)
        xp_max_size = xp_max.get_size()
        self.window.blit(xp_max, (int(pos[0] + pos[2] * 0.8 - xp_max_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.8 - xp_max_size[1] * 0.5)))
        # Display xp bar
        rect = [int(pos[0] + pos[2] * 0.25), int(pos[1] + pos[3] * 0.78),
                int(pos[2] * 0.5), int(pos[3] * 0.04)]
        pygame.draw.rect(self.window, self.bg_color, rect, 0, rect[3])
        rect[2] = int(self.player.xp / self.player.xp_max * rect[2])
        pygame.draw.rect(self.window, self.xp_bar_color, rect, 0, rect[3])

    def Display_Lose(self):                                                     # Display lose screen
        if self.score > self.highscore and not self.beating:
            self.high_score_sound.play()                                        # Play sound
            self.add_message(f"New high score : {self.score} pts")
            self.beating = True
        # Display lose background
        pos = self.display_default_box(self.lose_screen_percent)
        # Display lose title
        title = "New high score !" if self.score > self.highscore else "You lose !"
        title_font = self.small_title_font.render(f"{title}", True, self.font_color)
        title_size = title_font.get_size()
        self.window.blit(title_font, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                      int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display lose text
        cheer = "Nice work, keep going." if self.score > self.highscore else \
                "Your fruit has protruded from the top of the bag."
        text = self.main_font.render(f"{cheer}", True, self.font_color)
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
        teaser = "Want to beat a new high score ?" if self.score > self.highscore else \
                 "Would you like to play again ?"
        text = self.main_font.render(f"{teaser}", True, self.font_color)
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
        warning = self.main_font.render(f"All progress in the game will be lost !", True, self.font_color)
        warning_size = warning.get_size()
        self.window.blit(warning, (int(pos[0] + pos[2] * 0.5 - warning_size[0] * 0.5),
                                   int(pos[1] + pos[3] * 0.4 - warning_size[1] * 0.5)))
        # Display buttons
        if self.display_button("Yes", (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.7),
                                       int(pos[2] * 0.3), int(pos[3] * 0.25)), "Y"):
            self.start_new_game()
        if self.display_button("No", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.7),
                                      int(pos[2] * 0.3), int(pos[3] * 0.25)), "N"):
            self.on_resG = not self.on_resG

    def display_default_box(self, size, bg_color=None, border_color=None,
                            width_ratio=1.0, border_ratio=1.0):                 # Used for screens and boxes
        bg_color = self.screen_color if bg_color is None else bg_color
        border_color = self.border_color if border_color is None else border_color
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        short = min(pos[2], pos[3])
        radius = int(short * 0.1 * border_ratio)
        width = int(short * self.border_ratio * width_ratio)
        pygame.draw.rect(self.window, bg_color, pos, 0, radius)
        pygame.draw.rect(self.window, border_color, pos, width, radius)

        return pos                                                              # Most screens need this

    def Display_Volume(self):                                                   # Display volume bar
        pos = [self.screen_width * 0.95, self.screen_height * 0.2,
               self.screen_height * 0.01, self.screen_height * 0.2]
        pygame.draw.rect(self.window, "orange", pos, 0, int(pos[2]))
        pos[1] = pos[1] + (1 - self.volume) * pos[3]                            # Adapt to volume
        pos[3] = pos[3] * self.volume
        if self.is_mute and self.volume > 0:
            glassed_gold = pygame.surface.Surface((pos[2], pos[3]), pygame.SRCALPHA)
            pygame.draw.rect(glassed_gold, pygame.Color(255, 215, 0, 128), (0, 0, pos[2], pos[3]), 0, int(pos[2]))
            self.window.blit(glassed_gold, (pos[0], pos[1]))
        else:
            pygame.draw.rect(self.window, "gold", pos, 0, int(pos[2]))
        # Display command
        command = self.main_font.render(f"[M]", True, self.font_color)
        command_size = command.get_size()
        self.window.blit(command, (int(pos[0] + pos[2] + command_size[0] * 0.25),
                                   int(pos[1] - command_size[1] * 0.5)))

    def Display_Set_Avatar(self):                                               # Set player pseudo and avatar
        # Display bg image
        self.window.blit(self.bg_image, (0, 0))
        percent = self.set_avatar_screen_percent
        # Display avatar background
        avatar = (percent[0], percent[1], self.avatar_screen_size[0], self.avatar_screen_size[1])
        posA = self.display_default_box(avatar)
        # Display avatar title
        title = self.button_font.render(f"Personnalize your avatar", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(posA[0] + posA[2] * 0.5 - title_size[0] * 0.5),
                                 int(posA[1] + posA[3] * 0.1 - title_size[1] * 0.5)))
        image = self.player.proto.resize((int(posA[2] * 0.6), int(posA[2] * 0.6)))
        if type(image) != pygame.surface.Surface:
            image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        self.window.blit(image, (int(posA[0] + posA[2] * 0.2), int(posA[1] + posA[3] * 0.25)))
        pseudo = self.button_font.render(f"{self.player.pseudo}", True, self.font_color)
        pseudo_size = pseudo.get_size()
        pseudo_pos = (int(posA[0] + posA[2] * 0.5 - pseudo_size[0] * 0.5),
                      int(posA[1] + posA[3] * 0.9 - pseudo_size[1] * 0.5))
        self.window.blit(pseudo, pseudo_pos)

        if self.on_keys:                                                        # Draw cursor
            cursor = self.button_font.render(f"{self.player.pseudo[:self.key_index]}", True, self.font_color)
            cursor_size = cursor.get_size()
            pygame.draw.line(self.window, self.font_color, (int(pseudo_pos[0] + cursor_size[0]), pseudo_pos[1]),
                             (int(pseudo_pos[0] + cursor_size[0]), pseudo_pos[1] + cursor_size[1]), 3)
        # Display faces background
        height = round(1 - avatar[1] * 2 - avatar[3] - self.gap_avatar_screen, 2)
        faces = (avatar[0], avatar[1] + avatar[3] + self.gap_avatar_screen, avatar[2], height)
        posF = self.display_default_box(faces, width_ratio=1.8, border_ratio=1.7)
        # Display commands / faces title
        gap = 5
        text = "Commands" if self.on_keys else "Faces"
        title = self.button_font.render(f"{text}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(posF[0] + posF[2] * 0.5 - title_size[0] * 0.5),
                                 int(posF[1] + posF[3] * 0.1 - title_size[1] * 0.5)))
        if self.on_keys:                                                        # If setting pseudo
            specials = ""
            for c in self.AuthorizedChars:
                specials += c if c == self.AuthorizedChars[-1] else f"{c}, "
            Commands = ["LEFT / RIGHT ARROW - Move cursor", "BACKSPACE - Remove letter at left of cursor",
                        "RETURN - Valid current pseudonyme", f"Specials allowed : {specials}",
                        "Save your pseudo to load your account",
                        f"Pseudo is {self.pseudo_lenght_min} characters minimum"]
            for i, command_text in enumerate(Commands):
                command = self.main_font.render(f"{command_text}", True, self.font_color)
                command.set_alpha(128)
                command_size = command.get_size()
                self.window.blit(command, (int(posF[0] + posF[2] * 0.05),
                                           int(posF[1] + posF[3] * 0.25 + i * command_size[1])))
        else:
            by_column = 4
            by_line = 6
            face_size = int(posF[3] * 0.8 / by_column)
            for i, face in enumerate(self.Faces):                               # Draw faces
                if i >= by_column * by_line:
                    break
                x = int(posF[0] + posF[2] * 0.12 + (i % by_line) * face_size * 1.2)
                y = int(posF[1] + posF[3] * 0.2 + int(i / by_line) * face_size)
                if self.player.face == face:                                    # If current face
                    select_pos = (x - gap, y - gap, face.size[0] + gap * 2, face.size[1] + gap * 2)
                    pygame.draw.rect(self.window, self.face_bg_color, select_pos,
                                     border_radius=int(face_size * 0.25))
                image = pygame.image.fromstring(face.tobytes(), face.size, face.mode)
                self.window.blit(image, (x, y))
                if self.click and x <= self.mouse[0] <= x + face_size and \
                        y <= self.mouse[1] <= y + face_size:                    # If select face
                    if self.current_time - self.click_last_timer >= self.click_timer_duration:
                        self.player.face = None if self.player.face == face else face
                        self.player.set_proto()
                        self.click_last_timer = time()
        # Display skins background
        skins = (avatar[0] + avatar[2] + self.gap_avatar_screen * 0.6, avatar[1],
                 round(1 - avatar[0] * 2 - avatar[2] - self.gap_avatar_screen * 0.6, 2), percent[3])
        posK = self.display_default_box(skins, width_ratio=0.6, border_ratio=0.5)
        # Display skins title
        title = self.button_font.render(f"Skins", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(posK[0] + posK[2] * 0.5 - title_size[0] * 0.5),
                                 int(posK[1] + posK[3] * 0.05)))
        # Display commands
        command = self.main_font.render(f"Click on skin to select bg avatar", True, self.font_color)
        command.set_alpha(128)
        command_size = command.get_size()
        self.window.blit(command, (int(posK[0] + posK[2] * 0.62), int(posK[1] + posK[3] * 0.05)))
        command = self.main_font.render(f"Click on face to (un)select avatar face", True, self.font_color)
        command.set_alpha(128)
        self.window.blit(command, (int(posK[0] + posK[2] * 0.62), int(posK[1] + posK[3] * 0.05 + command_size[1])))
        # Display skins
        by_column = len(self.Skins)
        by_line = len(self.Fruits)
        skin_size = int(posK[2] * 0.7 / by_line)
        for i, skin in enumerate(self.Skins):
            if i >= by_column * by_line:
                break
            for j, image in enumerate(skin.Images):
                x = int(posK[0] + posK[2] * 0.1 + (j % by_line) * skin_size * 1.2)
                y = int(posK[1] + posK[3] * 0.15 + (i % by_column) * skin_size * 1.2)
                if self.player.skin == image:                                   # If current skin
                    select_pos = (x - gap, y - gap, skin_size + gap * 2, skin_size + gap * 2)
                    pygame.draw.rect(self.window, self.face_bg_color, select_pos,
                                     border_radius=int(skin_size * 0.25))
                pic = pygame.transform.scale(skin.PygameImages[j], (skin_size, skin_size))
                self.window.blit(pic, (x, y))
                if self.click and x <= self.mouse[0] <= x + skin_size and \
                        y <= self.mouse[1] <= y + skin_size:                    # If select skin
                    self.player.skin = image
                    self.player.set_proto()
        # Check if pseudo valid
        check = self.player.pseudo.lower()
        self.player.pseudo_is_valid = False if (check == "player" or
            check == self.creator_pseudo.lower() or len(check) < self.pseudo_lenght_min) else True
        # Display buttons
        button_size = [int(self.screen_width * 0.1), int(self.screen_height * 0.08)]
        prop = 0.7                                                              # Proportion (button size)
        random_pos = (int(posK[0] + posK[2] * 0.1), int(posK[1] + posK[3] * 0.05),
                      int(button_size[0] * prop), int(button_size[1] * prop))
        if self.display_button("Random", random_pos):
            skin = choice(self.Skins)
            self.player.skin = choice(skin.Images)
            self.player.face = choice(self.Faces)
            self.player.set_proto()
        if self.display_button("Save", (int(self.screen_width * 0.3),
                int(self.screen_height * 0.91), *button_size), "S", not self.on_keys):
            if self.player.pseudo_is_valid:
                self.player.valid_proto()
                self.Load_player_data()
                self.setProto = False
            else:
                if len(self.player.pseudo) < self.pseudo_lenght_min:
                    self.add_message(f"Pseudonyme must have at least a length of "
                                     f"{self.pseudo_lenght_min} characters !")
                else:
                    self.add_message(f"'{self.player.pseudo}' isn't a valid pseudonyme !")
        if self.display_button("Close", (int(self.screen_width * 0.7 - button_size[0]),
                 int(self.screen_height * 0.91), *button_size), "RETURN", not self.on_keys):
            self.setProto = False
        # Display info on pseudo (in front of the rest)
        if pseudo_pos[0] - 10 <= self.mouse[0] <= pseudo_pos[0] + pseudo_size[0] + 10 and \
                pseudo_pos[1] <= self.mouse[1] <= pseudo_pos[1] + pseudo_size[1] and not self.on_keys:
            info = self.main_font.render(f"Left click to set pseudo", True, self.font_color)
            info_size = info.get_size()
            info_pos = (self.mouse[0] + 10, self.mouse[1] + 10, *info_size)
            pygame.draw.rect(self.window, "lightgrey", info_pos, border_radius=int(info_pos[3] * 0.25))
            self.window.blit(info, info_pos)
            if self.click:
                self.on_keys = True

    def Keyboard_Manager(self, event):                                          # Set player pseudo
        pseudo = self.player.pseudo
        char = event.dict['unicode']                                            # Get character
        place = 0 if self.key_index - 1 < 0 else self.key_index
        if event.key == pygame.K_BACKSPACE:                                     # Remove letter
            mini = 0 if self.key_index - 1 < 0 else self.key_index - 1
            pseudo = pseudo[:mini] + pseudo[self.key_index:]
            self.key_index -= 1
        elif event.key == pygame.K_LEFT:                                        # Move cursor
            self.key_index -= 1
        elif event.key == pygame.K_RIGHT:                                       # //
            self.key_index += 1
        elif char != "" and (char in self.Alphabet or char in self.AuthorizedChars):
            if len(pseudo) < self.pseudo_lenght_max:
                if self.pressed[pygame.K_LSHIFT] or self.pressed[pygame.K_RSHIFT]:  # Uppercase
                    char = char.upper()
                pseudo = pseudo[:place] + char + pseudo[place:]
                self.key_index += 1
        elif char.isdigit() and int(char) in self.Numbers:                      # Enter integer
            if len(pseudo) < self.pseudo_lenght_max:
                pseudo = pseudo[:place] + char + pseudo[place:]
                self.key_index += 1
        elif event.key == pygame.K_RETURN:                                      # Valid pseudo
            self.on_keys = False

        # Set values
        self.key_index = 0 if self.key_index < 0 else len(pseudo) \
                         if self.key_index > len(pseudo) else self.key_index
        self.player.pseudo = pseudo

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

    def change_skin(self):                                                      # Change all skins
        if self.using_skin:
            if self.skin_index is None:
                for i, level in enumerate(self.SkinsLevel):
                    if self.player.level >= level:
                        self.skin_index = i
                else:                                                           # If player levels too low
                    self.using_skin = False
                    self.add_message("No skins available for you yet")
        else:
            self.skin_index = None

        # Update fruits image spread all over the game
        place = self.FruitsName.index(self.next_fruit.name)
        skin_image = None if not self.using_skin else \
                     self.Skins[self.skin_index].Images[place]
        self.next_fruit.set_image(skin_image, False)                            # No bg for next fruit
        for fruit in self.Fruits:
            skin_image = None
            if self.using_skin:
                place = self.FruitsName.index(fruit.name)
                skin_image = self.Skins[self.skin_index].Images[place]
            fruit.set_image(skin_image, self.using_bg)
            if self.current_fruit.name == fruit.name:
                self.current_fruit.image = fruit.image
            for panier in self.Panier.sprites():
                if panier.name == fruit.name:
                    panier.image = fruit.image

    def start_new_game(self):                                                   # Reset game
        self.pausing = False
        self.beating = False
        self.powering = False
        self.choosing = False
        self.on_menu = False
        self.on_game = True
        self.on_lose = False
        self.on_back = False
        self.on_resG = False
        self.on_allF = False
        self.as_gain = False

        if self.score > self.highscore:                                         # Update highscore
            self.highscore = self.score

        self.create_physics_space()
        self.create_fruits()
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

        self.Panier.empty()
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
        self.Scoreboard = list(set(self.Scoreboard))                            # Remove duplicates
        if self.score > 0 and self.score not in self.Scoreboard and \
                len(self.Scoreboard) < self.nb_score_saved_max:
            self.Scoreboard.append(self.score)
        self.Scoreboard.sort()
        self.Scoreboard.reverse()
        while len(self.Scoreboard) > self.nb_score_saved_max:                   # If too much score, delete lowest
            self.Scoreboard.pop(-1)

        file = open("scores/save.txt", "w")
        for score in self.Scoreboard:                                           # Save all not null score
            if score > 0:
                file.write(f"{score}\n")
        file.close()

    def Load_scores(self):                                                      # Load current score
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

    def Save_player_data(self):
        if self.player.pseudo_is_valid and self.player.proto_is_valid:          # If pseudo and avatar valid
            if not os.path.exists(f"players/{self.player.pseudo}"):             # If dir not exists
                os.mkdir(f"{self.path}/players/{self.player.pseudo}")           # Create dir
            file = open(f"players/{self.player.pseudo}/data.txt", "w")
            file.write(f"{self.player.level}\n")
            file.write(f"{self.player.xp}\n")
            file.write(f"{self.player.xp_max}\n")
            file.close()
            pygame.image.save(self.player.avatar, f"players/{self.player.pseudo}/avatar.png")
            self.player.skin.save(f"players/{self.player.pseudo}/skin.png")
            if self.player.face:                                                # Face is optional
                self.player.face.save(f"players/{self.player.pseudo}/face.png")
            self.add_message("Account successfully loaded !")

    def Load_player_data(self):
        if os.path.exists(f"players/{self.player.pseudo}/data.txt"):            # Check if player exists
            print("Loading player data...")
            file = open(f"players/{self.player.pseudo}/data.txt", "r")
            lines = file.readlines()
            if lines:
                self.player.level = int(lines[0])
                self.player.xp = int(lines[1])
                self.player.xp_max = int(lines[2])
            file.close()
            self.player.level_up()                                              # Just in case
            self.player.avatar = pygame.image.load(f"players/{self.player.pseudo}/avatar.png")
            self.player.skin = Image.open(f"{self.path}/players/{self.player.pseudo}/skin.png")
            if os.path.exists(f"players/{self.player.pseudo}/face.png"):
                self.player.face = Image.open(f"{self.path}/players/{self.player.pseudo}/face.png")
            self.player.set_proto()
            self.player.pseudo_is_valid = True
            self.player.proto_is_valid = True

    def Close_Game(self):                                                       # Close game
        self.Save_player_data()
        if self.save_score:
            self.Save_scores()
        print("Closing game...")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    jeu = Game(random_music=True)
