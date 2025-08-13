import pygame

from player.Player import Player


class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.sprite_groups = {
            "players": pygame.sprite.Group()
        }

        self.sprite_groups["players"].add(Player("left_player", 100, 100))
        self.sprite_groups["players"].add(Player("right_player", 400, 100))


    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False

    def draw(self):

        self.sprite_groups["players"].draw(self.screen)

        pygame.display.flip()

    def run_loop(self):
        while self.game_state.running:

            self.handle_events()

            self.sprite_groups["players"].update()

            self.draw()
