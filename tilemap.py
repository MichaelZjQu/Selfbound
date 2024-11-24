import pygame
from resources import *

class Tileset:


    def __init__(self, floor, imgs, name, size):
        """
        Init tileset from file

        Args:
        - imgs(int) - # of imgs
        - name(string) - filepath
        - size(int) - tile side length
        """
        self.tiles = []
        for i in range(imgs):
            surf = pygame.Surface((size,size), pygame.SRCALPHA, 32)
            tile = pygame.image.load("imgs/"+ name + "/"+ str(floor) + "/" +str(i) +'.png')
            tile.convert_alpha()
            surf.blit(tile, (0,0))
            self.tiles.append(surf)


from random import randint

class Tilemap:

    def __init__(self, tileset):
        """
        Init blank tilemap

        Args:
        - tileset (list(pygame.Surface))        
        """
        self.tileset = tileset

    @classmethod
    def floor1(cls, tileset):
        mp = cls(tileset)
        #grass
        mp.tilemap = [[randint(5, 7) for i in range(MAP_LENGTH)] for j in range(MAP_HEIGHT)]

        

        #dirt
        
        for j in range(10):
            for i in range(MAP_LENGTH-1):
                mp.tilemap[i//2 + j - 2][i] = randint(0, 4)

        for i in range(100):
            mp.tilemap[randint(0, MAP_HEIGHT-1)][randint(0, MAP_LENGTH-1)] = randint(11,12)
        for i in range(10):
            x, y = randint(16, MAP_HEIGHT-5), randint(16, MAP_LENGTH-5)
            for j in range(4):
                if randint(0, 1) == 0:
                    mp.tilemap[x+j][y-1] = randint(8, 10)
                if randint(0, 1) == 0:
                    mp.tilemap[x+j][y+4] = randint(8, 10)
                if randint(0, 1) == 0:
                    mp.tilemap[x-1][y+j] = randint(8, 10)
                if randint(0, 1) == 0:
                    mp.tilemap[x+4][y+j] = randint(8, 10)
                for k in range(4):
                    
                    mp.tilemap[x+j][y+k] = randint(8, 10)
            
            

        #bricks
        for i in range(MAP_LENGTH):
            mp.tilemap[0][i] = mp.tilemap[-2][i] = 13
        for i in range(MAP_HEIGHT):
            mp.tilemap[i][0] = mp.tilemap[i][-2] = 13
        return mp
        
    def render(self, px, py, screen):
        x = 0
        y = 0

        for i in self.tilemap:
            for j in i:
                renderx, rendery = OFFSET(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, px, py)

                screen.blit(self.tileset[j], (renderx, rendery))
                x += 1
            x = 0
            y += 1

    