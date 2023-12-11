# from math import *
from random import choice
from time import time
from os import getcwd, listdir
from fruit import Fruit
from data import *
import pygame
import sys

# !! Normaliser les poids des fruits OU augmenter les forces de repulsion entre les fruits


# [check] : Make window display
# [check] : Display random fruit
# [check] : Forbid fruit from going out window + add gravitation
# [check] : Make collision between fruits
# [check] : Make same fruit fusion and create next fruit
# [check] : Add box and collisions with it + bg
# [check] : Add score and next fruit
# [check] : Add player choose where to put fruit + make next fruit coherent
# [check] : Upgrade fruit physics + collisions + add timers (dropping next fruit + merging fruit)
# [check] : Add menu + buttons (start game, restart, go to menu, options, exit)
# [check] : Make buttons work + add project on GitHub
# [v0.1.3] : Add save scores for scoreboard + display all fruits
# [v0.1.4] : Add borders and reflect on fruits and buttons
# [v0.1.5] : [check] Add condition for losing game + make lose screen
# [v0.1.6] : Add musics + lector + volume
# [v0.1.7] : Add parameters + balance difficulties
# [v0.1.8] : Add skin for fruits + design boxes (add borders...)
# [v0.1.9] : Upgrade screen design
# [v0.2.0] : Add documentations + clean code + add comms
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        # Main data
        self.creator = "One Shot"
        self.version = "v0.1.2"
        self.game_name = "Suika Fruit"
        # Boolean data
        self.running = True
        self.pausing = False
        self.helping = False
        self.on_menu = True
        self.on_game = False
        self.on_lose = False
        self.on_help = False
        self.on_para = False                                                    # For parameters
        self.on_back = False                                                    # Ask for back menu (security)
        self.on_allF = False
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
        # Fruit data
        self.nb_fruit = 0
        self.FruitsName = ["cerise", "fraise", "raisin", "clémentine", "orange", "pomme",
                           "pamplemousse", "pêche", "ananas", "melon", "pastèque"]
        self.Fruits = []                                                        # All possible fruits
        self.FruitsChoosable = []                                               # Fruits that can be dropped
        self.Panier = pygame.sprite.Group()                                     # Fruits in bucket during game
        # Screens and tips data
        self.button_color = (230, 255, 140)
        self.parameters_screen_percent = [0.1, 0.1, 0.8, 0.8]
        self.ask_screen_percent = [0.35, 0.35, 0.3, 0.3]
        self.lose_screen_percent = [0.3, 0.1, 0.4, 0.8]                         # Also used for help screen
        self.all_fruits_screen_percent = [0.1, 0.25, 0.8, 0.5]
        self.screens_color = (250, 250, 200)
        self.Tips = ["Try not to separate large fruits from each other",
                     "You can see the fruit evolution at the bottom left of the screen",
                     "Try to sort fruits by size so they can merge more easily",
                     "If the next fruit is the same as your current fruit, \n"
                     "you can merge them to have the next bigger fruit",
                     "Try to get used to the physics of the game"]
        self.tip = None
        # Main box data (for fruits)
        self.main_box_percent = [0.33, 0.15, 0.34, 0.8]
        self.box_pos = (self.screen_width * self.main_box_percent[0], self.screen_height * self.main_box_percent[1],
                        self.screen_width * self.main_box_percent[2], self.screen_height * self.main_box_percent[3])
        self.main_box_width = 10                                                # px
        self.main_box_color = (255, 200, 90)
        self.merging_fruit_start_timer = time()
        self.merging_fruit_last_timer = None
        self.merging_fruit_timer_duration = 0.1
        # Score data
        self.score = 0
        self.highscore = 0
        self.score_box_percent = [0.08, 0.3, 0.15, 0.15]
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
        self.help_line_color = (255, 255, 220, 128)
        self.help_line_width = 5
        # Pause data
        self.paused_glass = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.rect(self.paused_glass, (255, 255, 255), self.paused_glass.get_rect())
        self.paused_glass.set_alpha(120)
        # Gameplay data
        self.gravity = gravity                                                  # Falling speed
        self.resistance = resistance                                            # Slowing speed
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
        # Loading data
        self.create_fruits()
        self.run()

    def create_fruits(self):                                                    # Load fruits
        cerise =    Fruit(self.FruitsName[0],  (240, 0, 0),     10, 11, 2)
        fraise =    Fruit(self.FruitsName[1],  (255, 140, 160), 20, 10, 4)
        raisin =    Fruit(self.FruitsName[2],  (195, 75, 255),  30,  9, 8)
        clement =   Fruit(self.FruitsName[3],  (255, 210, 40),  40,  8, 16)
        orange =    Fruit(self.FruitsName[4],  (255, 145, 45),  50,  7, 32)
        pomme =     Fruit(self.FruitsName[5],  (250, 20, 20),   60,  6, 64)
        mousse =    Fruit(self.FruitsName[6],  (255, 240, 105), 70,  5, 128)
        peche =     Fruit(self.FruitsName[7],  (255, 190, 235), 80,  4, 256)
        ananas =    Fruit(self.FruitsName[8],  (255, 250, 30),  90,  3, 512)
        melon =     Fruit(self.FruitsName[9],  (160, 250, 70),  100, 2, 1024)
        pasteque =  Fruit(self.FruitsName[10], (60, 210, 25),   110, 1, 2048)
        self.Fruits = [cerise, fraise, raisin, clement, orange, pomme, mousse, peche, ananas, melon, pasteque]
        self.FruitsChoosable = self.Fruits[:5]
        self.nb_fruit = len(self.Fruits)

        self.Panier.empty()
        self.current_fruit = choice(self.FruitsChoosable)
        self.next_fruit = choice(self.FruitsChoosable)

    def run(self):                                                              # Main fonction of game
        self.Load_score()

        while self.running:                                                     # Main loop of game
            if self.on_game:
                if not self.pausing:
                    self.Update_Manager()
                    self.Collision_Manager()
                    self.Check_Lose()

            self.Inputs_Manager()

            self.Display_Manager()

            pygame.display.flip()
            self.horloge.tick(self.fps)

        self.Close_Game()

    def Update_Manager(self):
        self.Panier.update()                                                    # Update all fruits

    def Display_Manager(self):
        if self.on_menu:
            self.Display_Menu()
            if self.on_help:
                self.Display_Help()
            if self.on_para:
                self.Display_Parameters()
        elif self.on_game:
            self.Display_Game()

    def Display_Menu(self):
        self.window.fill(self.bg_color)

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

        # pygame.mouse.set_cursor(pygame.cursors.diamond)                       # ! Change cursor

    def display_title(self):                                                    # Display game name (menu)
        title = self.title_font.render(f"{self.game_name}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(self.screen_width * 0.5 - title_size[0] * 0.5),
                                 int(self.screen_height * 0.2 - title_size[1] * 0.5)))

    def display_button(self, name, pos, command=""):
        # Display button background
        pygame.draw.rect(self.window, self.button_color, pos, 0, pos[3])
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

    def Display_Help(self):
        # Display help background
        size = self.lose_screen_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.screens_color, pos, 0, int(pos[2] * 0.1))
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

    def Display_Parameters(self):
        # Display parameters background
        size = self.parameters_screen_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.screens_color, pos, 0, int(pos[3] * 0.1))
        # Display parameters title
        title = self.small_title_font.render(f"Parameters", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.1 - title_size[1] * 0.5)))
        # Display parameters text
        working = True
        if working:
            text = self.title_font.render(f"Work in progress...", True, self.font_color)
            text_size = text.get_size()
            self.window.blit(text, (int(pos[0] + pos[2] * 0.5 - text_size[0] * 0.5),
                                    int(pos[1] + pos[3] * 0.5 - text_size[1] * 0.5)))
        else:
            text = self.button_font.render(f"Screen", True, self.font_color)
            text_size = text.get_size()
            self.window.blit(text, (int(pos[0] + pos[2] * 0.2 - text_size[0] * 0.5),
                                    int(pos[1] + pos[3] * 0.25 - text_size[1] * 0.5)))
            text = self.button_font.render(f"Difficulty", True, self.font_color)
            text_size = text.get_size()
            self.window.blit(text, (int(pos[0] + pos[2] * 0.2 - text_size[0] * 0.5),
                                    int(pos[1] + pos[3] * 0.55 - text_size[1] * 0.5)))
            text = self.button_font.render(f"Sounds", True, self.font_color)
            text_size = text.get_size()
            self.window.blit(text, (int(pos[0] + pos[2] * 0.6 - text_size[0] * 0.5),
                                    int(pos[1] + pos[3] * 0.25 - text_size[1] * 0.5)))
            text = self.button_font.render(f"Music", True, self.font_color)
            text_size = text.get_size()
            self.window.blit(text, (int(pos[0] + pos[2] * 0.6 - text_size[0] * 0.5),
                                    int(pos[1] + pos[3] * 0.55 - text_size[1] * 0.5)))
            # Display buttons
            self.display_button("Save", (int(pos[0] + pos[2] * 0.2), int(pos[1] + pos[3] * 0.85),
                                         int(pos[2] * 0.2), int(pos[3] * 0.1)), "S")
            self.display_button("Menu", (int(pos[0] + pos[2] * 0.6), int(pos[1] + pos[3] * 0.85),
                                         int(pos[2] * 0.2), int(pos[3] * 0.1)), "P")

    def Display_Game(self):
        self.window.fill(self.bg_color)

        self.display_small_title()

        self.display_box()                                                      # Main box for fruits
        self.display_score()
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

        if self.helping:
            self.display_help_line()

        self.Panier.draw(self.window)                                           # Display all fruits

        if self.on_allF:
            self.Display_Fruitopedia()

        if self.on_lose:
            self.Display_Lose()

        if self.on_back:
            self.ask_back_menu()

        if self.pausing:
            self.display_pause_screen()

    def display_small_title(self):                                              # Display small game name
        title = self.small_title_font.render(f"{self.game_name}", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(self.screen_width * 0.5 - title_size[0] * 0.5),
                                 int(self.screen_height * 0.1 - title_size[1] * 0.5)))

    def display_box(self):                                                      # Display main box for fruits
        pygame.draw.rect(self.window, self.main_box_color, self.box_pos, self.main_box_width, self.main_box_width * 2)

    def display_score(self):                                                    # Display scoreboard
        # Display score background
        size = self.score_box_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.score_box_color, pos, 0, int(pos[3] * 0.1))
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

    def display_evolution(self):                                                # Display evolution of fruits
        # Display evolution background
        size = self.evolution_box_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.evolution_box_color, pos, 0, int(pos[3] * 0.1))
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
        image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(image, fruit.color, (radius, radius), radius)
        pygame.draw.circle(image, fruit.border_color, (radius, radius), radius, int(fruit.width * percent))
        self.window.blit(image, pos)

    def display_next_fruit(self):                                               # Display next fruit box
        # Display next fruit background
        size = self.next_fruit_box_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.next_fruit_box_color, pos, 0, int(pos[2] * 0.1))
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
        size = self.commands_box_percent
        pos = (int(self.screen_width * size[0]), self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.commands_box_color, pos, 0, int(pos[2] * 0.1))
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

    def display_help_line(self):
        coord_x = int(self.current_fruit.rect.center[0] - self.help_line_width * 0.5)
        up = self.current_fruit.rect.bottom
        down = self.box_pos[1] + self.box_pos[3] - self.main_box_width
        surface = pygame.Surface((self.help_line_width, down - up)).convert_alpha()
        surface.fill(self.help_line_color)
        self.window.blit(surface, (coord_x, up))

    def display_pause_screen(self):
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

    def Display_Fruitopedia(self):
        # Display ask background
        size = self.all_fruits_screen_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.screens_color, pos, 0, int(pos[3] * 0.1))
        # Display ask title
        title = self.small_title_font.render(f"Fruitopedia", True, self.font_color)
        title_size = title.get_size()
        self.window.blit(title, (int(pos[0] + pos[2] * 0.5 - title_size[0] * 0.5),
                                 int(pos[1] + pos[3] * 0.15 - title_size[1] * 0.5)))
        percent = 0.6
        for i, fruit in enumerate(self.Fruits):
            equation = i ** 1.5 / (len(self.Fruits) ** 1.5) + 0.05 if i > 0 else 0.05               # Function
            fruit.rect.x = pos[0] + pos[2] * equation - fruit.radius * percent
            fruit.rect.y = pos[1] + pos[3] * 0.5 - fruit.radius * percent
            self.draw_reduced_fruit(fruit, (fruit.rect.x, fruit.rect.y), percent)
            mouse = pygame.mouse.get_pos()
            if fruit.collide_point(mouse, percent):
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

    def Display_Lose(self):
        # Display lose background
        size = self.lose_screen_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.screens_color, pos, 0, int(pos[2] * 0.1))
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

                        if event.key == pygame.K_r and self.pausing:
                            self.start_new_game()

        self.pressed = pygame.key.get_pressed()

        if self.pressed[pygame.K_q] or self.pressed[pygame.K_ESCAPE]:
            self.Close_Game()

    def drop_fruit(self):                                                       # Drop current fruit
        self.next_fruit_last_timer = time()                                     # Check timer
        if self.next_fruit_last_timer - self.next_fruit_start_timer >= self.next_fruit_timer_duration:
            fruit = Fruit(self.current_fruit.name, self.current_fruit.color, self.current_fruit.radius,
                          self.current_fruit.weight, self.current_fruit.score)
            fruit.rect.x = self.current_fruit.rect.x                            # Place fruit
            fruit.rect.y = self.current_fruit.rect.y
            self.Panier.add(fruit)
            self.current_fruit = self.next_fruit                                # Replace current fruit
            self.next_fruit = choice(self.FruitsChoosable)                      # Change next fruit
            self.score += fruit.score
            self.next_fruit_start_timer = time()

    def ask_back_menu(self):
        # Display ask background
        size = self.ask_screen_percent
        pos = (self.screen_width * size[0], self.screen_height * size[1],
               self.screen_width * size[2], self.screen_height * size[3])
        pygame.draw.rect(self.window, self.screens_color, pos, 0, int(pos[2] * 0.1))
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

    def start_new_game(self):
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

    def go_to_menu(self):
        self.on_menu = True
        self.on_game = False
        self.on_lose = False
        self.on_help = False
        self.on_para = False                                                    # For parameters
        self.on_back = False
        self.on_allF = False

    def Collision_Manager(self):                                                # Manage collisions
        for index_f, fruit in enumerate(self.Panier.sprites()):
            for index_o, other in enumerate(self.Panier.sprites()):             # Provide fruits to collide each other
                # If fruit merge
                if fruit != other and fruit.collide_circle(other) and fruit.name == other.name:
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

                            next_f = self.Fruits[pos]
                            bigger = Fruit(next_f.name, next_f.color, next_f.radius, next_f.weight, next_f.score)
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
            if fruit.rect.bottom >= self.screen_height:
                fruit.rect.bottom = self.screen_height
                fruit.vel_y = 0

    def Check_Lose(self):
        for fruit in self.Panier.sprites():
            if fruit.rect.bottom < self.box_pos[1] and abs(fruit.vel_y) < 1:
                self.on_lose = True
                self.Save_score()
                break

    def Get_score(self):                                                        # ! Doesn't count merged last fruit
        self.score = 0
        for fruit in self.Panier.sprites():
            self.score += fruit.score

    @staticmethod
    def Reset_score():
        print(f"Saved score reset !")
        file = open("scores/save.txt", "w")
        file.write(str(0))
        file.close()

    def Save_score(self):                                                       # Save current score
        if self.score > self.highscore:
            print(f"Saving current score... [{self.score} pts]")
            file = open("scores/save.txt", "w")
            file.write(str(self.score))
            file.close()
        elif self.score > 0:
            print(f"High score not beaten : {self.highscore} pts")

    def Load_score(self):                                                       # Load current score
        print("Loading last high score...")
        file = open("scores/save.txt", "r")
        lines = file.readlines()
        if lines:
            self.highscore = int(lines[0])
        file.close()

    def Close_Game(self):                                                       # Close game
        self.Save_score()
        print("Closing game...")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    jeu = Game()
