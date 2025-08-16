import pygame


class GameState:

    running = True
    clock = pygame.time.Clock()
    score_left = 0
    score_right = 0

    players = []
    balls = []

    sprite_groups = {
        "players": pygame.sprite.Group(),
        "platforms": pygame.sprite.Group(),
        "balls": pygame.sprite.Group()
    }
