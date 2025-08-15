import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Game Constants ---
# Screen dimensions
WIDTH, HEIGHT = 800, 600
FLOOR_HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player constants
PLAYER_SIZE = 32
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_STRENGTH = -12

# Ball constants
BALL_SIZE = 20
BALL_SPEED = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Frame rate
FPS = 60
clock = pygame.time.Clock()


# --- Pygame Classes ---

# A class for the player character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create the player surface and get its rectangle for positioning
        self.surf = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect()

        # We use a vector for position, velocity, and acceleration
        # This is a good way to handle physics in a 2D game
        self.position = pygame.Vector2((100, HEIGHT - FLOOR_HEIGHT - PLAYER_SIZE))
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.on_ground = True  # A flag to check if the player is on the ground

    def update(self, platforms):
        # Reset horizontal acceleration to 0
        self.acceleration.x = 0

        # --- Handle player input for movement ---
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if pressed_keys[pygame.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION

        # --- Apply gravity ---
        # The core of gravity is a constant downward acceleration.
        # We add a positive value to the y-acceleration in every frame.
        # In Pygame, a larger y value means lower on the screen.
        self.acceleration.y = PLAYER_GRAVITY

        # --- Physics calculations ---
        # Apply friction to slow the player down when not moving
        # We multiply by friction, which is a negative value, to oppose velocity
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION

        # Update velocity based on acceleration
        self.velocity += self.acceleration

        # Update position based on velocity
        self.position += self.velocity

        # Clamp player position to screen boundaries
        if self.position.x < PLAYER_SIZE // 2:
            self.position.x = PLAYER_SIZE // 2
            self.velocity.x = 0
        if self.position.x > WIDTH - PLAYER_SIZE // 2:
            self.position.x = WIDTH - PLAYER_SIZE // 2
            self.velocity.x = 0

        # Update the rectangle's position to match the player's position vector
        self.rect.midbottom = self.position

    def jump(self):
        # We can only jump if we are on the ground
        if self.on_ground:
            # Set a negative y velocity to move the player upwards
            self.velocity.y = PLAYER_JUMP_STRENGTH
            self.on_ground = False

    def check_collisions(self, platforms):
        # Get a list of all sprites the player has collided with
        hits = pygame.sprite.spritecollide(self, platforms, False)

        # The key to collision is to handle it *after* updating the position.
        # This prevents the player from "phasing" through platforms at high speeds.

        # --- Handle floor/platform collision ---
        # If there's a collision and the player is moving downwards (positive y velocity)
        # and not jumping
        if hits and self.velocity.y > 0:
            # Snap the player to the top of the platform they hit
            # This is crucial to prevent the player from sinking into the ground
            self.position.y = hits[0].rect.top + 1
            self.velocity.y = 0  # Stop all vertical movement
            self.on_ground = True  # Set the flag so we can jump again
            # If the platform is moving, the player should move with it
            if hasattr(hits[0], 'is_moving') and hits[0].is_moving:
                self.position.x += hits[0].move_speed * hits[0].move_direction


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, is_moving=False, move_range=0):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(topleft=(x, y))

        # New attributes for moving platforms
        self.is_moving = is_moving
        self.move_range = move_range
        self.move_speed = 0.8  # Decreased speed for a slower movement
        self.move_direction = 1  # 1 for right, -1 for left
        self.start_x = x

    def update(self):
        if self.is_moving:
            self.rect.x += self.move_speed * self.move_direction
            # Check if the platform has moved past its boundaries
            if self.move_direction == 1 and self.rect.right > self.start_x + self.move_range:
                self.move_direction = -1
            if self.move_direction == -1 and self.rect.left < self.start_x:
                self.move_direction = 1


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(center=(random.randint(BALL_SIZE, WIDTH - BALL_SIZE),
                                               random.randint(BALL_SIZE, HEIGHT - FLOOR_HEIGHT - BALL_SIZE)))
        # Random starting velocity
        self.velocity = pygame.Vector2(random.choice([-BALL_SPEED, BALL_SPEED]),
                                       random.choice([-BALL_SPEED, BALL_SPEED]))
        # We'll use a position vector for more precise movement
        self.position = pygame.Vector2(self.rect.center)

    def update(self, platforms):
        # --- Move the ball and check for collisions on each axis separately ---

        # Update the horizontal position
        self.position.x += self.velocity.x
        self.rect.center = self.position

        # Check for horizontal bouncing off the screen edges
        if self.rect.left <= 0:
            self.rect.left = 0
            self.velocity.x *= -1
            self.position = pygame.Vector2(self.rect.center)
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.velocity.x *= -1
            self.position = pygame.Vector2(self.rect.center)

        # Check for horizontal bouncing off platforms
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            # Move the ball out of the platform before reversing velocity
            if self.velocity.x > 0:  # Moving right, hit left side of platform
                self.rect.right = hits[0].rect.left
            else:  # Moving left, hit right side of platform
                self.rect.left = hits[0].rect.right
            self.velocity.x *= -1
            self.position = pygame.Vector2(self.rect.center)

        # Update the vertical position
        self.position.y += self.velocity.y
        self.rect.center = self.position

        # Check for vertical bouncing off the screen edges
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y *= -1
            self.position = pygame.Vector2(self.rect.center)
        if self.rect.bottom >= HEIGHT - FLOOR_HEIGHT:
            self.rect.bottom = HEIGHT - FLOOR_HEIGHT
            self.velocity.y *= -1
            self.position = pygame.Vector2(self.rect.center)

        # Check for vertical bouncing off platforms
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            # Move the ball out of the platform before reversing velocity
            if self.velocity.y > 0:  # Moving down, hit top side of platform
                self.rect.bottom = hits[0].rect.top
            else:  # Moving up, hit bottom side of platform
                self.rect.top = hits[0].rect.bottom
            self.velocity.y *= -1
            self.position = pygame.Vector2(self.rect.center)

    def respawn(self):
        # Reset the ball's position to a new random location
        self.rect.center = (random.randint(BALL_SIZE, WIDTH - BALL_SIZE),
                            random.randint(BALL_SIZE, HEIGHT - FLOOR_HEIGHT - BALL_SIZE))
        # Give it a new random velocity
        self.velocity = pygame.Vector2(random.choice([-BALL_SPEED, BALL_SPEED]),
                                       random.choice([-BALL_SPEED, BALL_SPEED]))
        self.position = pygame.Vector2(self.rect.center)


# --- Game Setup ---
# Create the sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
balls = pygame.sprite.Group()

# Create the player and add to the sprite group
player = Player()
all_sprites.add(player)

# Create the ground platform and add to sprite groups
ground = Platform(0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT)
platforms.add(ground)
all_sprites.add(ground)

# Add more platforms for the player to jump on
platform_data = [
    (150, 450, 150, 20),
    (400, 350, 150, 20),
    (600, 250, 150, 20),
]

# Create a moving platform and add it to the groups
moving_platform = Platform(150, 450, 150, 20, is_moving=True, move_range=400)
platforms.add(moving_platform)
all_sprites.add(moving_platform)

# Create the static platforms
static_platforms_data = [
    (400, 350, 150, 20),
    (600, 250, 150, 20),
]
for plat in static_platforms_data:
    p = Platform(plat[0], plat[1], plat[2], plat[3])
    platforms.add(p)
    all_sprites.add(p)

# Create the ball and add to sprite groups
ball = Ball()
balls.add(ball)
all_sprites.add(ball)

# --- Game Loop ---
running = True
while running:
    # Set the frame rate
    clock.tick(FPS)

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # --- Update game objects ---
    # Update all platforms, including the moving one
    for p in platforms:
        p.update()
    player.update(platforms)
    player.check_collisions(platforms)
    ball.update(platforms)

    # Check for player and ball collision
    if pygame.sprite.spritecollide(player, balls, False):
        score += 1
        ball.respawn()

    # --- Drawing ---
    screen.fill(BLACK)

    # Draw all the sprites
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # Render and draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# --- Quit Pygame ---
pygame.quit()
sys.exit()
