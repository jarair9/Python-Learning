import pygame
pygame.init()

class Blocks:
    def __init__(self):
        self.W = 70
        self.H = 30
        self.gap = 2
        self.rows = 7
        self.cols = 8
        self.blocks = []

        for r in range(self.rows):
            for c in range(self.cols):
                block_rect = pygame.Rect(
                    r * (self.W + self.gap),
                    c * (self.H + self.gap),
                    self.W,
                    self.H
                )
                self.blocks.append(block_rect)

    def update(self):
        for rects in self.blocks:
            pygame.draw.rect(screen, "red", rects)


class BallANDPADDLE:
    def __init__(self):
        self.ball_radius = 10
        self.w = 90
        self.h = 20
        self.peddle_rect = pygame.Rect(300, 470, self.w, self.h)
        self.ball_rect = pygame.Rect(300, 300, self.ball_radius * 2, self.ball_radius * 2)
        self.velocity_x = 3   # ✅ give starting sideways speed
        self.velocity_y = -5  # ✅ negative means going UP at start

    def ball(self, blocks):
        self.gravity = 0.2

        self.ball_rect.y += self.velocity_y
        self.ball_rect.x += self.velocity_x

        # ✅ gravity only on Y, not X!
        self.velocity_y += self.gravity

        # ✅ safe block removal - collect first, remove after
        blocks_to_remove = []
        for rect in blocks:
            if self.ball_rect.colliderect(rect):
                blocks_to_remove.append(rect)
                self.velocity_y *= -1  # bounce off block

        for rect in blocks_to_remove:
            blocks.remove(rect)

        pygame.draw.circle(screen, "white", self.ball_rect.center, self.ball_radius)

    def peddle(self):
        pygame.draw.rect(screen, "blue", self.peddle_rect)


screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

running = True
b = Blocks()
m = BallANDPADDLE()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    # Paddle collision
    if m.ball_rect.colliderect(m.peddle_rect):
        m.velocity_y *= -1
        m.ball_rect.bottom = m.peddle_rect.top  # ✅ push ball above paddle

    # Top wall
    if m.ball_rect.top <= 0:
        m.velocity_y *= -1
        m.ball_rect.top = 0

    # Left wall
    if m.ball_rect.left <= 0:
        m.velocity_x *= -1
        m.ball_rect.left = 0

    # Right wall
    if m.ball_rect.right >= 500:
        m.velocity_x *= -1
        m.ball_rect.right = 500

    # Game over
    if m.ball_rect.bottom > 500:
        running = False
        pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        m.peddle_rect.x -= 10
    if keys[pygame.K_RIGHT]:
        m.peddle_rect.x += 10

    if m.peddle_rect.left < 0:
        m.peddle_rect.left = 0
    if m.peddle_rect.right > 500:
        m.peddle_rect.right = 500

    screen.fill("Black")
    b.update()
    m.ball(b.blocks)  # ✅ passing blocks as argument instead of using global b
    m.peddle()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()