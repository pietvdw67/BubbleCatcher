import pygame

from platforms.platform_base import PlatformBase
from utils.image_utils import ImageUtils

class Platform(PlatformBase):

    def set_images(
            self,
            sheet_name: str,
            tile_width: int,
            tile_height: int,
            left_image_pos: pygame.math.Vector2,
            center_image_pos: pygame.math.Vector2,
            right_image_pos: pygame.math.Vector2,
            scale: int = 1
    ) -> None:

        width = tile_width * scale
        height = tile_height * scale

        self.left_image = ImageUtils.get_image_from_sprite_sheet(
            sheet_name,
            left_image_pos.x,
            left_image_pos.y,
            left_image_pos.x + tile_width,
            left_image_pos.y + tile_height,
            scale)

        self.center_image = ImageUtils.get_image_from_sprite_sheet(
            sheet_name,
            center_image_pos.x,
            center_image_pos.y,
            center_image_pos.x + tile_width,
            center_image_pos.y + tile_height,
            scale)

        self.right_image = ImageUtils.get_image_from_sprite_sheet(
            sheet_name,
            right_image_pos.x,
            right_image_pos.y,
            right_image_pos.x + tile_width,
            right_image_pos.y + tile_height,
            scale)

        super().build_image()
