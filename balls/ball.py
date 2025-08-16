import pygame
import os
import random

from constants import Constants
from utils.image_utils import ImageUtils
from balls.ball_constants import BallConstants
from game_state import GameState


class Ball(pygame.sprite.Sprite):

    def __init__(self, game_state: GameState, position: pygame.math.Vector2, color: str) -> None:
        super().__init__()
        self.game_state = game_state
        self.position = position
        self.velocity = pygame.math.Vector2(0, 0)
        self.color = color
        self.load_animations(color)
        self.images = None
        self.animation_delay = 4
        self._animation_delay_count = 0
        self.animation_frame_index = 0
        self.image = None
        self.rect = None
        self.height = 0
        self.width = 0

        vel_x = random.choice([-BallConstants.BALL_SPEED, BallConstants.BALL_SPEED])
        vel_y = random.choice([-BallConstants.BALL_SPEED, BallConstants.BALL_SPEED])
        self.velocity = pygame.math.Vector2(vel_x, vel_y)

        self.load_animations(color)
        self.update()

    def load_animations(self, ball_name):

        image_path = os.path.join(Constants.ASSETS_FOLDER, "balls", ball_name + ".png")
        images = ImageUtils.get_animation_frames_from_sprite_sheet(
            sheet_name=image_path,
            cols=8,
            rows=1,
            scale=0.7
        )
        self.height = images[0].get_height()
        self.width = images[0].get_width()

        self.images = images

    def update(self):
        pygame.sprite.Sprite.update(self)

        self._set_animation_frame()

        self.image = self.images[self.animation_frame_index]
        self.rect = self.image.get_rect()

        # Bounds
        if self.position.x >= Constants.WIDTH - self.width:
            self.velocity.x *= -1
        if self.position.x <= 0:
            self.velocity.x *= -1
        if self.position.y <= 0:
            self.velocity.y *= -1
        if self.position.y >= BallConstants.GROUND_HEIGHT - self.height:
            self.velocity.y *= -1

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def _set_animation_frame(self):

        if self.animation_delay == 0:
            return 0

        self._animation_delay_count += 1
        if self._animation_delay_count < self.animation_delay:
            return

        self._animation_delay_count = 0
        self.animation_frame_index += 1
        if self.animation_frame_index >= len(self.images):
            self.animation_frame_index = 0
