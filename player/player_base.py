import pygame


class PlayerBase(pygame.sprite.Sprite):

    def __init__(self, name, x_pos, y_pos):

        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.health = 100
        self.rect = None
        self.image = None

    def draw(self, screen):

        pygame.draw.rect(screen, (255,  255, 255), self.rect)

    def update(self):
        pygame.sprite.Sprite.update(self)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 30, 50)
        self.image = pygame.Surface((50, 50)).convert_alpha()
        self.image.fill((255, 255, 255))
