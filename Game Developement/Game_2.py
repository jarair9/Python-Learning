import pygame
import sys


pygame.init()
width = 700
height = 400

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping Pong")
font = pygame.font.Font("Game Developement/assets/Digitag.ttf",50)
clock = pygame.time.Clock()

right_panel = pygame.Rect(width-20,height // 2,20,100)
left_panel = pygame.Rect(width - width,height // 2,20,100)
ball = pygame.Rect(300, 300, 10 * 2, 10 * 2)


velocity_x = 5
velocity_y = 5

def restart_screen():
    screen.fill("black")
    restart_instruc = font.render("Press Any Key To Restart",False,"white")
    screen.blit(restart_instruc,(100,100))



is_running = True
while is_running:
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
    ball.x += velocity_x
    ball.y += velocity_y

    



    # Ball Bottom Floor
    if ball.bottom > height:
        velocity_y *= -1
        ball.bottom = height

    if ball.top < 0:
        velocity_y *= -1
        ball.top = 0

    if ball.colliderect(right_panel):
        velocity_x *= -1
        ball.right = right_panel.left

    if ball.colliderect(left_panel):
        velocity_x *= -1
        ball.left = left_panel.right

    if ball.right > width:
        restart_screen()
        

    if ball.left < 0:
        restart_screen()


    
    pygame.draw.rect(screen, "red", right_panel)
    pygame.draw.rect(screen, "red", left_panel)
    pygame.draw.circle(screen, "cyan", ball.center, 10)
    


    pygame.display.update()
    clock.tick(60)