import pygame, sys, os, math
from pygame.locals import *

pygame.init()

# Set the clock parameters
clock = pygame.time.Clock()
Frames_Per_Second = 30
gametime = 0

#Set the screen parameters
width = 1000
height = 550
screen = pygame.display.set_mode((width,height))
#blueColor = pygame.Color(0,0,255)
#fontObj = pygame.font.Font('freesansbold.ttf',32)


# Load background image, initialize background and caption
sky = pygame.image.load("clouds1.jpg").convert()
screen.blit(sky,(0,0))
screen.convert_alpha()
pygame.display.set_caption("Bullet Hell using PyGame")
    


#Class to represent the player's ship
class Ship(pygame.sprite.Sprite):
    #Define initial velocity
    vel = [0,0]
    
    #Methods for the player's ship
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        #Set image and rect for the player's ship
        self.image = pygame.image.load("Spaceship2.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        
    def change_vel(self,x,y):
        self.vel[0] += x
        self.vel[1] += y
		
	def shoot(self):
		return None
        
    def update(self):
        global width, height
        new_x = self.rect.x + self.vel[0]
        new_y = self.rect.y + self.vel[1]
        if (new_x > 0) and (new_x < width-self.rect.width):
            self.rect.x = new_x
        if (new_y > 0) and (new_y < height-self.rect.height):
            self.rect.y = new_y

#Class for enemy ships
class Enemy(pygame.sprite.Sprite):
    age = 0
    def __init__(self,pos, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.vel = vel
        
    def update(self):
        global width, height
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        if self.rect.y >= height:
            dead_sprite_group.add(self)
        if self.age%30 == 0:
            self.shoot()
        self.age += 1
        
    #method to define a vector so that the enemy can shoot in the direction of the player    
    def vector_to_ship(self,player):
        vector = [0,0]
        vector[0] = player.rect.centerx - self.rect.centerx
        vector[1] = player.rect.centery - self.rect.centery
        c = math.sqrt((vector[0])**2 + (vector[1])**2)
        vector[0] = vector[0]/c
        vector[1] = vector[1]/c        
        return vector
    
    def shoot(self):
        missile_start = [self.rect.topleft[0],self.rect.centery]
        missile_group.add(EnemyMissile(missile_start,10,self.vector_to_ship(player_ship)))

class EnemyMissile(pygame.sprite.Sprite):
    age = 0
    def __init__(self,pos,vel,vel_vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_missile.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.vel = [vel*i for i in vel_vector]
        
    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        if self.age > 100:
            dead_sprite_group.add(self)
        self.age += 1
        
        
def enemy_spawner(interval):
    global gametime
    if gametime % (interval*30) == 0:
        enemy_sprite_group.add(Enemy([800,0],[0,4]))

#Initialize the player's ship
player_ship = Ship(200,225)
player_sprite_group = pygame.sprite.Group((player_ship))

#Initialize a group of enemy sprites and a group of dead sprites
#Every update, the list of dead sprites will be removed from the list of enemy sprites
enemy_sprite_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
dead_sprite_group = pygame.sprite.Group()
    
while True:
# Main while loop
    
    for event in pygame.event.get():
    #Do all event processing here
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Need to update the key handlers to make movement more smooth
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_ship.change_vel(-4,0)
            if event.key == pygame.K_RIGHT:
                player_ship.change_vel(4,0)
            if event.key == pygame.K_UP:
                player_ship.change_vel(0,-4)
            if event.key == pygame.K_DOWN:
                player_ship.change_vel(0,4)
			if event.key == pygame.K_SPACE:
				player_ship.shoot()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_ship.change_vel(4,0)
            if event.key == pygame.K_RIGHT:
                player_ship.change_vel(-4,0)
            if event.key == pygame.K_UP:
                player_ship.change_vel(0,4)
            if event.key == pygame.K_DOWN:
                player_ship.change_vel(0,-4)

    #Spawn a new enemy at some set time interval in seconds
    gametime +=1
    enemy_spawner(1)
    #Remove dead enemies from the enemy sprite group, then empty the dead sprite group
    enemy_sprite_group.remove(dead_sprite_group.sprites())
    missile_group.remove(dead_sprite_group.sprites())
    dead_sprite_group.empty()
    
    #Update sprites and game time
    player_ship.update()
    enemy_sprite_group.update()
    missile_group.update()

    
    #Handle all drawing here
    player_sprite_group.clear(screen,sky)
    player_sprite_group.draw(screen)
    enemy_sprite_group.clear(screen,sky)
    enemy_sprite_group.draw(screen)
    missile_group.clear(screen,sky)
    missile_group.draw(screen)
    pygame.display.flip()
    
    #Limit to the amount of frames per second specified
    clock.tick(Frames_Per_Second)

