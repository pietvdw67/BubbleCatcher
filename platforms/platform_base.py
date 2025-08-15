import pygame

from utils.image_utils import ImageUtils


class PlatformBase(pygame.sprite.Sprite):
    def __init__(
            self,
            position: pygame.math.Vector2,
            length: int = 0,
            is_moving: bool = False,
            move_range: int = 100,
            move_speed: float = 0.5
    ) -> None:

        super().__init__()

        self.position = position
        self.length = max(3, length)
        self.is_moving = is_moving
        self.move_range = move_range
        self.move_speed = move_speed

        self.image = None
        self.rect = None

        self.left_image = None
        self.right_image = None
        self.center_image = None

        self._start_x = self.position.x
        self.current_moving_speed = self.move_speed

    def build_image(self):

        width = self.center_image.get_width()
        height = self.center_image.get_height()

        self.image = pygame.Surface((width * self.length, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        for i in range(self.length):
            image = self.center_image
            if i == 0:
                image = self.left_image
            elif i == self.length-1:
                image = self.right_image

            self.image.blit(image, (i * width, 0))

        self.rect.x = self.position.x
        self.rect.y = self.position.y

        # set rect smaller to stop player / ball from colliding next to sprite
        self.rect.x += 10
        self.rect.width -= 20

    def update(self):
        if not self.is_moving:
            return

        if self.position.x < self._start_x:
            self.current_moving_speed = abs(self.move_speed)
        if self.position.x > self._start_x + self.move_range:
            self.current_moving_speed = abs(self.move_speed) * -1

        self.position.x += self.current_moving_speed

        self.rect.x = self.position.x






