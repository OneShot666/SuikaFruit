import pygame
import sys

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Créer la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Music and sound test")

# Sounds
pygame.mixer.music.load("musics/main_music.mp3")
sound = pygame.mixer.Sound("sounds/unlock_skins.wav")
volume_music = 0.5
volume_sound = 0.3

pygame.mixer.music.set_volume(volume_music)
pygame.mixer.music.play(-1)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fenetre.fill("cyan")                                                        # Background

    if pygame.mouse.get_pressed()[0]:                                           # Trigger (click)
        sound.set_volume(volume_sound)
        sound.play()

    pygame.display.flip()                                                       # Update screen
