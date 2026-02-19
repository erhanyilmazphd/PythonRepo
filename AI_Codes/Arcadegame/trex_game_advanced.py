import pygame
import random
import sys
from enum import Enum
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 0, 139)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
SKY_BLUE = (135, 206, 235)
SAND = (238, 214, 175)
DARK_SAND = (210, 180, 140)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced T-Rex Runner Game")

# Font
font_large = pygame.font.Font(None, 70)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 35)
font_tiny = pygame.font.Font(None, 25)


class GameState(Enum):
    MENU = 1
    CHARACTER_SELECT = 2
    BACKGROUND_SELECT = 3
    PLAYING = 4
    GAME_OVER = 5
    PAUSE = 6


class Background:
    def __init__(self, bg_type):
        self.type = bg_type
        self.scroll_offset = 0
        self.parallax_offset = 0
        
    def draw(self, surface):
        if self.type == "desert":
            self.draw_desert(surface)
        elif self.type == "jungle":
            self.draw_jungle(surface)
        elif self.type == "snow":
            self.draw_snow(surface)
        elif self.type == "volcano":
            self.draw_volcano(surface)
        elif self.type == "space":
            self.draw_space(surface)
        elif self.type == "night":
            self.draw_night(surface)
    
    def draw_desert(self, surface):
        surface.fill(SAND)
        # Sun
        pygame.draw.circle(surface, YELLOW, (SCREEN_WIDTH - 100, 80), 40)
        # Sand dunes
        pygame.draw.polygon(surface, DARK_SAND, [(0, SCREEN_HEIGHT - 100), (150, SCREEN_HEIGHT - 150), (300, SCREEN_HEIGHT - 100)])
        pygame.draw.polygon(surface, DARK_SAND, [(250, SCREEN_HEIGHT - 100), (400, SCREEN_HEIGHT - 140), (550, SCREEN_HEIGHT - 100)])
        # Ground line
        pygame.draw.line(surface, DARK_SAND, (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 3)
    
    def draw_jungle(self, surface):
        surface.fill((50, 150, 50))
        # Trees
        pygame.draw.rect(surface, BROWN, (100, 250, 20, 100))
        pygame.draw.polygon(surface, GREEN, [(60, 250), (110, 150), (160, 250)])
        pygame.draw.rect(surface, BROWN, (400, 280, 25, 80))
        pygame.draw.polygon(surface, GREEN, [(350, 280), (412, 160), (475, 280)])
        # Vines
        for i in range(0, SCREEN_WIDTH, 80):
            pygame.draw.line(surface, (34, 100, 34), (i, 100), (i + 20, 200), 3)
        # Ground line
        pygame.draw.line(surface, (30, 100, 30), (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 3)
    
    def draw_snow(self, surface):
        surface.fill((220, 230, 250))
        # Snow-covered mountains
        pygame.draw.polygon(surface, WHITE, [(0, SCREEN_HEIGHT - 100), (250, 100), (500, SCREEN_HEIGHT - 100)])
        pygame.draw.polygon(surface, WHITE, [(400, SCREEN_HEIGHT - 100), (650, 150), (900, SCREEN_HEIGHT - 100)])
        # Snow particles
        for i in range(0, SCREEN_WIDTH, 100):
            pygame.draw.circle(surface, WHITE, (i + 50, 50), 5)
            pygame.draw.circle(surface, WHITE, (i + 30, 150), 4)
        # Ground
        pygame.draw.line(surface, LIGHT_GRAY, (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 3)
    
    def draw_volcano(self, surface):
        surface.fill((100, 50, 50))
        # Volcano
        pygame.draw.polygon(surface, (80, 40, 40), [(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 100), (SCREEN_WIDTH // 2, 100), (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT - 100)])
        # Lava
        pygame.draw.polygon(surface, RED, [(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100), (SCREEN_WIDTH // 2, 150), (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT - 100)])
        # Ground line
        pygame.draw.line(surface, (60, 30, 30), (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 3)
    
    def draw_space(self, surface):
        surface.fill(BLACK)
        # Stars
        random.seed(42)
        for i in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT - 100)
            pygame.draw.circle(surface, WHITE, (x, y), 1)
        # Planet
        pygame.draw.circle(surface, BLUE, (SCREEN_WIDTH - 150, 80), 50)
        # Ground line (metal platform)
        pygame.draw.rect(surface, DARK_GRAY, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
        pygame.draw.line(surface, CYAN, (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 3)
    
    def draw_night(self, surface):
        surface.fill((30, 30, 50))
        # Moon
        pygame.draw.circle(surface, YELLOW, (SCREEN_WIDTH - 100, 80), 45)
        pygame.draw.circle(surface, (30, 30, 50), (SCREEN_WIDTH - 110, 70), 40)
        # Stars
        random.seed(123)
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT - 100)
            pygame.draw.circle(surface, WHITE, (x, y), 2)
        # Ground line
        pygame.draw.line(surface, (50, 50, 70), (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 3)
    
    def update(self):
        self.scroll_offset += 1


class Character:
    def __init__(self, char_type):
        self.type = char_type
        self.width = 50
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.draw_character()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.vel_y = 0
        self.is_jumping = False
        self.jump_power = 15
        self.double_jump_available = False
        self.dash_available = False
        self.is_dashing = False
        self.dash_timer = 0

    def draw_character(self):
        self.image.fill(WHITE)
        if self.type == "trex":
            self.draw_trex()
        elif self.type == "pterodactyl":
            self.draw_pterodactyl()
        elif self.type == "raptor":
            self.draw_raptor()
        elif self.type == "robot":
            self.draw_robot()
        elif self.type == "robot_female":
            self.draw_robot_female()

    def draw_trex(self):
        # Body
        pygame.draw.rect(self.image, BROWN, (10, 20, 30, 30))
        # Head
        pygame.draw.circle(self.image, BROWN, (30, 15), 8)
        # Eye
        pygame.draw.circle(self.image, BLACK, (32, 13), 2)
        # Tail
        pygame.draw.polygon(self.image, BROWN, [(5, 30), (0, 25), (2, 35)])
        # Legs
        pygame.draw.rect(self.image, BROWN, (12, 50, 4, 10))
        pygame.draw.rect(self.image, BROWN, (25, 50, 4, 10))

    def draw_pterodactyl(self):
        # Head
        pygame.draw.circle(self.image, GREEN, (30, 20), 8)
        # Beak
        pygame.draw.polygon(self.image, GREEN, [(22, 20), (15, 18), (15, 22)])
        # Wings
        pygame.draw.polygon(self.image, GREEN, [(38, 20), (48, 10), (48, 30)])
        pygame.draw.polygon(self.image, GREEN, [(22, 20), (12, 10), (12, 30)])
        # Eye
        pygame.draw.circle(self.image, BLACK, (31, 18), 2)
        # Tail
        pygame.draw.polygon(self.image, GREEN, [(25, 28), (20, 50), (28, 48)])

    def draw_raptor(self):
        # Body
        pygame.draw.rect(self.image, RED, (12, 25, 26, 25))
        # Head
        pygame.draw.circle(self.image, RED, (32, 18), 7)
        # Eye
        pygame.draw.circle(self.image, YELLOW, (34, 16), 2)
        # Claw marks
        pygame.draw.polygon(self.image, DARK_GRAY, [(8, 35), (5, 40), (10, 38)])
        pygame.draw.polygon(self.image, DARK_GRAY, [(42, 35), (45, 40), (40, 38)])
        # Legs
        pygame.draw.rect(self.image, RED, (14, 50, 4, 10))
        pygame.draw.rect(self.image, RED, (28, 50, 4, 10))
        # Tail (curved)
        pygame.draw.polygon(self.image, RED, [(12, 28), (0, 20), (8, 35)])

    def draw_robot(self):
        # Body
        pygame.draw.rect(self.image, DARK_GRAY, (12, 20, 26, 30))
        # Head
        pygame.draw.rect(self.image, DARK_GRAY, (15, 8, 20, 12))
        # Eyes
        pygame.draw.rect(self.image, CYAN, (17, 10, 4, 4))
        pygame.draw.rect(self.image, CYAN, (29, 10, 4, 4))
        # Antenna
        pygame.draw.line(self.image, DARK_GRAY, (25, 8), (25, 2), 2)
        pygame.draw.circle(self.image, CYAN, (25, 2), 2)
        # Arms
        pygame.draw.rect(self.image, DARK_GRAY, (8, 22, 4, 20))
        pygame.draw.rect(self.image, DARK_GRAY, (38, 22, 4, 20))
        # Legs
        pygame.draw.rect(self.image, DARK_GRAY, (15, 50, 5, 10))
        pygame.draw.rect(self.image, DARK_GRAY, (30, 50, 5, 10))

    def draw_robot_female(self):
        # Body
        pygame.draw.rect(self.image, PURPLE, (12, 20, 26, 30))
        # Head
        pygame.draw.rect(self.image, PURPLE, (14, 5, 22, 15))
        # Eyes
        pygame.draw.circle(self.image, PINK, (18, 12), 3)
        pygame.draw.circle(self.image, PINK, (32, 12), 3)
        # Hair
        pygame.draw.polygon(self.image, PINK, [(14, 5), (18, 0), (22, 5)])
        pygame.draw.polygon(self.image, PINK, [(36, 5), (32, 0), (28, 5)])
        # Arms
        pygame.draw.rect(self.image, PURPLE, (8, 22, 4, 20))
        pygame.draw.rect(self.image, PURPLE, (38, 22, 4, 20))
        # Legs
        pygame.draw.rect(self.image, PURPLE, (15, 50, 5, 10))
        pygame.draw.rect(self.image, PURPLE, (30, 50, 5, 10))

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -self.jump_power
            self.double_jump_available = True
        elif self.double_jump_available and self.type in ["raptor", "robot_female"]:
            self.vel_y = -self.jump_power * 0.7
            self.double_jump_available = False

    def dash(self):
        if self.dash_available and self.type in ["raptor", "robot"]:
            self.is_dashing = True
            self.dash_timer = 10
            self.dash_available = False

    def update(self):
        # Apply gravity
        self.vel_y += 0.6
        self.rect.y += self.vel_y

        # Ground collision
        if self.rect.y >= SCREEN_HEIGHT - 100:
            self.rect.y = SCREEN_HEIGHT - 100
            self.is_jumping = False
            self.vel_y = 0
            self.dash_available = True

        # Dash animation
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False

    def draw(self, surface):
        if self.is_dashing:
            # Draw dashing effect
            self.image.set_alpha(150)
            surface.blit(self.image, self.rect)
            self.image.set_alpha(255)
        else:
            surface.blit(self.image, self.rect)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, powerup_type):
        super().__init__()
        self.type = powerup_type
        self.width = 25
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.draw_powerup()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - 150
        self.vel_x = -8
        self.float_offset = 0
        self.float_direction = 1

    def draw_powerup(self):
        if self.type == "shield":
            pygame.draw.circle(self.image, BLUE, (12, 12), 10)
            pygame.draw.circle(self.image, WHITE, (12, 12), 8)
        elif self.type == "speed_boost":
            pygame.draw.rect(self.image, YELLOW, (5, 8, 15, 9))
            pygame.draw.polygon(self.image, ORANGE, [(20, 12), (25, 15), (25, 9)])
        elif self.type == "coin":
            pygame.draw.circle(self.image, YELLOW, (12, 12), 10)
            pygame.draw.circle(self.image, ORANGE, (12, 12), 8)
            pygame.draw.line(self.image, YELLOW, (6, 12), (18, 12), 2)

    def update(self):
        self.rect.x += self.vel_x
        self.float_offset += self.float_direction
        if self.float_offset > 5:
            self.float_direction = -1
        elif self.float_offset < -5:
            self.float_direction = 1
        self.rect.y += self.float_direction * 0.5

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type, difficulty=1):
        super().__init__()
        self.type = obstacle_type
        self.width = 30
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.difficulty = difficulty
        
        if obstacle_type == "cactus":
            self.draw_cactus()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 105
        elif obstacle_type == "rock":
            self.draw_rock()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 95
        elif obstacle_type == "pterodactyl":
            self.draw_pterodactyl()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 170
            self.flap_counter = 0
        elif obstacle_type == "spikes":
            self.draw_spikes()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 100
        elif obstacle_type == "laser":
            self.draw_laser()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 150
            self.laser_height = 30

        self.vel_x = -8

    def draw_cactus(self):
        pygame.draw.rect(self.image, GREEN, (12, 10, 6, 30))
        pygame.draw.rect(self.image, GREEN, (5, 20, 6, 15))
        pygame.draw.rect(self.image, GREEN, (22, 20, 6, 15))
        pygame.draw.polygon(self.image, GREEN, [(12, 10), (9, 5), (15, 8)])

    def draw_rock(self):
        pygame.draw.circle(self.image, DARK_GRAY, (15, 20), 12)
        pygame.draw.circle(self.image, DARK_GRAY, (10, 28), 10)
        pygame.draw.circle(self.image, DARK_GRAY, (20, 32), 8)

    def draw_pterodactyl(self):
        pygame.draw.circle(self.image, GREEN, (15, 15), 6)
        pygame.draw.polygon(self.image, GREEN, [(10, 15), (5, 10), (5, 20)])
        pygame.draw.polygon(self.image, GREEN, [(21, 15), (28, 10), (28, 20)])
        pygame.draw.circle(self.image, BLACK, (16, 13), 2)

    def draw_spikes(self):
        for i in range(3):
            pygame.draw.polygon(self.image, RED, [(5 + i * 10, 35), (8 + i * 10, 15), (11 + i * 10, 35)])

    def draw_laser(self):
        pygame.draw.rect(self.image, RED, (8, 10, 14, 3))
        pygame.draw.circle(self.image, RED, (15, 20), 5)
        pygame.draw.line(self.image, RED, (15, 25), (15, 45), 2)

    def update(self):
        self.rect.x += self.vel_x
        if self.type == "pterodactyl":
            self.flap_counter += 1
            if self.flap_counter > 10:
                self.rect.y += random.choice([-2, 2])
                self.flap_counter = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Particle:
    def __init__(self, x, y, vel_x, vel_y, color, lifetime):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.radius = 3

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2
        self.lifetime -= 1

    def draw(self, surface):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = self.color
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        return self.lifetime > 0


class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.character = None
        self.character_type = "trex"
        self.background = None
        self.background_type = "desert"
        self.obstacles = []
        self.powerups = []
        self.particles = []
        self.score = 0
        self.coins = 0
        self.game_speed = 8
        self.spawn_timer = 0
        self.spawn_rate = 80
        self.high_score = 0
        self.combo = 0
        self.combo_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.difficulty = 1
        self.character_options = ["trex", "pterodactyl", "raptor", "robot", "robot_female"]
        self.background_options = ["desert", "jungle", "snow", "volcano", "space", "night"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.CHARACTER_SELECT
                elif self.state == GameState.CHARACTER_SELECT:
                    if event.key == pygame.K_LEFT:
                        idx = self.character_options.index(self.character_type)
                        self.character_type = self.character_options[(idx - 1) % len(self.character_options)]
                    elif event.key == pygame.K_RIGHT:
                        idx = self.character_options.index(self.character_type)
                        self.character_type = self.character_options[(idx + 1) % len(self.character_options)]
                    elif event.key == pygame.K_SPACE:
                        self.state = GameState.BACKGROUND_SELECT
                elif self.state == GameState.BACKGROUND_SELECT:
                    if event.key == pygame.K_LEFT:
                        idx = self.background_options.index(self.background_type)
                        self.background_type = self.background_options[(idx - 1) % len(self.background_options)]
                    elif event.key == pygame.K_RIGHT:
                        idx = self.background_options.index(self.background_type)
                        self.background_type = self.background_options[(idx + 1) % len(self.background_options)]
                    elif event.key == pygame.K_SPACE:
                        self.start_game()
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.character.jump()
                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.character.dash()
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSE
                elif self.state == GameState.PAUSE:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.CHARACTER_SELECT
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        return True

    def start_game(self):
        self.state = GameState.PLAYING
        self.character = Character(self.character_type)
        self.background = Background(self.background_type)
        self.obstacles = []
        self.powerups = []
        self.particles = []
        self.score = 0
        self.coins = 0
        self.game_speed = 8
        self.spawn_timer = 0
        self.spawn_rate = 80
        self.combo = 0
        self.combo_timer = 0
        self.shield_active = False
        self.speed_boost_active = False
        self.difficulty = 1

    def update(self):
        if self.state == GameState.PLAYING:
            self.character.update()
            self.background.update()

            # Update powerup timers
            if self.shield_active:
                self.shield_timer -= 1
                if self.shield_timer <= 0:
                    self.shield_active = False
            
            if self.speed_boost_active:
                self.speed_boost_timer -= 1
                if self.speed_boost_timer <= 0:
                    self.speed_boost_active = False
                    self.game_speed = max(8, self.game_speed - 3)

            # Update combo
            if self.combo_timer > 0:
                self.combo_timer -= 1
            else:
                self.combo = 0

            # Spawn obstacles
            self.spawn_timer += 1
            spawn_rate = max(40, self.spawn_rate - int(self.difficulty * 5))
            if self.spawn_timer >= spawn_rate:
                obstacle_types = ["cactus", "rock"]
                if self.score > 5:
                    obstacle_types.append("pterodactyl")
                if self.score > 15:
                    obstacle_types.append("spikes")
                if self.score > 30:
                    obstacle_types.append("laser")
                
                obstacle_type = random.choice(obstacle_types)
                new_obstacle = Obstacle(obstacle_type, self.difficulty)
                new_obstacle.vel_x = -(self.game_speed + (3 if self.speed_boost_active else 0))
                self.obstacles.append(new_obstacle)
                self.spawn_timer = 0
            
            # Spawn powerups occasionally
            if random.randint(0, 1000) < 5:
                powerup_type = random.choice(["shield", "speed_boost", "coin"])
                new_powerup = PowerUp(SCREEN_WIDTH, powerup_type)
                new_powerup.vel_x = -self.game_speed
                self.powerups.append(new_powerup)

            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()

                # Check collision
                if pygame.sprite.spritecollide(self.character, [obstacle], False):
                    if self.shield_active:
                        self.shield_active = False
                        self.obstacles.remove(obstacle)
                        self.create_particles(self.character.rect.centerx, self.character.rect.centery, BLUE)
                    else:
                        self.state = GameState.GAME_OVER
                        if self.score > self.high_score:
                            self.high_score = self.score

                # Remove off-screen obstacles
                if obstacle.rect.x < -obstacle.width:
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.combo += 1
                    self.combo_timer = 60

            # Update powerups
            for powerup in self.powerups[:]:
                powerup.update()

                # Check collision with character
                if pygame.sprite.spritecollide(self.character, [powerup], False):
                    if powerup.type == "shield":
                        self.shield_active = True
                        self.shield_timer = 300
                        self.create_particles(powerup.rect.centerx, powerup.rect.centery, BLUE)
                    elif powerup.type == "speed_boost":
                        self.speed_boost_active = True
                        self.speed_boost_timer = 200
                        self.game_speed += 3
                        self.create_particles(powerup.rect.centerx, powerup.rect.centery, YELLOW)
                    elif powerup.type == "coin":
                        self.coins += 1
                        self.create_particles(powerup.rect.centerx, powerup.rect.centery, YELLOW)
                    self.powerups.remove(powerup)

                # Remove off-screen powerups
                if powerup.rect.x < -powerup.width:
                    self.powerups.remove(powerup)

            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if not particle.is_alive():
                    self.particles.remove(particle)

            # Increase difficulty
            if self.score % 5 == 0 and self.score > 0:
                self.difficulty = 1 + (self.score // 5) * 0.3

    def create_particles(self, x, y, color):
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            self.particles.append(Particle(x, y, vel_x, vel_y, color, 30))

    def draw(self):
        screen.fill(WHITE)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.CHARACTER_SELECT:
            self.draw_character_select()
        elif self.state == GameState.BACKGROUND_SELECT:
            self.draw_background_select()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSE:
            self.draw_game()
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        screen.fill(SKY_BLUE)
        title = font_large.render("T-REX RUNNER", True, BROWN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        subtitle = font_medium.render("ADVANCED EDITION", True, RED)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 120))

        # Draw all characters
        char_types = ["trex", "pterodactyl", "raptor", "robot", "robot_female"]
        start_x = SCREEN_WIDTH // 2 - 200
        for i, char_type in enumerate(char_types):
            char = Character(char_type)
            screen.blit(char.image, (start_x + i * 90, 200))

        instructions = font_small.render("Press SPACE to Continue", True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 380))

    def draw_character_select(self):
        screen.fill(SKY_BLUE)
        title = font_large.render("Select Character", True, BROWN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Draw selected character
        selected = Character(self.character_type)
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 80, 150, 160, 140), 3)
        screen.blit(selected.image, (SCREEN_WIDTH // 2 - 25, 160))

        # Character name
        char_names = {"trex": "T-REX", "pterodactyl": "PTERODACTYL", "raptor": "RAPTOR", "robot": "ROBOT", "robot_female": "ROBOT GIRL"}
        name_text = font_medium.render(char_names[self.character_type], True, BROWN)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 310))

        # Abilities based on character
        abilities = {
            "trex": "Standard jumper",
            "pterodactyl": "Can fly higher",
            "raptor": "Double jump + Dash",
            "robot": "Dash ability",
            "robot_female": "Double jump"
        }
        ability_text = font_small.render(abilities[self.character_type], True, BLACK)
        screen.blit(ability_text, (SCREEN_WIDTH // 2 - ability_text.get_width() // 2, 360))

        instructions = font_tiny.render("LEFT/RIGHT Arrow to Select - SPACE to Continue", True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 440))

    def draw_background_select(self):
        screen.fill(SKY_BLUE)
        title = font_large.render("Select Background", True, BROWN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Draw selected background
        bg = Background(self.background_type)
        bg_surface = pygame.Surface((300, 150))
        bg.draw(bg_surface)
        screen.blit(bg_surface, (SCREEN_WIDTH // 2 - 150, 150))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 150, 150, 300, 150), 3)

        # Background name
        name_text = font_medium.render(self.background_type.upper(), True, BROWN)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 330))

        instructions = font_tiny.render("LEFT/RIGHT Arrow to Select - SPACE to Play", True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 440))

    def draw_game(self):
        self.background.draw(screen)

        # Draw ground
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 2)

        # Draw character
        self.character.draw(screen)

        # Draw shield effect
        if self.shield_active:
            pygame.draw.circle(screen, BLUE, (self.character.rect.centerx, self.character.rect.centery), 60, 2)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(screen)

        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

        # Draw UI
        score_text = font_small.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        coins_text = font_small.render(f"Coins: {self.coins}", True, YELLOW)
        screen.blit(coins_text, (20, 60))

        if self.combo > 1:
            combo_text = font_small.render(f"Combo x{self.combo}!", True, RED)
            screen.blit(combo_text, (SCREEN_WIDTH - 250, 20))

        speed_text = font_tiny.render(f"Speed: {self.game_speed:.1f}", True, BLACK)
        screen.blit(speed_text, (20, 100))

        # Shield indicator
        if self.shield_active:
            shield_text = font_tiny.render(f"Shield: {self.shield_timer // 30}s", True, BLUE)
            screen.blit(shield_text, (SCREEN_WIDTH - 250, 60))

        # Speed boost indicator
        if self.speed_boost_active:
            boost_text = font_tiny.render(f"Boost: {self.speed_boost_timer // 30}s", True, YELLOW)
            screen.blit(boost_text, (SCREEN_WIDTH - 250, 100))

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        pause_text = font_large.render("PAUSED", True, YELLOW)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        resume_text = font_small.render("Press P to Resume", True, WHITE)
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2))

        menu_text = font_small.render("Press ESC for Menu", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 50))

        score_text = font_medium.render(f"Score: {self.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))

        coins_text = font_medium.render(f"Coins: {self.coins}", True, YELLOW)
        screen.blit(coins_text, (SCREEN_WIDTH // 2 - coins_text.get_width() // 2, 210))

        high_score_text = font_small.render(f"High Score: {self.high_score}", True, YELLOW)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 270))

        restart_text = font_small.render("Press SPACE to Play Again", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

        menu_text = font_tiny.render("Press ESC for Menu", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 410))


def main():
    game = Game()
    running = True

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
