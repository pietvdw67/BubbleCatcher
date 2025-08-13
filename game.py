import pygame

from player.Player import Player


class Game:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.clock = pygame.time.Clock()
        self.sprite_groups = {
            "players": pygame.sprite.Group()
        }

        self.players = []
        self.players.append(Player("VirtualGuy", 100, 100))
        self.players.append(Player("NinjaFrog", 400, 100))
        self.players.append(Player("PinkMan", 100, 300))

        self.sprite_groups["players"].add(self.players[0])
        self.sprite_groups["players"].add(self.players[1])
        self.sprite_groups["players"].add(self.players[2])

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        self.players[0].vel[0] = 0
        vel = self.players[0].vel
        self.players[1].vel[0] = 0
        vel = self.players[1].vel
        self.players[2].vel[0] = 0
        vel = self.players[2].vel
        if keys[pygame.K_d]:
            self.players[0].direction = "right"
            self.players[0].vel[0] = 1
        if keys[pygame.K_a]:
            self.players[0].direction = "left"
            self.players[0].vel[0] = -1
        if keys[pygame.K_RIGHT]:
            self.players[1].direction = "right"
            self.players[1].vel[0] = 1
        if keys[pygame.K_LEFT]:
            self.players[1].direction = "left"
            self.players[1].vel[0] = -1
        if keys[pygame.K_l]:
            self.players[2].direction = "right"
            self.players[2].vel[0] = 1
        if keys[pygame.K_j]:
            self.players[2].direction = "left"
            self.players[2].vel[0] = -1


    def draw(self):
        self.screen.fill((0, 0, 0))

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

