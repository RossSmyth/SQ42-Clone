import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (150, 20, 20)

#player character class file
class Player(pygame.sprite.Sprite):
        
    def __init__(self, x, y):
            """Constructor function"""
            # Call the parent's constructor
            super().__init__()
    
            # Load the image looking to the right
            self.image_right = pygame.image.load("hornet.png").convert()
            self.image_right.set_colorkey(BLACK)
    
            # Load the image again, flipping it, so it points left
            self.image_left = pygame.transform.flip(pygame.image.load("hornet.png").convert(), True, False)
            self.image_left.set_colorkey(BLACK)
    
            # By default, point right
            self.image = self.image_right
            self.pointing_right = True
            self.rect = self.image.get_rect()
    
            # Make our top-left corner the passed-in location.
            self.rect.x = x
            self.rect.y = y
            
            self.original_x = x
            self.original_y = y
    
            # -- Attributes
            # Set speed vector
            self.change_x = 0
            self.change_y = 0
            
    def changespeed(self, x, y):
            """ Change the speed of the player"""
            self.change_x += x
            self.change_y += y
    
            # Select if we want the left or right image based on the direction
            # we are moving.
            if self.change_x > 0:
                self.image = self.image_right
                self.pointing_right = True
            elif self.change_x < 0:
                self.image = self.image_left
                self.pointing_right = False
    
    def cory(self):
        """super secret function"""
        self.image_right = pygame.image.load("cory_player.jpg").convert()
        self.image_left = pygame.transform.flip(pygame.image.load("cory_player.jpg").convert(), True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        
    def update(self):
            """ Find a new position for the player"""
            self.rect.x += self.change_x
            self.rect.y += self.change_y

class Enemy(pygame.sprite.Sprite):
 
    def __init__(self, difficulty, cory):
        """constructs the enemies"""
        super().__init__()
        
        if cory:
            self.image = pygame.image.load("cory_enemy.jpg").convert()
        else:
            self.image = pygame.image.load("glaive2.png").convert()
 
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        self.image.set_colorkey(BLACK)
 
        self.rect = self.image.get_rect()
        
        self.rect.x = 1280
        self.rect.y = random.randrange(1025)
        
        self.change_x = random.randrange(5, 10) * 1.2 ** difficulty
        
    def update(self):
        """updates the enemy to the next position"""
        self.rect.x -= self.change_x
        
    def reset(self, difficulty):
        """resets the enemy to the initial position"""
        self.rect.x = 1280
        self.rect.y = random.randrange(1025)
        self.change_x = random.randrange(5, 10) * 1.2 ** difficulty
        
    def cory(self):
        """super secret function"""
        self.image = pygame.image.load("cory_enemy.jpg").convert()
        
        
class Background(pygame.sprite.Sprite):
        
    def __init__(self):
        """constructs the background"""
        super().__init__()
       
        self.image = pygame.Surface([2, 2])
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(1279)
        self.rect.y = random.randrange(1022)
        
    def update(self):
        """updates the stars position"""
        self.rect.x -= random.randrange(14, 20)
        
    def reset(self):
        """puts stars at the end"""
        self.rect.x = 1280

class Laser(pygame.sprite.Sprite):
        
    def __init__(self, player_x, pointing_right, x, y, cory):
        """constructs the bullet sprites"""
        
        super().__init__()
        
        if cory:
            self.image = pygame.image.load("cory_laser.jpg").convert()
        else:
            self.image = pygame.Surface([15, 5])
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y + 33
        
        if pointing_right:
            self.change_x = player_x + 10
            self.rect.x += 50
        else:
            self.change_x = player_x - 10
            
    def cory(self):
        self.image = pygame.image.load("cory_laser.jpg").convert()
        
    def update(self):
        """should move the lasers"""
            
        self.rect.x += self.change_x
    
        
        