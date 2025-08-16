import os

import pygame

pygame.mixer.init()

class Constants:

    WIDTH, HEIGHT = 1024, 768
    ASSETS_FOLDER = 'assets'
    TILE_SIZE = 128

    JUMP_AUDIO = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, 'audio', 'jump.wav'))
    COIN_AUDIO = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, 'audio', 'coin.wav'))
