import pygame
from resources import ENEMY_LOCS
from tilemap import Tilemap, Tileset
from player import Player
from projectile import Projectile
from enemies import Enemy
import math
from random import randint


pygame.init()


screen = pygame.display.set_mode((1120,640))

tileset = Tileset(1, 14, 'ground', 32)

tilemap = Tilemap.floor1(tileset.tiles)

clock = pygame.time.Clock()
player = Player(16, "player")


running = True
act = {}

playerProjectiles = []
enemyProjectiles = []
enemylist = []


def spawn_enemies(wave):
    if wave == 1:
        for i in ENEMY_LOCS:
            if randint(1,4) == 1:
                new_enemy = Enemy(i[0], i[1], 4, "ghost")
                enemylist.append(new_enemy)
                act[new_enemy] = 0




spawn_enemies(1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tilemap.render(player.x, player.y, screen)

    keys = pygame.key.get_pressed()
    player.move(keys, pygame.time.get_ticks(), tilemap.tilemap)
    tt = player.shoot(keys, pygame.time.get_ticks())
    if tt != None:
        playerProjectiles.append(tt)
    player.render(screen)


    for npc in enemylist:
        act_t, shot = npc.move(pygame.time.get_ticks(), player.x, player.y, act[npc])
        act[npc] = act_t
        npc.render(player.x, player.y, screen)
    
        if shot != None:
            enemyProjectiles.append(shot)

    for i in playerProjectiles:
        enemylist, dealt, killed = i.collide(enemylist)
        if dealt:
            if player.leach:
                player.leacher(dealt)
            if player.vampire:
                player.vampirer(killed)
            playerProjectiles.remove(i)
            del(i)
        else:
            if not i.update():
                playerProjectiles.remove(i)
                del(i)
                continue
            i.render(player.x, player.y, screen)

        
                
    
    for i in enemyProjectiles:
        if player.hit(i):
            enemyProjectiles.remove(i)
            del(i)
            print(player.stats[0])
            break
        if not i.update():
            del(i)
            continue
        i.render(player.x, player.y, screen)

        
    
    pygame.display.flip()



    clock.tick(30)
