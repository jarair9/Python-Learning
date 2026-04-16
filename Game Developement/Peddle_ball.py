import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

class Blocks:
    def __init__(self):
        self.W = 55  # Adjusted width to fit the screen better
        self.H = 20
        self.gap = 5
        self.rows = 5
        self.cols = 8
        self.blocks = []
        self.reset()

    def reset(self):
        self.blocks = []
        for r in range(self.rows):
            for c in range(self.cols):
                # Swapped r and c logic to align correctly
                block_rect = pygame.Rect(
                    c * (self.W + self.gap) + 10, 
                    r * (self.H + self.gap) + 50,
                    self.W,
                    self.H
                )
                self.blocks.append(block_rect)

    def draw(self, surface):
        for rect in self.blocks:
            pygame.draw.rect(surface, "red", rect)

class BallANDPADDLE:
    def __init__(self):
        self.ball_radius = 10
        self.w = 100
        self.h = 15
        self.reset()

    def reset(self):
        self.paddle_rect = pygame.Rect(SCREEN_WIDTH//2 - self.w//2, 470, self.w, self.h)
        self.ball_rect = pygame.Rect(SCREEN_WIDTH//2, 300, self.ball_radius * 2, self.ball_radius * 2)
        self.velocity_x = 4
        self.velocity_y = -4

    def update_ball(self, blocks):
        self.ball_rect.x += self.velocity_x
        self.ball_rect.y += self.velocity_y

        # Block Collision
        for rect in blocks[:]: # Iterate over a copy to safely remove
            if self.ball_rect.colliderect(rect):
                self.velocity_y *= -1
                blocks.remove(rect)
                break # Collision with one block per frame prevents "phasing"

    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.ball_rect.center, self.ball_radius)
        pygame.draw.rect(surface, "blue", self.paddle_rect)

def show_restart_screen():
    screen.fill((33, 33, 33))
    text = font.render("GAME OVER", True, "white")
    subtext = font.render("Press R to Restart or Q to Quit", True, "gray")
    screen.blit(text, (SCREEN_WIDTH // 2 - 80, 200))
    screen.blit(subtext, (SCREEN_WIDTH // 2 - 180, 250))
    pygame.display.flip()

# Game Objects
b = Blocks()
m = BallANDPADDLE()
game_active = True

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    b.reset()
                    m.reset()
                    game_active = True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    if game_active:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and m.paddle_rect.left > 0:
            m.paddle_rect.x -= 7
        if keys[pygame.K_RIGHT] and m.paddle_rect.right < SCREEN_WIDTH:
            m.paddle_rect.x += 7

        # Ball Logic
        m.update_ball(b.blocks)

        # Wall Collisions
        if m.ball_rect.left <= 0 or m.ball_rect.right >= SCREEN_WIDTH:
            m.velocity_x *= -1
        if m.ball_rect.top <= 0:
            m.velocity_y *= -1

        # Paddle Collision
        if m.ball_rect.colliderect(m.paddle_rect):
            if m.velocity_y > 0: # Only bounce if falling down
                m.velocity_y *= -1
                m.ball_rect.bottom = m.paddle_rect.top

        # Floor (Lose condition)
        if m.ball_rect.bottom > SCREEN_HEIGHT:
            game_active = False

        # Rendering
        screen.fill("black")
        b.draw(screen)
        m.draw(screen)
        pygame.display.flip()
    else:
        show_restart_screen()

    clock.tick(FPS)