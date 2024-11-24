import pygame
from resources import *
from random import randint
from projectile import Projectile

class Enemy:
    def __init__(self, x, y, imgs, name, width = PLAYER_WIDTH, height = PLAYER_HEIGHT):
        self.frames = []
        for i in range(imgs):
            temp = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            temp.convert_alpha()
            temp.set_colorkey((255,255,255))
            frame = pygame.image.load("imgs/" + name + "/"+str(i) + '.png')
            temp.blit(frame, (0,0))
            self.frames.append(temp)
        
        self.rightFrames = self.frames[0:2]
        self.leftFrames = self.frames[2:4]

        self.x = x
        self.y = y 

        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, width, height)

        #HP0, DMG1, ARMOR2, SPEED3, ATK4
        self.maxstats = [100, 100, 100, 3, 400]
        self.stats = [100, 100, 100, 3, 400]
        self.abilities = []

        self.flame = self.leach = self.vampire = False

        self.frame = 0
        self.lastmove = 0
        self.lastshot = 0
        self.lastframe = 0
    
    def move(self, tick, px, py, act):
        if tick - self.lastmove > 500:
            act = randint(1, 100)
            self.lastmove = tick

        speed = self.stats[3]

        shoot = randint(1, 30)

        shot = None

        if shoot == 1 and tick - self.lastshot > self.stats[4] and DIST(self.x, self.y, px, py) < 300:
            shot = self.shoot(px, py)
            self.lastshot = tick

        if 1 <= act <= 10:
            self.x += speed
            self.frames = self.rightFrames
        elif 11 <= act <= 20:
            self.x -= speed
            self.frames = self.leftFrames
        elif 21 <= act <= 30:
            self.y += speed
        elif 31 <= act <= 40:
            self.y -= speed
        elif 500> DIST (self.x, self.y, px, py) > 200:
            angle = 360-ANGLETOPOS(self.x, self.y, px, py)

            if 90 < math.degrees(angle)  % 360 < 270:
                self.frames = self.leftFrames
            else:
                self.frames = self.rightFrames

            self.x += math.cos(angle)*speed
            self.y += -math.sin(angle)*speed

        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

        if tick - self.lastframe > 200:
            self.frame += 1
            self.frame %= 2
            self.lastframe = tick

        return act, shot

    def shoot(self, px, py):
        angle = ANGLETOPOS(self.x+self.width//2, self.y+self.height//2, px, py)
        shot = Projectile(self.x + self.width//2, self.y+self.height//2, 0, 20, 20, angle, 10, 400, self.stats[1], (self.flame, self.leach, self.vampire))
        return shot
    
    def hit(self, projectile):
        if self.rect.colliderect(projectile.rect):
            dmg_dealt = projectile.dmg*2/(1+math.e**(0.01*self.stats[2]))
            self.stats[0] -= dmg_dealt
            return dmg_dealt
        return 0

    def render(self, px, py, screen):



        renderx, rendery = OFFSET(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT, px, py)
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(renderx, rendery - 30, self.width, 10))
        pygame.draw.rect(screen, (57, 255, 20), pygame.Rect(renderx, rendery - 30, self.width*self.stats[0]/self.maxstats[0], 10))

        screen.blit(self.frames[self.frame], (renderx, rendery))