import pygame

from game_state import GameState
from game import Game
from constants import Constants

pygame.init()


class Main:
    def __init__(self):
        self.game_state = GameState()
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        pygame.display.set_caption("Bubble Catcher")

    def run(self):
        self.start_game()

        pygame.quit()
        exit()

    def start_game(self):
        self.game_state.running = True
        game = Game(self.screen, self.game_state)
        game.run_loop()


if __name__ == '__main__':
    Main().run()
