import pygame
import os

from constants import Constants
from player.player_base import PlayerBase
from utils.assets_utils import AssetsUtils
from utils.image_utils import ImageUtils


class Player(PlayerBase):

    def __init__(self, name, x_pos, y_pos):

        super().__init__(name, x_pos, y_pos)

        self.load_animations(name)
        self.set_animation_active("idle_right")

    def load_animations(self, player_folder):
        image_path = os.path.join(Constants.ASSETS_FOLDER, "players", player_folder, "idle.png")
        images = ImageUtils.get_animation_frames_from_sprite_sheet(
            sheet_name=image_path,
            cols=11
        )
        self.animations["idle_right"] = images
        self.animations_delays["idle_right"] = 4

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



    def move(self, dt):
        super().move(dt)
        base_animation = "idle"
        if self.vel.x == 0:
            base_animation = "idle"
        else:
            base_animation = "run"

        self.set_animation_active(base_animation + '_' + self.direction)









