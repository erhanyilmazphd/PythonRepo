import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("T-Rex Runner Game")

# Font
font_large = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 40)
font_tiny = pygame.font.Font(None, 30)


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


class TRex(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.draw_trex()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 80
        self.vel_y = 0
        self.is_jumping = False
        self.jump_power = 15

    def draw_trex(self):
        self.image.fill(WHITE)
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

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -self.jump_power

    def update(self):
        # Apply gravity
        self.vel_y += 0.6
        self.rect.y += self.vel_y

        # Ground collision
        if self.rect.y >= SCREEN_HEIGHT - 80:
            self.rect.y = SCREEN_HEIGHT - 80
            self.is_jumping = False
            self.vel_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()
        self.type = obstacle_type  # "cactus" or "pterodactyl"
        self.width = 30
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)

        if obstacle_type == "cactus":
            self.draw_cactus()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 85
        else:  # pterodactyl
            self.draw_pterodactyl()
            self.rect = self.image.get_rect()
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - 150
            self.flap_counter = 0

        self.vel_x = -8

    def draw_cactus(self):
        # Draw cactus shape
        pygame.draw.rect(self.image, GREEN, (12, 10, 6, 30))
        pygame.draw.rect(self.image, GREEN, (5, 20, 6, 15))
        pygame.draw.rect(self.image, GREEN, (22, 20, 6, 15))
        # Spikes
        pygame.draw.polygon(self.image, GREEN, [(12, 10), (9, 5), (15, 8)])
        pygame.draw.polygon(self.image, GREEN, [(12, 40), (9, 45), (15, 42)])

    def draw_pterodactyl(self):
        # Draw pterodactyl shape
        pygame.draw.circle(self.image, GREEN, (15, 15), 6)  # Head
        pygame.draw.polygon(self.image, GREEN, [(10, 15), (5, 10), (5, 20)])  # Beak
        pygame.draw.polygon(self.image, GREEN, [(21, 15), (28, 10), (28, 20)])  # Wing
        pygame.draw.circle(self.image, BLACK, (16, 13), 2)  # Eye

    def update(self):
        self.rect.x += self.vel_x
        
        # Pterodactyl flapping animation
        if self.type == "pterodactyl":
            self.flap_counter += 1
            if self.flap_counter > 10:
                self.rect.y += random.choice([-2, 2])
                self.flap_counter = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.trex = TRex()
        self.obstacles = []
        self.score = 0
        self.game_speed = 8
        self.spawn_timer = 0
        self.spawn_rate = 80
        self.high_score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.trex.jump()
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        return True

    def start_game(self):
        self.state = GameState.PLAYING
        self.trex = TRex()
        self.obstacles = []
        self.score = 0
        self.game_speed = 8
        self.spawn_rate = 80
        self.spawn_timer = 0

    def update(self):
        if self.state == GameState.PLAYING:
            self.trex.update()

            # Spawn obstacles
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_rate:
                obstacle_type = random.choice(["cactus", "pterodactyl"])
                new_obstacle = Obstacle(obstacle_type)
                new_obstacle.vel_x = -self.game_speed
                self.obstacles.append(new_obstacle)
                self.spawn_timer = 0

            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()

                # Check collision
                if pygame.sprite.spritecollide(self.trex, [obstacle], False):
                    self.state = GameState.GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score

                # Remove off-screen obstacles and increase score
                if obstacle.rect.x < -obstacle.width:
                    self.obstacles.remove(obstacle)
                    self.score += 1

            # Increase difficulty
            if self.score % 5 == 0 and self.score > 0:
                self.game_speed = 8 + (self.score // 5) * 0.5

    def draw(self):
        screen.fill(WHITE)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        title = font_large.render("T-REX RUNNER", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Draw a large T-Rex
        trex_surface = pygame.Surface((100, 120))
        trex_surface.fill(WHITE)
        pygame.draw.rect(trex_surface, BROWN, (25, 40, 50, 50))
        pygame.draw.circle(trex_surface, BROWN, (60, 30), 15)
        pygame.draw.circle(trex_surface, BLACK, (65, 25), 4)
        pygame.draw.polygon(trex_surface, BROWN, [(20, 50), (10, 40), (15, 60)])
        pygame.draw.rect(trex_surface, BROWN, (30, 90, 6, 20))
        pygame.draw.rect(trex_surface, BROWN, (50, 90, 6, 20))
        screen.blit(trex_surface, (SCREEN_WIDTH // 2 - 50, 120))

        instructions = font_small.render("Press SPACE to Start", True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 300))

    def draw_game(self):
        # Draw ground
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, SCREEN_HEIGHT - 20), 2)

        # Draw clouds
        pygame.draw.circle(screen, (200, 200, 200), (100, 50), 20)
        pygame.draw.circle(screen, (200, 200, 200), (130, 55), 25)
        pygame.draw.circle(screen, (200, 200, 200), (600, 60), 22)
        pygame.draw.circle(screen, (200, 200, 200), (630, 50), 20)

        # Draw T-Rex
        self.trex.draw(screen)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(screen)

        # Draw score
        score_text = font_small.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        speed_text = font_tiny.render(f"Speed: {self.game_speed:.1f}", True, BLACK)
        screen.blit(speed_text, (20, 60))

    def draw_game_over(self):
        self.draw_game()

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 80))

        score_text = font_small.render(f"Score: {self.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 160))

        high_score_text = font_small.render(f"High Score: {self.high_score}", True, YELLOW)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 210))

        restart_text = font_tiny.render("Press SPACE to Restart or ESC for Menu", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))


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
