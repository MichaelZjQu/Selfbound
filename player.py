import pygame
from projectile import Projectile
from pygame.locals import *
from resources import *
import math


class Player:
    x = 300
    y = 300

    PLAYER_SPEED = 5


    def __init__(self, imgs, name, width = PLAYER_WIDTH, length = PLAYER_HEIGHT):
        #init frames
        self.frames = []
        for i in range(imgs):
            temp = pygame.Surface((width, length), pygame.SRCALPHA, 32)
            temp.convert_alpha()
            temp.set_colorkey((255,255,255))
            frame = pygame.image.load("imgs/" + name + "/"+str(i) + '.png')
            temp.blit(frame, (0,0))
            self.frames.append(temp)

        self.downFrames = self.frames[0:4]
        self.upFrames = self.frames[4:8]
        self.leftFrames = self.frames[8:12]
        self.rightFrames = self.frames[12:16]
        
        self.rect = pygame.Rect(self.x, self.y, width, length)

        self.flame = False
        self.leach = False
        self.vampire = False

        #HP0, DMG1, ARMOR2, SPEED3, ATK4 
        self.maxstats = [100, 100, 100, 5, 400]
        self.stats = [100, 100, 100, 5, 500]
        self.abilities = []

        self.frame = 0
        self.moving = True  
        self.lastmove = 0
        self.lastshot = 0

        self.lasthit = 0

    def collide(self, controls, tilemap):
        speed = self.stats[3]
        nextx = self.x + speed*controls[3] - speed*controls[1]
        nexty = self.y + speed*controls[2] - speed*controls[0]

        collisions = []

        #left
        if COORDTOTILE(nextx, self.y, tilemap) in SOLID_TILES:
            collisions.append('l')
        #right
        if COORDTOTILE(nextx+PLAYER_WIDTH, self.y, tilemap) in SOLID_TILES:
            collisions.append('r')
        #top
        if COORDTOTILE(self.x, nexty, tilemap) in SOLID_TILES:
            collisions.append('t')
        #bottom
        if COORDTOTILE(self.x, nexty+PLAYER_HEIGHT, tilemap) in SOLID_TILES:
            collisions.append('b')
        
        #bottomright
        if COORDTOTILE(nextx+PLAYER_WIDTH, nexty+PLAYER_HEIGHT, tilemap) in SOLID_TILES:
            collisions.append('b')
            collisions.append('r')
        
        #bottomleft
        if COORDTOTILE(nextx, nexty+PLAYER_HEIGHT, tilemap) in SOLID_TILES:
            collisions.append('b')
            collisions.append('l')

        return collisions

    def move(self, keys, tick, tilemap, walkSound):

        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        
        down = (w, a, s, d)


        collisions = self.collide(down, tilemap)

        if down not in [(1,0,1,0), (0,1,0,1), (0,0,0,0), (1,1,1,1)]:
            if not self.moving:
                self.sound(0, walkSound)
            self.moving = True
            if tick-self.lastmove > 120:
                self.frame += 1
                self.frame %= 4
                self.lastmove = tick

        else:
            self.sound(1, walkSound)
            self.moving = False
            self.frame = 0

        if w and not s:
            if not 't' in collisions:
                self.y -= self.PLAYER_SPEED
            self.frames = self.upFrames
        if s and not w:
            if not 'b' in collisions:
                self.y += self.PLAYER_SPEED
            self.frames = self.downFrames

        if a and not d:
            if not 'l' in collisions:
                self.x -= self.PLAYER_SPEED 
            self.frames = self.leftFrames
        
        if d and not a:
            if not 'r' in collisions:
                self.x += self.PLAYER_SPEED
            self.frames = self.rightFrames
        
        if w and a:
            self.x += self.PLAYER_SPEED*(1-math.sqrt(2)/2)
            self.y += self.PLAYER_SPEED*(1-math.sqrt(2)/2)
        if s and a:
            self.x += self.PLAYER_SPEED*(1-math.sqrt(2)/2)
            self.y -= self.PLAYER_SPEED*(1-math.sqrt(2)/2)
        if w and d:
            self.x -= self.PLAYER_SPEED*(1-math.sqrt(2)/2)
            self.y += self.PLAYER_SPEED*(1-math.sqrt(2)/2)
        if s and d:
            self.x -= self.PLAYER_SPEED*(1-math.sqrt(2)/2)
            self.y -= self.PLAYER_SPEED*(1-math.sqrt(2)/2)


        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def sound(self, stop, walkSound):
        if stop:
            walkSound.stop()
        else:
            walkSound.play(-1)
    
    
    def shoot(self, keys, tick, rockSound):
        mx, my = pygame.mouse.get_pos()
        qx, qy = OFFSET(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT, self.x, self.y)
        qx += PLAYER_WIDTH//2
        qy += PLAYER_HEIGHT//2

        rel_x, rel_y = mx - qx, my - qy
        mouse_angle = -math.radians((-180/math.pi) * math.atan2(rel_y, rel_x) - 90)
        if keys[K_SPACE] and tick - self.lastshot > self.stats[4]:
            rockSound.play()
            self.lastshot = tick
            temp = Projectile(self.x+PLAYER_WIDTH//2, self.y+PLAYER_HEIGHT//2, 0, 20, 20, mouse_angle, 10, 400, self.stats[1], (self.flame, self.leach, self.vampire))
            return temp

    def hit(self, projectile):
        if self.rect.colliderect(projectile.rect):
            self.lasthit = pygame.time.get_ticks()
            self.stats[0] -= projectile.dmg*2/(1+math.e**(0.01*self.stats[2]))
            return 1
        return 0
    
    def leacher(self, dealt):
        self.stats[0] += 0.1*dealt
    
    def vampirer(self, killed):
        if killed:
            self.stats[0] += self.maxstats[0] * 0.2

    def render(self, screen, hitImage):
        renderx, rendery = OFFSET(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT, self.x, self.y)
        
        
        screen.blit(self.frames[self.frame], (renderx, rendery))

        if pygame.time.get_ticks() - self.lasthit < 500:
            hitImage.set_alpha(64)
            screen.blit(hitImage, (0, 0))
    
