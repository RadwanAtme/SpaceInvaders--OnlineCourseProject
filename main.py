import pygame
import random
import math
from pygame import mixer

width = 800
height = 600
# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((width, height))

# Title and Icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Player
playerImg = pygame.image.load('player.png')
playerX = width / 2 - 20
playerX_change = 0
playerY = height * 3 / 4

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - you can't see the bullet on the sreen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('font.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('font.ttf', 64)


def show_score(x, y):
    score = font.render("Score " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collided(enemyX, enemyY, bulletX, bulletY):
    distanceX = math.pow(enemyX - bulletX, 2)
    distanceY = math.pow(enemyY - bulletY, 2)
    distance = math.sqrt(distanceX + distanceY)
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # RGB - Red, Green, Blue (0,255)
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # Checking for boundaries of spaceship so it dosen't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collided(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('Explosion.wav')
            explosion_Sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= -50:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
