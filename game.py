import pygame


class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False

    def draw(self):

        pygame.display.flip()

    def run_loop(self):
        while self.game_state.running:

            self.handle_events()
            self.draw()
