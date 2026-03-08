import pygame
import random
import sys
# self.ball.bottom == self.paddle.top:
# The gravity formula is: velocity += gravity and position += velocity
pygame.init()
# shoot_sound = pygame.mixer.Sound("PYGAME/graphics/breaked.wav")
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
        self.peddle_rect = pygame.Rect(300,470,self.w,self.h) 
        self.ball_rect = pygame.Rect(300, 300, self.ball_radius*2, self.ball_radius*2)
        self.velocity_x = 0  
        self.velocity_y  = 0     
        

    def ball(self):
        # constant Value
        self.gravity = 0.5                
       
        self.ball_rect.y += self.velocity_y  # velocity Y for rising and falling
        self.ball_rect.x += self.velocity_x - 1 # velocity x for forward and backward

        # Semulation for Gravity 
        self.velocity_y += self.gravity
        self.velocity_x += self.gravity

        for rect in b.blocks:
            if m.ball_rect.colliderect(rect):
                # shoot_sound.play()
                b.blocks.remove(rect)
        pygame.draw.circle(screen, "white", self.ball_rect.center, self.ball_radius)

    def peddle(self):
        pygame.draw.rect(screen,"blue",self.peddle_rect)

 
        
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

running = True
b = Blocks()
m = BallANDPADDLE()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    

    if m.ball_rect.colliderect(m.peddle_rect):
        m.velocity_y = m.velocity_y * - 1
        m.ball_rect.y += m.velocity_y  

    if m.ball_rect.top >=  500:
        m.velocity_x = m.velocity_x - 0.5
        m.velocity_y = m.velocity_y * - 1
        m.ball_rect.y += m.velocity_y 




        
        


     
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
    m.ball()
    m.peddle()
   
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

