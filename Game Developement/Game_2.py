import pygame
import sys


pygame.init()
width = 700
height = 400

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

right_panel = pygame.Rect(width-20,height // 2,20,100)
left_panel = pygame.Rect(width - width,height // 2,20,100)
ball = pygame.Rect(300, 300, 10 * 2, 10 * 2)

gravity = 0.5
velocity = 0
velocity_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    key = pygame.key.get_pressed()

    if key[pygame.K_w]:
        left_panel.y -= 10
    if key[pygame.K_s]:
        left_panel.y += 10
    if key[pygame.K_UP]:
        right_panel.y -= 10
    if key[pygame.K_DOWN]:
        right_panel.y += 10
    

    # Creating FLoor
    if left_panel.bottom > height:
        left_panel.bottom = height
    if left_panel.top < 0:
        left_panel.top = 0
    
    if right_panel.bottom > height:
        right_panel.bottom = height
    if right_panel.top < 0:
        right_panel.top = 0
    
    # Applying Gravity
    ball.x += velocity 
    ball.y += velocity_y

    velocity_y += gravity
    velocity += gravity

    # Ball Bottom Floor
    if ball.bottom > height:
        velocity_y *= -1
        ball.bottom = height

    if ball.top > height :
        velocity_y *= -1
        ball.bottom = height

    if ball.colliderect(right_panel):
        velocity *= -1
        ball.right = right_panel.left



    




    pygame.draw.rect(screen, "red", right_panel)
    pygame.draw.rect(screen, "red", left_panel)
    pygame.draw.circle(screen, "cyan", ball.center, 10)
    


    pygame.display.update()
    clock.tick(60)