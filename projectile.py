import pygame
from resources import *

from math import sin, cos

class Projectile:

    

    def __init__(self, x, y, imgn, width, len, dir, speed, range, dmg, spec):
        temp = pygame.Surface((width, len), pygame.SRCALPHA, 32)
        temp.convert_alpha()
        img = pygame.image.load("imgs/proj/" + str(imgn) + '.png')
        temp.blit(img, (0, 0))
        self.image = temp
        self.rect = pygame.Rect(x, y, len, width)
        
        self.flame, self.leach, self.vampire = spec

        self.dir = dir
        self.speed = speed
        self.range = range
        self.dmg = dmg

        

        self.x = self.startx = x
        self.y = self.starty = y

        
        self.xgoal = round(x + sin(dir) * self.range)
        self.ygoal = round(y + -cos(dir) * self.range)

    def collide(self, npclist):
        dealt = 0
        killed = False
        for i in npclist:
            dealt = i.hit(self)
            if dealt:
                if i.stats[0] <= 0:
                    npclist.remove(i)
                    killed = True
                    del(i)
                break
        return npclist, dealt, killed

    def update(self):

        x_rate = sin(self.dir)*self.speed
        y_rate = -cos(self.dir)*self.speed
    

        if self.rect.left != self.xgoal or self.rect.top != self.ygoal:
            self.x += min(x_rate, self.xgoal - self.rect.left, key=abs)
            self.y += min(y_rate, self.ygoal - self.rect.top, key=abs)
            self.rect = pygame.Rect(round(self.x), round(self.y), self.rect.width, self.rect.height)
            return 1
        else:
            return 0


    def render(self, px, py, screen):
        renderx, rendery = OFFSET(self.rect.left, self.rect.top, self.rect.width, self.rect.height, px, py)

        screen.blit(self.image, (renderx, rendery))
