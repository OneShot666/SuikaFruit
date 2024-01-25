from random import *
import string
import pygame

pygame.init()

size = (400, 300)
window = pygame.display.set_mode(size)
couleur_fond = (0, 0, 0)
window.fill(couleur_fond)

grand_font = pygame.font.Font(f"fonts/Bubble Bobble.ttf", 50)
small_font = pygame.font.Font(f"fonts/Bubble Bobble.ttf", 25)

Alphabet = string.ascii_letters
Numbers = [i for i in range(0, 10)]
Special = ["_"]
phrase = "Bonjour"
letter_size = 21
index = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            char = event.dict['unicode']
            print(f"Dict : {char}")                                             # Pour ajouter
            letter = pygame.key.name(event.key)
            print(f"Name : {letter}")                                           # Pour identifier
            if event.key == pygame.K_BACKSPACE:
                mini = 0 if index - 1 < 0 else index - 1
                phrase = phrase[:mini] + phrase[index:]
                index -= 1
            elif event.key == pygame.K_LEFT:
                index -= 1
            elif event.key == pygame.K_RIGHT:
                index += 1
            elif char in Alphabet or char in Special:
                if pygame.key.get_pressed()[pygame.K_LSHIFT] or \
                       pygame.key.get_pressed()[pygame.K_RSHIFT]:
                    char = char.upper()
                place = 0 if index - 1 < 0 else index
                phrase = phrase[:place] + char + phrase[place:]
                index += 1
            elif char.isdigit() and int(char) in Numbers:
                place = 0 if index - 1 < 0 else index
                phrase = phrase[:place] + char + phrase[place:]
                index += 1
            index = 0 if index < 0 else len(phrase) if index > len(phrase) else index
            print(f"({index}) {phrase}")

    window.fill("darkgrey")

    sentence = grand_font.render(f"{phrase}", True, "white")
    sentence_size = sentence.get_size()
    sentence_pos = (int(size[0] * 0.5 - sentence_size[0] * 0.5),
                    int(size[1] * 0.5 - sentence_size[1] * 0.5))
    window.blit(sentence, sentence_pos)

    pos = grand_font.render(f"{phrase[:index]}", True, "white")
    pos_size = pos.get_size()
    pygame.draw.line(window, "white", (int(sentence_pos[0] + pos_size[0]), sentence_pos[1]),
                     (int(sentence_pos[0] + pos_size[0]), sentence_pos[1] + sentence_size[1]), 3)

    number = small_font.render(f"{index}", True, "white")
    number_size = number.get_size()
    window.blit(number, (int(size[0] * 0.5 - number_size[0] * 0.5),
                         int(size[1] * 0.65 - number_size[1] * 0.5)))

    pygame.display.flip()

pygame.display.quit()
