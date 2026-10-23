import math
import pygame
import random

SCREEN_WIDTH=800
SCREEN_HEIGHT=500
PLAYER_START_X=370
PLAYER_START_Y=380
ENEMY_START_Y_MIN=50
ENEMY_START_Y_MAX=150
ENEMY_SPEED_X=4
ENEMY_SPEED_Y=40
BULLET_SPEED_Y=10
COLLISION_DISTANCE=27

pygame.init()
clock=pygame.time.Clock()

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background=pygame.image.load("bg.jpg")
background=pygame.transform.scale(background,((SCREEN_WIDTH,SCREEN_HEIGHT)))

pygame.display.set_caption("Space Invader")
pygame.display.set_icon(pygame.image.load("ufo.png"))

playerimg=pygame.image.load("ship.png")
playerimg=pygame.transform.scale(playerimg,(64,64))
playerX=PLAYER_START_X
playerY=PLAYER_START_Y
playerX_change=0

num_of_enemies=6
enemyImg,enemy_x,enemy_Y,enemyX_change,enemyY_change=[],[],[],[],[]
ENEMY_SIZE=50


for i in range(num_of_enemies):
    enemyImg.append(pygame.transform.scale(pygame.image.load("enemy.png"),(ENEMY_SIZE,ENEMY_SIZE)))
    enemy_x.append(random.randint(0,SCREEN_WIDTH,ENEMY_SIZE))
    enemy_Y.append(random.randint(ENEMY_START_Y_MIN,ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)

bulletImg=pygame.image.load("bullet.png")
bulletImg=pygame.transform.scale(bulletImg,(16,32))
bulletX=0
bulletY=PLAYER_START_Y
bullet_state="ready"

score=0
font=pygame.font.Font("freesansbold.ttf",32)
game_over=pygame.font.Font("freesansbold.ttf",64)

running=True
while running:
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False

        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            elif event.key==pygame.K_RIGHT:
                playerX_change=5
            elif event.key==pygame.K_SPACE and bullet_state=="ready":
                bulletX=playerX
                bullet_state="fire"

        elif event.type == pygame.KEYUP:
            playerX_change=0

    playerX += playerX_change
    playerX=max(0,min(playerX,SCREEN_WIDTH - 64))

    if bullet_state == "fire":
        screen.blit(bulletImg,(bulletX + 16,bulletY + 10))
        bulletY-=BULLET_SPEED_Y

    if bulletY <= 0:
        bulletY=PLAYER_START_Y
        bullet_state="ready"

    for i in range(num_of_enemies):
        enemy_x[i] += enemyX_change[i]

        if enemy_x[i] <= 0 or enemy_x[i] >= SCREEN_WIDTH - ENEMY_SIZE:
            enemyX_change[i]*= -1
            enemy_Y[i]+= ENEMY_SPEED_Y

        if math.hypot(enemy_x[i]-bulletX,enemy_Y-bulletY)< COLLISION_DISTANCE:
            score+= 1
            playerY=PLAYER_START_Y
            bullet_state="ready"
            enemy_x[i]=random.randint(0,SCREEN_WIDTH - ENEMY_SIZE)
            enemy_Y[i]=random.randint(ENEMY_START_Y_MIN,ENEMY_START_Y_MAX)

        if enemy_Y[i] > 340:
            screen.blit(game_over.render("GAME OVER",True,(255,255,255)),(180,220))
            running=False

        screen.blit(enemyImg[i],(enemy_x[i],enemy_Y[i]))

    screen.blit(playerimg,(playerX,playerY))
    screen.blit(font.render(f"Score:{score}",True,(255,255,255)),(10,10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()