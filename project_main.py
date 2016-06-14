"""
Use sprites to collect blocks.
 
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Explanation video: http://youtu.be/4W2AqUetBi4
"""
import time
import pygame
import random
from player import *


 
# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)


# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 1280
screen_height = 1024
screen = pygame.display.set_mode([screen_width, screen_height], pygame.FULLSCREEN)

difficulty = 0
cory = False

cory_theme = pygame.mixer.Sound('cory.wav')

# All blocks and the player block as well.
enemy_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
background_sprites_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()

#defines the player
player = Player(100, 100)
all_sprites_list.add(player)

#creates the enemies
for enemy in range(10):
    e = Enemy(difficulty, cory)
    enemy_sprites_list.add(e)
    all_sprites_list.add(e)

#creates the background stars
for star in range (100):
    star = Background()
    background_sprites_list.add(star)
    

 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

font = pygame.font.SysFont('Calibri', 25, True, False) #sets font
score = 0 #the starting score is 0

lives = 5

space_down = False #spac eisn't pressed

frame = 0 #frame counter is set to 0

laser_sound = pygame.mixer.Sound("laser_sound.wav") #sound of laser
explosion_sound = pygame.mixer.Sound("explosion.wav") #sound of enemy exploding
scream_sound = pygame.mixer.Sound("scream.wav") #player dying

 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True #so you can quit the game
            elif event.key == pygame.K_UP: #you can move up
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN: #you can move down
                player.changespeed(0, 3)
            elif event.key == pygame.K_LEFT: #you can move left
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT: #you can move right
                player.changespeed(3, 0)
            elif event.key == pygame.K_SPACE: #you can shoot
                laser = Laser(player.change_x, player.pointing_right, player.rect.x, player.rect.y, cory) #makes the laser
                
                all_sprites_list.add(laser)
                laser_list.add(laser)
                
                space_down = True #space is down
                frame = 0 #resets frame counter to 0
            elif event.key == pygame.K_RETURN and lives <= 0:
                lives = 5
                score = 0
                difficulty = 0
            elif event.key == pygame.K_c:
                cory = True
                cory_theme.play()
                for sprite in all_sprites_list:
                    sprite.cory()
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)
            elif event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_SPACE:
                space_down = False
 
    # Clear the screen
    screen.fill(BLACK) #background is black
    
    if lives > 0:
        
        if space_down and frame % 10 == 0: #every 20 frames when space is down it will make a new laser
            laser = Laser(player.change_x, player.pointing_right, player.rect.x, player.rect.y, cory) #makes the laser
                    
            all_sprites_list.add(laser)
            laser_list.add(laser)
            laser_sound.play()
        
        #checks if enemy is past the screen edge
        for enemy in enemy_sprites_list:
            if enemy.rect.x < -75:
                enemy.reset(difficulty)
            
        #checks if the background star
        for star in background_sprites_list:
            if star.rect.x < -2:
                star.reset()
        
        #checks if the player is hitting an enemy
        for enemy in enemy_sprites_list:
            enemy_hit_list = pygame.sprite.spritecollide(player, enemy_sprites_list, True)
            
            if len(enemy_hit_list) >= 1: #resets the player if they are hit
                scream_sound.play()
                lives -= 1
                player.rect.x = player.original_x
                player.rect.y = player.original_y
        
        #makes the laser hit stuff
        for laser in laser_list:
            if laser.rect.x > 1295 or laser.rect.y < -15:
                all_sprites_list.remove(laser)
                laser_list.remove(laser)
                
            enemy_laser_hit_list = pygame.sprite.spritecollide(laser, enemy_sprites_list, True) #enemies hit by laser
    
            for hit_enemy in enemy_laser_hit_list:
                laser_list.remove(laser)
                all_sprites_list.remove(laser)
                explosion_sound.play()
                score += 1
                if score % 10 == 0:
                    difficulty += 1
                    for enemy in enemy_sprites_list:
                        enemy.change_x *= 1.2
        
        #generates the enemies once they are destroyed by laser
        if len(enemy_sprites_list) < 10:
            e = Enemy(difficulty, cory)
            enemy_sprites_list.add(e)
            all_sprites_list.add(e)
            
        
    
        # Draw all the spites
        all_sprites_list.update()
        all_sprites_list.draw(screen)
        
        #draws the background sprites
        background_sprites_list.update()
        background_sprites_list.draw(screen)
        
        #draws the score
        score_window = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_window, [10, 10])
        
        #draws the lives
        lives_window = font.render("Lives: " + str(lives), True, WHITE)
        screen.blit(lives_window, [150, 10])
    else:
        dead = font.render("You died! Press enter to continue", True, WHITE)
        screen.blit(dead, [500, 500])
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    frame += 1
 
    # Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()