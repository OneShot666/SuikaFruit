from math import pi
from random import choice
from time import time
from os import getcwd, listdir
from fruit import Fruit
from data import *
import pygame
import sys

""" Documentation
creator : One Shot
name : Suika Fruit
year of creation : 2023
version : 0.2.0
language : python
purpose : Small game where you can merge fruit to get score. The bigger the fruit, the higher the score.
          Any resemblance to an existing game would be coincidental.
          All arguments are optionnal.
arguments : (3)
    - difficulty_index : Default value = 1. Informs about the difficulty level of the game.
    - random_music : Default value = True. By default, choose one random music. If False, choose real game music.
    - fruit_image : Default value = False. By default, fruits are circles. If False, fruits are images.
requirements : libraries 'pygame', 'math', 'random', 'time' and 'sys'.
"""


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
# [v0.2.1] : Make all parameters work + can select with mouse + save with key 's'
# [v0.2.2] : Make all buttons work + fix 'save score' problem (saving score multiples times)
# [v0.2.3] : Add powers (cost score) : pop fruit / sort basket / make fruit smaller and heavier
# [v0.2.4] : Upgrade physics + balance score + make score when fruit merge
# [v0.2.5] : Change lost screen if high score beaten and update + make changing volume fluid
# [v0.2.6] : On menu, make random fruits roll on the background
class Game:                                                                     # Manage all game
    def __init__(self, difficulty_index=1, random_music=True, fruit_image=False):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        # Main data
        self.creator = "One Shot"
        self.version = "v0.2.0"
        self.game_name = "Suika Fruit"
        # Boolean data
        self.running = True
        self.loading = False                                                    # ! [later] For loading screen
        self.pausing = False
        self.helping = False                                                    # For help line
        self.playing = True                                                     # For loading music
        self.on_menu = True
        self.on_game = False
        self.on_lose = False
        self.on_help = False                                                    # For help note
        self.on_para = False                                                    # For parameters
        self.on_back = False                                                    # Ask for back menu (security)
        self.on_allF = False                                                    # For Fruitopedia
        self.on_mute = False
        # Game data
        self.path = getcwd()                                                    # Get actual position of files
        self.pressed = pygame.key.get_pressed()                                 # Pressed keys
        self.horloge = pygame.time.Clock()                                      # Manage the fps
        self.fps = 60
        # Screen data
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
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
        # Screens, screen border and tips data
        self.ask_screen_percent = [0.35, 0.35, 0.3, 0.3]
        self.lose_screen_percent = [0.3, 0.1, 0.4, 0.8]                         # Also used for help screen
        self.all_fruits_screen_percent = [0.1, 0.25, 0.8, 0.5]
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
        self.ParametersPercent = [(0.2, 0.25), (0.2, 0.55), (0.6, 0.25),        # ! Use later
                                  (0.6, 0.55)]
        self.select_param_color = self.border_color                             # ! Keep to change later ?
        self.select_param_index = 0
        # Difficulty data
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
        self.merging_fruit_start_timer = time()
        self.merging_fruit_last_timer = None
        self.merging_fruit_timer_duration = 0.1
        # Score data
        self.score = 0
        self.highscore = 0
        self.Scoreboard = []
        self.score_box_percent = [0.08, 0.25, 0.15, 0.15]
        self.score_box_color = (255, 200, 90)
        # Evolution of fruit box data
        self.evolution_box_percent = [0.06, 0.53, 0.19, 0.32]
        self.evolution_box_color = (255, 250, 140)
        # Current and next fruit data
        self.current_fruit = None
        self.next_fruit_box_percent = [0.8, 0.21, 0.1, 0.18]
        self.next_fruit_box_color = (255, 250, 140)
        self.next_fruit = None
        self.next_fruit_start_timer = time()
        self.next_fruit_last_timer = None
        self.next_fruit_timer_duration = 0.25
        # Commands and helping player data
        self.commands_box_percent = [0.775, 0.55, 0.15, 0.3]
        self.commands_box_color = (240, 210, 115)
        self.help_line_color = (255, 255, 220, 160)
        self.help_line_width = 5
        # Pause data
        self.paused_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.rect(self.paused_glass, (255, 255, 255), self.paused_glass.get_rect())
        self.paused_glass.set_alpha(120)
        # Icon data
        self.icon = pygame.image.load("images/icon.png")
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
        self.gap = 0.05
        # Main function
        self.run()

    def create_fruits(self):                                                    # Load fruits
        percent = 55 if self.diff_index == 0 else 50 if self.diff_index == 1 else \
                  45 if self.diff_index == 2 else 40
        size = int(self.screen_width * self.main_box_percent[2] / percent)      # Get fruit size (dynamic)
        cerise =    Fruit(self.FruitsName[0],  (240, 0, 0),     size * 1, 11, 2, self.fruit_image)
        fraise =    Fruit(self.FruitsName[1],  (255, 140, 160), size * 2, 10, 4, self.fruit_image)
        raisin =    Fruit(self.FruitsName[2],  (195, 75, 255),  size * 3,  9, 8, self.fruit_image)
        clement =   Fruit(self.FruitsName[3],  (255, 210, 40),  size * 4,  8, 16, self.fruit_image)
        orange =    Fruit(self.FruitsName[4],  (255, 145, 45),  size * 5,  7, 32, self.fruit_image)
        pomme =     Fruit(self.FruitsName[5],  (250, 20, 20),   size * 6,  6, 64, self.fruit_image)
        poire =     Fruit(self.FruitsName[6],  (255, 240, 105), size * 7,  5, 128, self.fruit_image)
        peche =     Fruit(self.FruitsName[7],  (255, 190, 235), size * 8,  4, 256, self.fruit_image)
        ananas =    Fruit(self.FruitsName[8],  (255, 250, 30),  size * 9,  3, 512, self.fruit_image)
        melon =     Fruit(self.FruitsName[9],  (160, 250, 70),  size * 10, 2, 1024, self.fruit_image)
        pasteque =  Fruit(self.FruitsName[10], (60, 210, 25),   size * 11, 1, 2048, self.fruit_image)
        self.Fruits = [cerise, fraise, raisin, clement, orange, pomme, poire, peche, ananas, melon, pasteque]
        nb = 4 if self.diff_index == 3 else 5
        self.FruitsChoosable = self.Fruits[:nb]                                 # Can drop 5 firsts fruits

        self.Panier.empty()
        self.current_fruit = choice(self.FruitsChoosable)
        self.next_fruit = choice(self.FruitsChoosable)

    def run(self):                                                              # Main fonction of game
        self.loading = True
        self.create_fruits()
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

            pygame.display.flip()
            self.horloge.tick(self.fps)

    def Update_Manager(self):
        self.Panier.update()                                                    # Update all fruits

    def Collision_Manager(self):                                                # Manage collisions
        for index_f, fruit in enumerate(self.Panier.sprites()):
            for index_o, other in enumerate(self.Panier.sprites()):             # Provide fruits to collide each other
                # If fruit merge
                if fruit != other and fruit.collide_circle(other, self.diff_index) and fruit.name == other.name:
                    self.merging_fruit_last_timer = time()
                    if self.merging_fruit_last_timer - self.merging_fruit_start_timer >= self.merging_fruit_timer_duration:
                        pos = int(self.FruitsName.index(fruit.name) + 1)
                        if pos > len(self.Fruits) - 1:                          # If bigger fruit merge
                            self.Panier.remove(fruit)
                            self.Panier.remove(other)
                        else:                                                   # Normally merging same fruit
                            coords = [(fruit.rect.x + other.rect.x) / 2, (fruit.rect.y + other.rect.y) / 2]
                            vel = [(fruit.vel_x + other.vel_x) / 2, (fruit.vel_y + other.vel_y) / 2]
                            self.Panier.remove(fruit)
                            self.Panier.remove(other)

                            next_f = self.Fruits[pos]                           # Make spawn bigger fruit
                            bigger = Fruit(next_f.name, next_f.color, next_f.radius,
                                           next_f.weight, next_f.score, self.fruit_image)
                            bigger.rect.x, bigger.rect.y = coords
                            bigger.vel_x, bigger.vel_y = vel
                            self.Panier.add(bigger)
                        self.merging_fruit_start_timer = time()

            # Prevent fruits to exit box
            if fruit.rect.left <= self.box_pos[0] + self.main_box_width:
                fruit.rect.left = self.box_pos[0] + self.main_box_width
                fruit.vel_x *= -1 * bounce                                      # Make small bounce against box
            elif fruit.rect.right >= self.box_pos[0] + self.box_pos[2] - self.main_box_width:
                fruit.rect.right = self.box_pos[0] + self.box_pos[2] - self.main_box_width
                fruit.vel_x *= -1 * bounce                                      # //
            if fruit.rect.bottom >= self.box_pos[1] + self.box_pos[3] - self.main_box_width:
                fruit.rect.bottom = self.box_pos[1] + self.box_pos[3] - self.main_box_width
                fruit.vel_y = 0

            # Prevents fruits to exit box (possible ?)
            if fruit.rect.left <= 0:
                fruit.rect.left = 0
                fruit.vel_x *= -1 * bounce                                      # Make slow bounce against walls
            elif fruit.rect.right >= self.screen_width:
                fruit.rect.right = self.screen_width
                fruit.vel_x *= -1 * bounce                                      # //
            if fruit.rect.top < 0:                                              # If fruit exit window, player lose
                self.on_lose = True
            if fruit.rect.bottom >= self.screen_height:
                fruit.rect.bottom = self.screen_height
                fruit.vel_y = 0

    def Check_Lose(self):                                                       # Check if fruit out main box
        for fruit in self.Panier.sprites():
            if fruit.rect.bottom < self.box_pos[1] and abs(fruit.vel_y) < 1:
                self.on_lose = True
                self.Scoreboard.append(self.score)
                break

    def Inputs_Manager(self):                                                   # Manage all inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Close_Game()

            if self.on_menu:                                                    # If on menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:                            # Start new game
                        self.start_new_game()

                    if not self.on_para and event.key == pygame.K_h:            # For help note
                        self.on_help = not self.on_help

                    if not self.on_help and event.key == pygame.K_p:            # For parameters
                        self.on_para = not self.on_para

                    if self.on_para:
                        if event.key == pygame.K_s:                             # [! later] Save params
                            self.on_para = False
            elif self.on_game:                                                  # If on game
                if self.on_lose:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:                        # Go to menu
                            self.go_to_menu()

                        if event.key == pygame.K_SPACE:                         # Restart a game
                            self.start_new_game()
                elif self.on_back:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:                             # Go back to menu
                            self.go_to_menu()
                        elif event.key == pygame.K_n:                           # Continue game
                            self.on_back = False
                else:
                    if (not self.pausing and not self.on_allF
                        and event.type == pygame.MOUSEBUTTONDOWN):              # Drop current fruit
                        self.drop_fruit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:                        # Want to quit game
                            if len(self.Panier.sprites()) > 0:                  # If game started, ask first
                                self.on_back = True
                                self.pausing = False
                            else:
                                self.go_to_menu()                               # Exit current game

                        if event.key == pygame.K_SPACE:                         # For pause
                            self.pausing = not self.pausing

                        if event.key == pygame.K_h and not self.pausing:        # For help line
                            self.helping = not self.helping

                        if event.key == pygame.K_f and not self.pausing:        # For fruitopedia
                            self.on_allF = not self.on_allF

                        if event.key == pygame.K_r and self.pausing:            # Restart game
                            self.start_new_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:                                     # (un)mute music
                    self.on_mute = not self.on_mute

                if event.key == pygame.K_UP:                                    # Change volume music
                    self.volume += self.gap
                elif event.key == pygame.K_DOWN:
                    self.volume -= self.gap

        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_q] or self.pressed[pygame.K_ESCAPE]:           # Quit programm
            self.Close_Game()

    def drop_fruit(self):                                                       # Drop current fruit
        self.next_fruit_last_timer = time()                                     # Check timer
        if self.next_fruit_last_timer - self.next_fruit_start_timer >= self.next_fruit_timer_duration:
            fruit = Fruit(self.current_fruit.name, self.current_fruit.color, self.current_fruit.radius,
                          self.current_fruit.weight, self.current_fruit.score, self.fruit_image)
            fruit.rect.x = self.current_fruit.rect.x                            # Place fruit
            fruit.rect.y = self.current_fruit.rect.y
            self.Panier.add(fruit)
            self.current_fruit = self.next_fruit                                # Replace current fruit
            self.next_fruit = choice(self.FruitsChoosable)                      # Change next fruit
            self.score += fruit.score                                           # ! Move score when fruit merge
            self.next_fruit_start_timer = time()

    def Display_Manager(self):                                                  # Manage all things to draw
        if self.on_menu:
            self.Display_Menu()
        elif self.on_game:
            self.Display_Game()
        self.Display_Volume()

    def Display_Menu(self):                                                     # Display main menu
        # self.window.fill(self.bg_color)
        self.window.blit(self.bg_image, (0, 0))

        self.display_title()

        # Display main buttons
        self.display_button("Play", (int(self.screen_width * 0.425), int(self.screen_height * 0.4),
                                     int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "RETURN")
        self.display_button("Help", (int(self.screen_width * 0.425), int(self.screen_height * 0.51),
                                     int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "H")
        self.display_button("Parameters", (int(self.screen_width * 0.425), int(self.screen_height * 0.62),
                                           int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "P")
        self.display_button("Quit", (int(self.screen_width * 0.425), int(self.screen_height * 0.73),
                                     int(self.screen_width * 0.15), int(self.screen_height * 0.09)), "Q")

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

    def display_button(self, name, pos, command=""):                            # Display all button in programm
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
        self.display_button("Menu", (int(pos[0] + pos[2] * 0.4), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "H")

    def Display_Parameters(self):                                               # Display parameters screen
        # Display parameters background
        pos = self.display_default_box(self.parameters_screen_percent)
        # Display parameters title
        title = self.small_title_font.render(f"Parameters", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display parameters text
        screen = self.button_font.render(f"Screen : ", True, self.font_color)
        self.window.blit(screen, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.25)))
        screen_1 = self.main_font.render(f"Fullscreen", True, self.font_color)
        self.window.blit(screen_1, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.35)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.25), int(pos[1] + pos[3] * 0.35)), True)      # Checkbox
        screen_2 = self.main_font.render(f"Luminosité", True, self.font_color)
        self.window.blit(screen_2, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.4)))
        self.display_gradient_bar((pos[0] + pos[2] * 0.25, pos[1] + pos[3] * 0.42), selected=3)
        screen_3 = self.main_font.render(f"Gamma", True, self.font_color)
        self.window.blit(screen_3, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.45)))
        self.display_gradient_bar((pos[0] + pos[2] * 0.25, pos[1] + pos[3] * 0.47), selected=3)

        sound = self.button_font.render(f"Gameplay : ", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.55)))
        sound = self.main_font.render(f"Auto save score", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.65)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.3), int(pos[1] + pos[3] * 0.65)), True)      # Checkbox
        sound = self.main_font.render(f"Auto restart game", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.7)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.3), int(pos[1] + pos[3] * 0.7)))             # Checkbox
        sound = self.main_font.render(f"Auto collect cookies", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.75)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.3), int(pos[1] + pos[3] * 0.75)), True)      # Checkbox
        sound = self.main_font.render(f"Show scoreboard", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.35), int(pos[1] + pos[3] * 0.65)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.48), int(pos[1] + pos[3] * 0.65)), True)     # Checkbox
        sound = self.main_font.render(f"Show next fruit", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.35), int(pos[1] + pos[3] * 0.7)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.48), int(pos[1] + pos[3] * 0.7)), True)      # Checkbox
        sound = self.main_font.render(f"Show help line", True, self.font_color)
        self.window.blit(sound, (int(pos[0] + pos[2] * 0.35), int(pos[1] + pos[3] * 0.75)))
        self.display_checkbox((int(pos[0] + pos[2] * 0.48), int(pos[1] + pos[3] * 0.75)), self.helping)  # Checkbox

        diff = self.button_font.render(f"Difficulty : ", True, self.font_color)
        self.window.blit(diff, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.25)))
        for i, diff in enumerate(self.Difficulties):
            diff_text = self.main_font.render(f"{diff}", True, self.font_color)
            diff_coords = (int(pos[0] + pos[2] * (0.55 + i * 0.08)), int(pos[1] + pos[3] * 0.35))
            self.window.blit(diff_text, diff_coords)
            if self.diff_index == i:
                diff_size = diff_text.get_size()
                select_pos = (int(diff_coords[0] - diff_size[0] * 0.15), int(diff_coords[1] - diff_size[1] * 0.1),
                              int(diff_size[0] * 1.3), int(diff_size[1] * 1.3))
                pygame.draw.rect(self.window, self.font_color, select_pos, 3, 5)

        music = self.button_font.render(f"Musics & Sounds : ", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.55)))
        music = self.main_font.render(f"Endless music", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.65)))
        endless = True if self.repeat == -1 else False
        self.display_checkbox((int(pos[0] + pos[2] * 0.66), int(pos[1] + pos[3] * 0.65)), endless)   # Checkbox
        music = self.main_font.render(f"Volume", True, self.font_color)
        self.window.blit(music, (int(pos[0] + pos[2] * 0.55), int(pos[1] + pos[3] * 0.7)))
        self.display_gradient_bar((pos[0] + pos[2] * 0.66, pos[1] + pos[3] * 0.72),
                                  gradient=11, selected=int(self.volume * 10 + 1))
        # Display selected parameter [en cours]
        short = min(pos[2], pos[3])
        width = int(short * self.border_ratio)
        pygame.draw.rect(self.window, self.select_param_color, (0, 0, 0, 0), width)
        # Display buttons
        self.display_button("Save", (int(pos[0] + pos[2] * 0.2), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "S")
        self.display_button("Menu", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "P")

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

    def display_gradient_bar(self, coords, lenght=0, gradient=5, selected=1):   # For parameters
        lenght = int(self.screen_width * 0.15) if lenght == 0 else lenght
        width = int(self.screen_height * 0.003)
        pygame.draw.line(self.window, self.font_color, coords, (coords[0] + lenght, coords[1]), width)
        height = self.screen_height * 0.01
        for i in range(gradient):                                               # Display gradient
            size = i / (gradient - 1) * lenght
            pygame.draw.line(self.window, self.font_color, (int(coords[0] + size), int(coords[1] - height * 0.5)),
                             (int(coords[0] + size), int(coords[1] + height * 0.5)), width)
            if (selected - 1) == i:                                             # ! Change selected for percent
                points = [(int(coords[0] + size), int(coords[1] - height * 1.2)),
                          (int(coords[0] + size + height * 1.2), int(coords[1])),
                          (int(coords[0] + size), int(coords[1] + height * 1.2)),
                          (int(coords[0] + size - height * 1.2), int(coords[1]))]
                pygame.draw.polygon(self.window, self.font_color, points, width)

    def Display_Game(self):                                                     # Display game
        # self.window.fill(self.bg_color)
        self.window.blit(self.bg_image, (0, 0))

        self.display_small_title()

        self.display_main_box()                                                 # Main box for fruits
        self.display_evolution()
        self.display_next_fruit()
        self.display_commands()

        # Draw current fruit based on mouse position
        if not self.pausing:
            mouse = pygame.mouse.get_pos()
            self.current_fruit.rect.x = mouse[0] - self.current_fruit.radius
            min_b = self.screen_width * self.main_box_percent[0] + self.main_box_width
            max_b = (min_b + self.screen_width * self.main_box_percent[2] -
                     (self.main_box_width + self.current_fruit.radius) * 2)
            self.current_fruit.rect.x = min_b if self.current_fruit.rect.x < min_b else max_b \
                                        if self.current_fruit.rect.x > max_b else self.current_fruit.rect.x
        self.current_fruit.rect.y = self.screen_height * 0.1 - self.current_fruit.radius
        self.current_fruit.draw(self.window)

        if self.helping:                                                        # Line beyond fruits
            self.display_help_line()

        self.Panier.draw(self.window)                                           # Display all fruits

        self.display_highscore()                                                # In front of line

        if self.on_allF:
            self.Display_Fruitopedia()

        if self.on_lose:
            self.Display_Lose()

        if self.on_back:
            self.ask_back_menu()

        if self.pausing:                                                        # Pause screen on foreground
            self.display_pause_screen()

    def display_small_title(self):                                              # Display small game name
        title = self.small_title_font.render(f"{self.game_name}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(self.screen_width * 0.5 - title_size[0] * 0.5),
                                 int(self.screen_height * 0.1 - title_size[1] * 0.5)))

    def display_main_box(self):                                                 # Display main box for fruits
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
        # pygame.draw.circle(self.window, "black", (pos[0] + pos[2] * 0.5, pos[1] + pos[3] * 0.55), 90, 2)
        self.draw_reduced_fruit(self.Fruits[0], (pos[0] + pos[2] * 0.49, pos[1] + pos[3] * 0.216))
        self.draw_reduced_fruit(self.Fruits[1], (pos[0] + pos[2] * 0.54, pos[1] + pos[3] * 0.21))
        self.draw_reduced_fruit(self.Fruits[2], (pos[0] + pos[2] * 0.6, pos[1] + pos[3] * 0.22))
        self.draw_reduced_fruit(self.Fruits[3], (pos[0] + pos[2] * 0.675, pos[1] + pos[3] * 0.275))
        self.draw_reduced_fruit(self.Fruits[4], (pos[0] + pos[2] * 0.73, pos[1] + pos[3] * 0.38))
        self.draw_reduced_fruit(self.Fruits[5], (pos[0] + pos[2] * 0.72, pos[1] + pos[3] * 0.53))
        self.draw_reduced_fruit(self.Fruits[6], (pos[0] + pos[2] * 0.63, pos[1] + pos[3] * 0.69))
        self.draw_reduced_fruit(self.Fruits[7], (pos[0] + pos[2] * 0.44, pos[1] + pos[3] * 0.76))
        self.draw_reduced_fruit(self.Fruits[8], (pos[0] + pos[2] * 0.21, pos[1] + pos[3] * 0.68))
        self.draw_reduced_fruit(self.Fruits[9], (pos[0] + pos[2] * 0.09, pos[1] + pos[3] * 0.43))
        self.draw_reduced_fruit(self.Fruits[10], (pos[0] + pos[2] * 0.21, pos[1] + pos[3] * 0.17))

    def draw_reduced_fruit(self, fruit, pos, percent=1 / 3):                    # Use to draw one reduced fruit
        radius = fruit.radius * percent
        copy = fruit.image
        copy = pygame.transform.scale(copy, (radius * 2, radius * 2))
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
        image = self.next_fruit.image
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
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.3)))
        text = "Show" if not self.helping else "Hide"
        command_text = self.main_font.render(f"H - {text} line", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.4)))
        command_text = self.main_font.render(f"F - Fruitopedia", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.5)))
        command_text = self.main_font.render(f"Space - Pause game", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.6)))
        command_text = self.main_font.render(f"Return - Back to menu", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.7)))
        command_text = self.main_font.render(f"Q / Escape - Quit game", True, self.font_color)
        self.window.blit(command_text, (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.8)))

    def display_help_line(self):                                                # Display help line
        coord_x = int(self.current_fruit.rect.center[0] - self.help_line_width * 0.5)
        up = self.current_fruit.rect.bottom
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
        if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3]:
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

    def Display_Fruitopedia(self):                                              # Display screen with fruits data
        # Display ask background
        pos = self.display_default_box(self.all_fruits_screen_percent)
        # Display ask title
        title = self.small_title_font.render(f"Fruitopedia", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        percent = 0.6
        for i, fruit in enumerate(self.Fruits):                                 # Display all fruits (dynamic)
            equation = i ** 1.5 / (len(self.Fruits) ** 1.5) + 0.05 if i > 0 else 0.05               # Function
            fruit.rect.x = pos[0] + pos[2] * equation - fruit.radius * percent
            fruit.rect.y = pos[1] + pos[3] * 0.5 - fruit.radius * percent
            self.draw_reduced_fruit(fruit, (fruit.rect.x, fruit.rect.y), percent)
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
        self.display_button("Close", (int(pos[0] + pos[2] * 0.45), int(pos[1] + pos[3] * 0.82),
                                      int(pos[2] * 0.1), int(pos[3] * 0.15)), "F")

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
        self.display_button("Restart", (int(pos[0] + pos[2] * 0.15), int(pos[1] + pos[3] * 0.85),
                                        int(pos[2] * 0.2), int(pos[3] * 0.1)), "SPACE")
        self.display_button("Menu", (int(pos[0] + pos[2] * 0.65), int(pos[1] + pos[3] * 0.85),
                                     int(pos[2] * 0.2), int(pos[3] * 0.1)), "RETURN")

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
        self.display_button("Yes", (int(pos[0] + pos[2] * 0.1), int(pos[1] + pos[3] * 0.7),
                                        int(pos[2] * 0.3), int(pos[3] * 0.25)), "Y")
        self.display_button("No", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.7),
                                     int(pos[2] * 0.3), int(pos[3] * 0.25)), "N")

    def display_pause_screen(self):                                             # Display pause screen
        self.window.blit(self.paused_glass, (0, 0))                             # Semi-transparent background
        # Display pause text
        size = (self.screen_width, self.screen_height)
        pause_text = self.title_font.render(f"Pause", True, self.font_color)
        pause_size = pause_text.get_size()
        self.window.blit(pause_text, (int(size[0] * 0.5 - pause_size[0] * 0.5),
                                      int(size[1] * 0.33 - pause_size[1] * 0.5)))
        # Display button
        self.display_button("Continue", (int(size[0] * 0.45), int(size[1] * 0.5),
                                         int(size[0] * 0.1), int(size[1] * 0.08)), "SPACE")
        self.display_button("Restart", (int(size[0] * 0.45), int(size[1] * 0.6),
                                        int(size[0] * 0.1), int(size[1] * 0.08)), "R")
        self.display_button("Menu", (int(size[0] * 0.45), int(size[1] * 0.7),
                                     int(size[0] * 0.1), int(size[1] * 0.08)), "RETURN")
        self.display_button("Quit", (int(size[0] * 0.45), int(size[1] * 0.8),
                                     int(size[0] * 0.1), int(size[1] * 0.08)), "Q")

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
        pos = [self.screen_width * 0.95, self.screen_height * 0.2, self.screen_height * 0.01, self.screen_height * 0.2]
        pygame.draw.rect(self.window, "orange", pos, 0, int(pos[2]))
        pos[1] = pos[1] + (1 - self.volume) * pos[3]
        pos[3] = pos[3] * self.volume
        pygame.draw.rect(self.window, "gold", pos, 0, int(pos[2]))

    def Music_Manager(self):                                                    # Manage music
        if self.playing:
            pygame.mixer.music.load(self.music)                                 # Load music (once)
            pygame.mixer.music.play(self.repeat)                                # Play endlessly : -1
            self.playing = False
        self.volume = 0 if self.volume < 0 else 1.0 if self.volume > 1.0 else self.volume
        volume = 0 if self.on_mute else self.volume
        pygame.mixer.music.set_volume(volume)                                   # Set volume

    def start_new_game(self):                                                   # Reset game
        self.pausing = False
        self.helping = False
        self.on_menu = False
        self.on_game = True
        self.on_lose = False
        self.on_back = False
        self.on_allF = False

        self.score = 0
        self.Panier.empty()
        self.current_fruit = choice(self.FruitsChoosable)
        self.next_fruit = choice(self.FruitsChoosable)
        self.tip = None

    def go_to_menu(self):                                                       # Change bools to go back to menu
        self.on_menu = True
        self.on_game = False
        self.on_lose = False
        self.on_help = False
        self.on_para = False                                                    # For parameters
        self.on_back = False
        self.on_allF = False

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
        self.Save_scores()
        print("Closing game...")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    jeu = Game(3, True, False)
