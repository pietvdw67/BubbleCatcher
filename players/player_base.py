import pygame

from players.player_constants import PlayerConstants
from constants import Constants

class PlayerBase(pygame.sprite.Sprite):

    def __init__(self, name, position: pygame.math.Vector2) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.position = position
        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

        self.health = 100
        self.direction = "right"
        self.on_ground = False

        self.rect = None
        self.image = None
        self.animations = {}
        self.animations_delays = {}
        self._animation_active = None
        self._animation_active_previous = None
        self.animation_frame_index = 0
        self._animation_delay_count = 0

    def update(self):
        pygame.sprite.Sprite.update(self)

        self._set_animation_frame()

        self.image = self.animations[self._animation_active][self.animation_frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        # Set rect a bit smaller so character does not hang in air next to platform
        self.rect.x += 10
        self.rect.width -= 20

    def move(self, dt):

        if self.acceleration.x > 0:
            self.direction = "right"
        if self.acceleration.x < 0:
            self.direction = "left"

        self.acceleration.y = PlayerConstants.PLAYER_GRAVITY

        self.acceleration.x += self.velocity.x * PlayerConstants.PLAYER_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity

        # Boundaries
        if self.position.y > PlayerConstants.PLAYER_GROUND_HEIGHT:
            self.position.y = PlayerConstants.PLAYER_GROUND_HEIGHT
            self.on_ground = True

        if self.position.x < 0:
            self.position.x = 0

        if self.image is not None:
            if self.position.x + self.image.get_width() > Constants.WIDTH-1:
                self.position.x = Constants.WIDTH-1 - self.image.get_width()

    def jump(self):
        if self.on_ground:
            self.velocity.y = PlayerConstants.PLAYER_JUMP_STRENGTH
            self.on_ground = False

    def set_animation_active(self, active_name):
        if not self._animation_active_previous:
            self._animation_active_previous = active_name
            self._animation_active = active_name
            self.animation_frame_index = 0
            return

        if self._animation_active_previous != active_name:
            self._animation_active_previous = active_name
            self._animation_active = active_name
            self.animation_frame_index = 0


    def _set_animation_frame(self):

        if self.animations_delays == 0:
            return 0

        self._animation_delay_count += 1
        if self._animation_delay_count < self.animations_delays[self._animation_active]:
            return

        self._animation_delay_count = 0
        self.animation_frame_index += 1
        if self.animation_frame_index >= len(self.animations[self._animation_active]):
            self.animation_frame_index = 0
