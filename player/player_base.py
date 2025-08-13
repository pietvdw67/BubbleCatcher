import pygame


class PlayerBase(pygame.sprite.Sprite):

    def __init__(self, name, x_pos, y_pos):

        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 200
        self.health = 100
        self.direction = "right"
        self.rect = None
        self.image = None
        self.animations = {}
        self.animations_delays = {}
        self._animation_active = None
        self._animation_active_previous = None
        self.animation_frame_index = 0
        self._animation_delay_count = 0

    def update(self):
        pygame.sprite.Sprite.update(self)

        self._set_animation_frame()

        self.image = self.animations[self._animation_active][self.animation_frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def move(self, dt):

        if self.vel.x > 0:
            self.direction = "right"
        if self.vel.x < 0:
            self.direction = "left"

        self.x_pos += self.vel[0] * self.speed * dt
        self.y_pos += self.vel[1] * self.speed * dt

    def set_animation_active(self, active_name):
        if not self._animation_active_previous:
            self._animation_active_previous = active_name
            self._animation_active = active_name
            self.animation_frame_index = 0
            return

        if self._animation_active_previous != active_name:
            self._animation_active_previous = active_name
            self._animation_active = active_name
            self.animation_frame_index = 0


    def _set_animation_frame(self):

        self._animation_delay_count += 1
        if self._animation_delay_count < self.animations_delays[self._animation_active]:
            return

        self._animation_delay_count = 0
        self.animation_frame_index += 1
        if self.animation_frame_index >= len(self.animations[self._animation_active]):
            self.animation_frame_index = 0
