import pygame
import sys
import random
pygame.init()

class Fruits:
    def __init__(self):  
        self.x = 20
        self.rects = []

    def Update(self):
        blocks = pygame.Rect(
            random.randint(1,400),
            random.randint(1,400),
            self.x,
            self.x
        )
        self.rects.append(blocks)
    
    def draw(self):
        for rect in self.rects:
            pygame.draw.rect(screen, "red", rect)


    def randomixe(self):
        pass



class Snack:
    def __init__(self):
        pass






W = 500
H = 500

pygame.display.set_caption("Snack game")
screen = pygame.display.set_mode((W,H))
font = pygame.font.Font(None, 32)

clock = pygame.time.Clock()

f = Fruits()
f.Update()
active = True
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    screen.fill((33,33,33))
  
    f.draw()
    clock.tick(60)
    pygame.display.update()
pygame.quit()