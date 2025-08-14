import pygame
import os

from player.Player import Player
from constants import Constants
from utils.image_utils import ImageUtils

class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.clock = pygame.time.Clock()
        self.sprite_groups = {
            "players": pygame.sprite.Group(),
        }

        self.players = []
        self.players.append(Player("VirtualGuy", 100, Constants.PLAYER_GROUND_HEIGHT))
        self.sprite_groups["players"].add(self.players[0])
        self.background_image = None
        self.build_background_image()

    def build_background_image(self):
        self.background_image = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        background_tile = pygame.image.load(os.path.join("assets", "background", "Blue.png"))
        rows = Constants.WIDTH // background_tile.get_width() + 1
        cols = Constants.HEIGHT // background_tile.get_height() + 10
        for row in range(rows):
            for col in range(cols):
                self.background_image.blit(background_tile, (col * background_tile.get_width(), row * background_tile.get_height()))

    def draw_background(self, screen):

        # Draw the background image created from individual tiles
        screen.blit(self.background_image, (0,0))

        # Draw the terrain floor
        image_count = Constants.WIDTH // Constants.TILE_SIZE + 1
        ground_image_path = os.path.join("assets", "terrain", "terrain.png")
        image = ImageUtils.get_image_from_sprite_sheet(ground_image_path, Constants.TILE_SIZE,0, Constants.TILE_SIZE*2, Constants.TILE_SIZE)

        for i in range(image_count):
            screen.blit(image, (i * image.get_width(), Constants.HEIGHT - image.get_height()))

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        self.players[0].vel[0] = 0
        vel = self.players[0].vel

        if keys[pygame.K_d]:
            self.players[0].direction = "right"
            self.players[0].vel[0] = 1
        if keys[pygame.K_a]:
            self.players[0].direction = "left"
            self.players[0].vel[0] = -1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_background(self.screen)

        self.sprite_groups["players"].draw(self.screen)

        pygame.display.flip()

    def run_loop(self):
        while self.game_state.running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.handle_keys()
            for player in self.players:
                player.move(dt)
            self.sprite_groups["players"].update()

            self.draw()

