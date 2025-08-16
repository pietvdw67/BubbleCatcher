import pygame
import os
import random

from players.player import Player
from players.player_constants import PlayerConstants
from constants import Constants
from utils.image_utils import ImageUtils
from platforms.platform import Platform
from balls.ball import Ball

pygame.font.init()


class Game:

    SCORE_FONT = pygame.font.SysFont("comicsans", 30)

    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state

        self.game_state.players.append(Player("left", "VirtualGuy", pygame.math.Vector2(100, PlayerConstants.PLAYER_GROUND_HEIGHT)))
        self.game_state.players.append(
            Player("right", "PinkMan", pygame.math.Vector2(500, PlayerConstants.PLAYER_GROUND_HEIGHT)))
        self.game_state.sprite_groups["players"].add(self.game_state.players[0])
        self.game_state.sprite_groups["players"].add(self.game_state.players[1])
        self.background_image = None
        self.build_background_image()
        self.build_platforms()

        self.game_state.balls.append(Ball(self.game_state, pygame.math.Vector2(Constants.WIDTH // 2 - 100, 50),"blue"))
        self.game_state.balls.append(Ball(self.game_state, pygame.math.Vector2(Constants.WIDTH // 2 - 150, 100), "red"))
        self.game_state.sprite_groups["balls"].add(self.game_state.balls[0])
        self.game_state.sprite_groups["balls"].add(self.game_state.balls[1])

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
                    self.game_state.players[0].jump()

                if event.key == pygame.K_RCTRL:
                    self.game_state.players[1].jump()

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        for player in  self.game_state.players:
            player.acceleration.x = 0

        if keys[pygame.K_d]:
            self.game_state.players[0].acceleration.x = PlayerConstants.PLAYER_ACCELERATION
        if keys[pygame.K_a]:
            self.game_state.players[0].acceleration.x = -PlayerConstants.PLAYER_ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.game_state.players[1].acceleration.x = PlayerConstants.PLAYER_ACCELERATION
        if keys[pygame.K_LEFT]:
            self.game_state.players[1].acceleration.x = -PlayerConstants.PLAYER_ACCELERATION

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_background(self.screen)

        score_left = Game.SCORE_FONT.render(f"Score: {self.game_state.score_left}", 1, "black")
        self.screen.blit(score_left, (10, 10))
        score_right = Game.SCORE_FONT.render(f"Score: {self.game_state.score_right}", 1, "black")
        self.screen.blit(score_right, (Constants.WIDTH - score_right.get_width() -10, 10))

        self.game_state.sprite_groups["platforms"].draw(self.screen)
        self.game_state.sprite_groups["players"].draw(self.screen)
        self.game_state.sprite_groups["balls"].draw(self.screen)

        pygame.display.flip()

    def run_loop(self):
        while self.game_state.running:
            dt = self.game_state.clock.tick(60) / 1000.0

            self.handle_events()
            self.handle_keys()
            for player in  self.game_state.players:
                player.move(dt)

            self.game_state.sprite_groups["players"].update()
            self.game_state.sprite_groups["platforms"].update()
            self.game_state.sprite_groups["balls"].update()

            for player in self.game_state.players:
                hits = pygame.sprite.spritecollide(player,  self.game_state.sprite_groups["platforms"], False)
                if hits and player.velocity.y > 0:

                    player.position.y = hits[0].rect.top + 1 - player.rect.height
                    player.velocity.y = 0
                    player.on_ground = True

                    if hasattr(hits[0], 'is_moving') and hits[0].is_moving:
                        player.position.x += hits[0].current_moving_speed

            for ball in self.game_state.balls:
                hits = pygame.sprite.spritecollide(ball, self.game_state.sprite_groups["platforms"], False)

                if hits:
                    if ball.velocity.x > 0 and self.is_close_corner(hits[0].rect.topleft, ball.rect.bottomright):
                        ball.velocity.x *= -1
                        ball.velocity.y *= -1
                    elif ball.velocity.x > 0 and self.is_close_corner(hits[0].rect.bottomleft, ball.rect.topright):
                        ball.velocity.x *= -1
                        ball.velocity.y *= -1
                    elif ball.velocity.x > 0 and abs(hits[0].rect.left - ball.rect.right) < 3:
                        ball.velocity.x *= -1
                    elif ball.velocity.x < 0 and self.is_close_corner(hits[0].rect.topright, ball.rect.bottomleft):
                        ball.velocity.x *= -1
                        ball.velocity.y *= -1
                    elif ball.velocity.x < 0 and self.is_close_corner(hits[0].rect.bottomright, ball.rect.topleft):
                        ball.velocity.x *= -1
                        ball.velocity.y *= -1
                    elif ball.velocity.x < 0 and abs(hits[0].rect.right - ball.rect.left) < 3:
                        ball.velocity.x *= -1

                    elif ball.velocity.y > 0 and abs(hits[0].rect.top - ball.rect.bottom) < 10:
                        ball.velocity.y *= -1
                    elif ball.velocity.y < 0 and abs(hits[0].rect.bottom - ball.rect.top) < 10:
                        ball.velocity.y *= -1

            for player in self.game_state.players:
                hits = pygame.sprite.spritecollide(player,  self.game_state.sprite_groups["balls"], True)
                if hits:
                    if hits[0].color == "blue":
                        self.game_state.score_left += 1
                    if hits[0].color == "red":
                        self.game_state.score_right += 1

                    if hits[0].color == "yellow":
                        if player.name == "left":
                            self.game_state.score_left += 5
                        else:
                            self.game_state.score_right += 5

                    for ball in self.game_state.balls[:]:
                        if ball.color == hits[0].color:
                            self.game_state.balls.remove(ball)

                    if not hits[0].color == "yellow":
                        self.respawn_ball(hits[0].color)

            self.draw()

    def respawn_ball(self, color):

        x_spawn_pos = random.choice([100, Constants.WIDTH - 100])

        ball = Ball(self.game_state, pygame.math.Vector2(x_spawn_pos, 50), color)
        self.game_state.balls.append(ball)
        self.game_state.sprite_groups["balls"].add(ball)

        if len(self.game_state.balls) == 2:
            spawn_yellow_chance = random.randint(1, 10)
            if spawn_yellow_chance < 3:
                ball = Ball(self.game_state, pygame.math.Vector2(Constants.WIDTH // 2 -100, 50), "yellow")
                self.game_state.balls.append(ball)
                self.game_state.sprite_groups["balls"].add(ball)


    def is_close_corner(self, corner_fist, corner_second):
        diffx = abs(corner_fist[0] - corner_second[0])
        diffy = abs(corner_fist[1] - corner_second[1])

        return diffx < 3 and diffy < 3

    def build_platforms(self):

        platform = Platform(pygame.math.Vector2(75, 450), 4)
        platform.set_images(
            os.path.join("assets", "terrain", "terrain.png"),
            128, 128,
            pygame.math.Vector2(0, 384),
            pygame.math.Vector2(128, 384),
            pygame.math.Vector2(256, 384),
            0.5)

        self.game_state.sprite_groups["platforms"].add(platform)

        platform = Platform(pygame.math.Vector2(625,  450), 4)
        platform.set_images(
            os.path.join("assets", "terrain", "terrain.png"),
            128, 128,
            pygame.math.Vector2(0, 384),
            pygame.math.Vector2(128, 384),
            pygame.math.Vector2(256, 384),
            0.5)

        self.game_state.sprite_groups["platforms"].add(platform)

        platform = Platform(pygame.math.Vector2(150,  250), 6, is_moving=True, move_range=325, move_speed=1)
        platform.set_images(
            os.path.join("assets", "terrain", "terrain.png"),
            128, 128,
            pygame.math.Vector2(0, 384),
            pygame.math.Vector2(128, 384),
            pygame.math.Vector2(256, 384),
            0.5)

        self.game_state.sprite_groups["platforms"].add(platform)


