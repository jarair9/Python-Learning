import pygame
from random import randint
import sys

pygame.init()
# shoot_sound = pygame.mixer.Sound("PYGAME/graphics/hit.wav")

class Enemy:
    def __init__(self):
        
        self.enemies = []
        self.counts = 0

    def spawn(self):
        self.x = randint(0,800 - enemy.get_width())
        self.y = 0
        enemy_rect = enemy.get_rect(topleft = (self.x,self.y))
        self.enemies.append(enemy_rect)

    def update(self):
        for enemy in self.enemies:
            enemy.y += 2
        self.enemies = [x for x in self.enemies if x.top < 600]

    def draw(self):
        for rect in self.enemies:
            screen.blit(enemy,rect)


    def collison(self):
        for bullets in bullets:
            for enemy in self.enemies:
                if bullet.colliderect(enemy):
                    # shoot_sound.play()
                    self.count += 1
                    self.enemies.remove(enemy)


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()


player = pygame.image.load("Game Developement/assets/player.png").convert_alpha()
player_rect = player.get_rect(midbottom=(400, 550))
enemy = pygame.image.load("Game Developement/assets/enemy.png").convert_alpha()


# Bullet system
bullets = []
bullet_speed = 7
player_speed = 5

last_spawn_time = 0
spawn_delay = 500   # 1000 ms = 1 second

A = Enemy()



def collison():
    for bullet in bullets:
        for enemy in A.enemies:
            if bullet.colliderect(enemy):
                # shoot_sound.play()
                A.enemies.remove(enemy)
                
def gameover():
    font = pygame.font.Font("Game Developement\assets\Digitag.ttf",50)
    text_score = font.render(f"Score : {A.counts}",True,"red")
    key_text = font.render(f"Press Enter to Start Again",True,50)
    screen.blit(key_text,(600,125))
    screen.blit(text_score,(700,90))
    
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player_rect.centerx - 2,
                    player_rect.top,
                    4,
                    12
                )
                bullets.append(bullet)

            if event.key == pygame.K_SPACE:
                pass


    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time > spawn_delay:
        A.spawn()
        last_spawn_time = current_time


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > 800:
        player_rect.right = 800

    
    for bullet in bullets:
        bullet.y -= bullet_speed

    bullets = [bullet for bullet in bullets if bullet.bottom > 0]

    screen.fill("black")
    screen.blit(player, player_rect)
    
    for bullet in bullets:
        pygame.draw.rect(screen, "red", bullet)

    A.update()
    A.draw()
    collison()

    for enemys in A.enemies:    
        if player_rect.colliderect(enemys):
            # gameover()
            pygame.quit()
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()