import pygame
import os

pygame.init()


class ImagePacker:

    SOURCE_FOLDER = 'D:/DEV/Python/learn/gamedev/BubbleCatcher/assets/tmpinput'
    TARGET_FILE = '/assets/tmpoutput/terrain.png'
    OUTPUT_COL = 5
    OUTPUT_ROW = 5

    def __init__(self):
        screen_width, screen_height = 800, 600
        screen = pygame.display.set_mode((screen_width, screen_height))

    def pack(self):
        entries = os.listdir(ImagePacker.SOURCE_FOLDER)
        images_list = []
        max_height = 0
        max_width = 0
        for entry in entries:
            file_name = os.path.join(ImagePacker.SOURCE_FOLDER, entry)
            image = pygame.image.load(file_name).convert_alpha()
            images_list.append(image)
            if image.get_height() > max_height:
                max_height = image.get_height()
            if image.get_width() > max_width:
                max_width = image.get_width()


        image_target = pygame.Surface((max_width * ImagePacker.OUTPUT_COL, max_height * ImagePacker.OUTPUT_ROW), pygame.SRCALPHA)
        current_index = 0
        for row in range(ImagePacker.OUTPUT_ROW):
            for col in range(ImagePacker.OUTPUT_COL):
                if current_index < len(images_list):
                    image_target.blit(images_list[current_index], (col * max_height, row*max_height))
                    current_index += 1

        pygame.image.save(image_target, ImagePacker.TARGET_FILE)
        print(f'Output file created, tile size is Width: {max_width}, Height: {max_height}')

















if __name__ == '__main__':
    ImagePacker().pack()




