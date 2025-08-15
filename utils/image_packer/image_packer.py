import pygame
import os
import math

pygame.init()


class ImagePacker:

    SOURCE_FOLDER = 'C:/Users/f3953289/Downloads/FreeTileset/png/Tiles'
    TARGET_FILE = 'C:/Users/f3953289/Downloads/terrain.png'
    OUTPUT_COL = 4
    OUTPUT_ROW = 5

    def __init__(self):
        screen_width, screen_height = 800, 600
        screen = pygame.display.set_mode((screen_width, screen_height))

    def pack(self, source_folder, target_file, cols_text, rows_text):
        cols = int(cols_text)
        rows = int(rows_text)

        entries = os.listdir(source_folder)
        images_list = []
        max_height = 0
        max_width = 0
        for entry in entries:
            file_name = os.path.join(source_folder, entry)
            image = pygame.image.load(file_name).convert_alpha()
            images_list.append(image)
            if image.get_height() > max_height:
                max_height = image.get_height()
            if image.get_width() > max_width:
                max_width = image.get_width()


        image_target = pygame.Surface((max_width * cols, max_height * rows), pygame.SRCALPHA)
        current_index = 0
        for row in range(rows):
            for col in range(cols):
                if current_index < len(images_list):
                    image_target.blit(images_list[current_index], (col * max_height, row*max_height))
                    current_index += 1

        pygame.image.save(image_target, target_file)

        pygame.quit()
        return f'Output file created, tile size is Width: {max_width}, Height: {max_height}'

    @staticmethod
    def get_suggested_layout(amount_of_images: int) -> ():

        if amount_of_images <= 0:
            return 0, 0

        columns = math.ceil(math.sqrt(amount_of_images))
        rows = math.ceil(amount_of_images / columns)

        return columns, rows


if __name__ == '__main__':
    result = ImagePacker().pack(ImagePacker.SOURCE_FOLDER, ImagePacker.TARGET_FILE, ImagePacker.OUTPUT_COL,ImagePacker.OUTPUT_ROW)
    print(result)
