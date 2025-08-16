import pygame
import os

from constants import Constants
from players.player_base import PlayerBase
from utils.image_utils import ImageUtils


class Player(PlayerBase):

    def __init__(self, name, asset_name: str, position: pygame.math.Vector2) -> None:

        super().__init__(name, position)

        self.load_animations(asset_name)
        self.set_animation_active("idle_right")

    def load_animations(self, player_folder):

        image_path = os.path.join(Constants.ASSETS_FOLDER, "players", player_folder, "idle.png")
        images = ImageUtils.get_animation_frames_from_sprite_sheet(
            sheet_name=image_path,
            cols=11
        )
        self.animations["idle_right"] = images
        self.animations_delays["idle_right"] = 4

        size_x = images[0].get_width()
        size_y = images[0].get_height()

        images = ImageUtils.get_animation_frames_from_sprite_sheet(
            sheet_name=image_path,
            cols=11,
            flip_horizontal=True
        )
        self.animations["idle_left"] = images
        self.animations_delays["idle_left"] = 4

        image_path = os.path.join(Constants.ASSETS_FOLDER, "players", player_folder, "run.png")
        images = ImageUtils.get_animation_frames_from_sprite_sheet(
            sheet_name=image_path,
            cols=12
        )
        self.animations["run_right"] = images
        self.animations_delays["run_right"] = 4
        images = ImageUtils.get_animation_frames_from_sprite_sheet(
            sheet_name=image_path,
            cols=12,
            flip_horizontal=True
        )
        self.animations["run_left"] = images
        self.animations_delays["run_left"] = 4

        image_path = os.path.join(Constants.ASSETS_FOLDER, "players", player_folder, "jump.png")
        images = pygame.image.load(image_path).convert_alpha()
        images = pygame.transform.scale(images, (size_x, size_y))
        self.animations["jump_right"] = [images]
        self.animations_delays["jump_right"] = 0

        image_path = os.path.join(Constants.ASSETS_FOLDER, "players", player_folder, "jump.png")
        images = pygame.image.load(image_path).convert_alpha()
        images = pygame.transform.flip(images, True, False)
        images = pygame.transform.scale(images, (size_x, size_y))
        self.animations["jump_left"] = [images]
        self.animations_delays["jump_left"] = 0

    def move(self, dt):

        super().move(dt)

        base_animation = "idle"

        if self.on_ground:
            if round(self.velocity.x) == 0:
                base_animation = "idle"
            else:
                base_animation = "run"
        else:
            base_animation = "jump"

        self.set_animation_active(base_animation + '_' + self.direction)
