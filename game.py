import pygame
import os

from players.player import Player
from players.player_constants import PlayerConstants
from constants import Constants
from utils.image_utils import ImageUtils
from platforms.platform import Platform
from balls.ball import Ball


class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.clock = pygame.time.Clock()
        self.sprite_groups = {
            "players": pygame.sprite.Group(),
            "platforms": pygame.sprite.Group(),
            "balls": pygame.sprite.Group()
        }

        self.players = []
        self.players.append(Player("VirtualGuy", pygame.math.Vector2(100, PlayerConstants.PLAYER_GROUND_HEIGHT)))
        self.sprite_groups["players"].add(self.players[0])
        self.background_image = None
        self.build_background_image()
        self.build_platforms()

        self.balls = []
        self.balls.append(Ball(pygame.math.Vector2(Constants.WIDTH // 2 - 100, 50),"blue"))
        self.balls.append(Ball(pygame.math.Vector2(Constants.WIDTH // 2 - 100, 100), "red"))
        self.balls.append(Ball(pygame.math.Vector2(Constants.WIDTH // 2 - 150, 80), "yellow"))
        self.sprite_groups["balls"].add(self.balls[0])
        self.sprite_groups["balls"].add(self.balls[1])
        self.sprite_groups["balls"].add(self.balls[2])


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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.players[0].jump()

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        for player in self.players:
            player.acceleration.x = 0

        if keys[pygame.K_d]:
            self.players[0].acceleration.x = PlayerConstants.PLAYER_ACCELERATION
        if keys[pygame.K_a]:
            self.players[0].acceleration.x = -PlayerConstants.PLAYER_ACCELERATION

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_background(self.screen)

        self.sprite_groups["platforms"].draw(self.screen)
        self.sprite_groups["players"].draw(self.screen)
        self.sprite_groups["balls"].draw(self.screen)

        pygame.display.flip()

    def run_loop(self):
        while self.game_state.running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.handle_keys()
            for player in self.players:
                player.move(dt)

            self.sprite_groups["players"].update()
            self.sprite_groups["platforms"].update()
            self.sprite_groups["balls"].update()

            for player in self.players:
                hits = pygame.sprite.spritecollide(player, self.sprite_groups["platforms"], False)
                if hits and player.velocity.y > 0:

                    player.position.y = hits[0].rect.top + 1 - player.rect.height
                    player.velocity.y = 0
                    player.on_ground = True

                    if hasattr(hits[0], 'is_moving') and hits[0].is_moving:
                        player.position.x += hits[0].current_moving_speed


            self.draw()

    def build_platforms(self):

        platform = Platform(pygame.math.Vector2(75, 450), 4)
        platform.set_images(
            os.path.join("assets", "terrain", "terrain.png"),
            128, 128,
            pygame.math.Vector2(0, 384),
            pygame.math.Vector2(128, 384),
            pygame.math.Vector2(256, 384),
            0.5)

        self.sprite_groups["platforms"].add(platform)

        platform = Platform(pygame.math.Vector2(625,  450), 4)
        platform.set_images(
            os.path.join("assets", "terrain", "terrain.png"),
            128, 128,
            pygame.math.Vector2(0, 384),
            pygame.math.Vector2(128, 384),
            pygame.math.Vector2(256, 384),
            0.5)

        self.sprite_groups["platforms"].add(platform)

        platform = Platform(pygame.math.Vector2(150,  250), 6, is_moving=True, move_range=325, move_speed=1)
        platform.set_images(
            os.path.join("assets", "terrain", "terrain.png"),
            128, 128,
            pygame.math.Vector2(0, 384),
            pygame.math.Vector2(128, 384),
            pygame.math.Vector2(256, 384),
            0.5)

        self.sprite_groups["platforms"].add(platform)


