import pygame


class ImageUtils:

    @staticmethod
    def get_image_from_sprite_sheet(sheet_name, start_x, start_y, end_x, end_y, scale=1):
        """"
        Load a sprite sheet and extract a image from it based on starting and ending position
        """

        sheet_surface = pygame.image.load(sheet_name).convert_alpha()
        width = end_x - start_x
        height = end_y - start_y
        color_key = (255, 0, 255)

        # Create a blank surface and fill it with the transparent color
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill(color_key)

        # Draw the section of the sheet onto the blank image
        image.blit( sheet_surface, (0, 0), (start_x, start_y, end_x, end_y))

        # Remove the transparent color
        image.set_colorkey(color_key)

        # Scale the image
        image = pygame.transform.scale(image, (width * scale, height * scale))

        # Optimize image for pygame
        image = image.convert_alpha()

        return image

    @staticmethod
    def get_animation_frames_from_sprite_sheet(sheet_name='', width=0, height=0, rows=1, cols=1, scale=2, flip_horizontal=False):
        """
        Extract all the frames of an animation from a sprite sheet
        :param sheet_name:
        :param sheet:
        :param width:
        :param height:
        :param rows:
        :param cols:
        :param scale:
        :return:
        """

        if width == 0 or height == 0:
            sprite_sheet_image = pygame.image.load(sheet_name).convert_alpha()
            width = sprite_sheet_image.get_width() / cols
            height = sprite_sheet_image.get_height() / rows
        images = []
        for col in range(cols):
            for row in range(rows):
                image = ImageUtils.get_image_from_sprite_sheet(sheet_name, col * width,row * height, col * width + width, height, scale)
                if flip_horizontal:
                    image = pygame.transform.flip(image, True, False)
                images.append(image)

        return images
