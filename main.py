import pygame
import random
import math

# start game
pygame.init()

# screen def
screen = pygame.display.set_mode((800,600)) # 800 is width and 600 is height

#background
background = pygame.image.load('pygame/images/background.jpg') 

# title and icon
pygame.display.set_caption("SPACE INVADERS")

programIcon = pygame.image.load('pygame/images/alien.png')
pygame.display.set_icon(programIcon)

# player
playerImage = pygame.image.load('pygame/images/space-invaders.png')
playerX = 370  # distance from left
playerY = 480  # distance from top
playerX_change = 0
playerY_change = 0

# Enemy
enemyImage =[]
enemyX = []
enemyY = []
enemyX_change = [] 
enemyY_change = []
num_of_enemies = 6
# Create multiple enemies
for i in range (num_of_enemies):
    enemyImage.append( pygame.image.load('pygame/images/moon.png') )
    enemyX.append( random.randint (0, 735) )
    enemyY.append( random.randint (50, 150) )
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletImage = pygame.image.load('pygame/images/bullet.png')
bulletX = 0
bulletY = 480  
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready" # Ready - Can't see bullet on screen

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) # 'free...' is the name of font, 32 is size

textX = 10
textY = 10

# Functions 
def player(x, y):
    # blit is to draw the image 
    screen.blit(playerImage, (x, y))

def enemy(x, y, i):
    # blit is to draw the image 
    screen.blit(enemyImage[i], (x, y))  

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def isColliding(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else :
        return False  

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
      

# game loop
running = True 
while running:

    screen.fill((0, 0, 0))
    
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        #check if key == left or right
        if event.type == pygame.KEYDOWN :        
            if event.key == pygame.K_LEFT:
                playerX_change = -5  # To move left, negative 
            if event.key == pygame.K_RIGHT:
                playerX_change = 5   # To move right, positive
            if event.key == pygame.K_SPACE:
                # To avoid bullet changing direction while moving
                if bullet_state == "ready" :
                    # Assign value to avoid bullet following
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)       

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0     # To stop value == 0       
     
    playerX += playerX_change

    #creating boundries for spaceship
    if playerX <= 0 :
        playerX = 0 
    elif playerX >= 750:
        playerX = 750    

    # Enemy movement
    for  i in range (num_of_enemies) :

        # Game over 
        if enemyY[i] > 430 :
            for j in range (num_of_enemies) :
                enemyY[j] = 2000
            game_over_text()
            break;    

        enemyX[i] += enemyX_change[i]
        # Def enemy movement with y - axis
        if enemyX[i] <= 0 :
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        #collision
        collision = isColliding(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint (0, 735)  
            enemyY[i] = random.randint (50, 150) 
        enemy(enemyX[i], enemyY[i], i) 
     
    # Bullet movement    
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY) 
        bulletY -= bulletY_change

    player(playerX, playerY) # player needs to be after screen fill as player comes on top of screen
    show_score(textX, textY)
    pygame.display.update()        