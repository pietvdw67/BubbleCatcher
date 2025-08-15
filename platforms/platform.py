import pygame

from utils.image_utils import ImageUtils


class Platform(pygame.sprite.Sprite):
    def __init__(
            self,
            position: pygame.math.Vector2,
            length: int = 0,
            is_moving: bool = False,
            move_range: int = 0,
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

    def set_image(
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

        left_image = ImageUtils.get_image_from_sprite_sheet(
            sheet_name,
            left_image_pos.x,
            left_image_pos.y,
            left_image_pos.x + tile_width,
            left_image_pos.y + tile_height,
            scale)

        center_image = ImageUtils.get_image_from_sprite_sheet(
            sheet_name,
            center_image_pos.x,
            center_image_pos.y,
            center_image_pos.x + tile_width,
            center_image_pos.y + tile_height,
            scale)

        right_image = ImageUtils.get_image_from_sprite_sheet(
            sheet_name,
            right_image_pos.x,
            right_image_pos.y,
            right_image_pos.x + tile_width,
            right_image_pos.y + tile_height,
            scale)

        self.image = pygame.Surface((width * self.length, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        for i in range(self.length):
            image = center_image
            if i == 0:
                image = left_image
            elif i == self.length-1:
                image = right_image

            self.image.blit(image, (i * width, 0))

        self.rect.x = self.position.x
        self.rect.y = self.position.y






