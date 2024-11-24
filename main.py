import pygame
from stats import Profile, Card
from menu import handleClick
from tilemap import Tilemap, Tileset
from player import Player
from ability import Ability, abilityUpdate
from enemies import Enemy
import math
from random import randint
from resources import ENEMY_LOCS

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1120, 640))

mainImage = pygame.image.load("imgs/menu/main.png")
gameImage = pygame.image.load("imgs/menu/game.png")
shopImage = pygame.image.load("imgs/menu/shop.png")
equipImage = pygame.image.load("imgs/menu/equip.png")

cardImage = pygame.image.load("imgs/menu/card.png")
slotImage = pygame.image.load("imgs/menu/slot.png")
r1Image = pygame.image.load("imgs/menu/r1.png")
r2Image = pygame.image.load("imgs/menu/r2.png")
l1Image = pygame.image.load("imgs/menu/l1.png")
l2Image = pygame.image.load("imgs/menu/l2.png")

playImage1 = pygame.image.load("imgs/menu/play1.png")
playImage2 = pygame.image.load("imgs/menu/play2.png")
shopImage1 = pygame.image.load("imgs/menu/shop1.png")
shopImage2 = pygame.image.load("imgs/menu/shop2.png")
equipImage1 = pygame.image.load("imgs/menu/equip1.png")
equipImage2 = pygame.image.load("imgs/menu/equip2.png")
startImage1 = pygame.image.load("imgs/menu/start1.png")
startImage2 = pygame.image.load("imgs/menu/start2.png")

vamponImage = pygame.image.load("imgs/cards/vampon.png")
vampoffImage = pygame.image.load("imgs/cards/vampoff.png")
leachonImage = pygame.image.load("imgs/cards/leachon.png")
leachoffImage = pygame.image.load("imgs/cards/leachoff.png")

barImage = pygame.image.load("imgs/stats/bar.png")
lostImage = pygame.image.load("imgs/stats/lost.png")
heartImage = pygame.image.load("imgs/stats/heart.png")
shieldImage = pygame.image.load("imgs/stats/shield.png")
swordImage = pygame.image.load("imgs/stats/sword.png")

walkSound = pygame.mixer.Sound("imgs/audio/walking.wav")
clickSound = pygame.mixer.Sound("imgs/audio/click.wav")
homeSound = pygame.mixer.Sound("imgs/audio/home.wav")
gameSound = pygame.mixer.Sound("imgs/audio/music2.mp3")
rockSound = pygame.mixer.Sound("imgs/audio/rock.wav")
cardSound = pygame.mixer.Sound("imgs/audio/card.wav")

hitImage = pygame.image.load("imgs/misc/3.png")


CARDCOUNT = 13
cardImages = []
for i in range(CARDCOUNT):
    cardImages.append(pygame.image.load('imgs/cards/' + str(i+1) + '.png'))

rage = Ability("Rage", 2000, "r")
wave = Ability("Shockwave", 15000, "e")
flame = Ability("Flame Trail", 30000, "f")
storm = Ability("Chaos Storm", 60000, "c")
leach = Ability("Life Leach", 0, "")
vampire = Ability("Vampire", 0, "")

Card.cardList.append((50, 20, 0, 0, 15, leach, cardImages[0]))
Card.cardList.append((35, 10, 5, 0, 10, vampire, cardImages[1]))
Card.cardList.append((40, 0, 20, 0, 0, rage, cardImages[2]))
Card.cardList.append((75, 15, 10, 0, 10, wave, cardImages[3]))
Card.cardList.append((100, 15, 10, 0, 10, flame, cardImages[4]))
Card.cardList.append((200, 30, 30, 0, 25, storm, cardImages[5]))
Card.cardList.append((10, 25, 0, 0, 0, None, cardImages[6]))
Card.cardList.append((15, 0, 20, 0, 0, None, cardImages[7]))
Card.cardList.append((10, 0, 0, 0, 20, None, cardImages[8]))
Card.cardList.append((150, 50, 50, 0, 50, None, cardImages[9]))
Card.cardList.append((50, 0, 0, 1, 0, None, cardImages[10]))
Card.cardList.append((70, 0, 40, -1, 50, None, cardImages[11]))
Card.cardList.append((80, 50, -30, 2, 0, None, cardImages[12]))

profile = Profile()
profile.fillShop()

tileset = Tileset(1, 18, 'ground', 32)
tilemap = Tilemap.floor1(tileset.tiles)

p = Player(16, "player")

act = {}

playerProjectiles = []
enemyProjectiles = []
enemylist = []


abilities = []

def startGame():
    global tileset, tilemap, p, playerProjectiles, enemyProjectiles, enemylist, act, abilities
    tileset = Tileset(1, 18, 'ground', 32)
    tilemap = Tilemap.floor1(tileset.tiles)

    p = Player(16, "player")

    act = {}

    playerProjectiles = []
    enemyProjectiles = []
    enemylist = []


    p.stats[0] = profile.hp
    p.stats[1] = profile.dmg
    p.stats[2] = profile.armor
    p.stats[3] = profile.speed
    p.stats[4] = 200
    abilities = []
    for i in range(10):
        if profile.active[i] and profile.active[i].ability:
            print(profile.active[i].ability.name)
            if profile.active[i].ability.name == "Life Leach":
                p.leach = True
            elif profile.active[i].ability.name == "Vampire":
                p.vampire = True
            else:
                abilities.append(profile.active[i].ability)

def introDisplay():
    screen.blit(mainImage, (0, 0))
    if pygame.Rect(320, 440, 287, 99).collidepoint(pygame.mouse.get_pos()):
        screen.blit(startImage2, (320, 440))
    else:
        screen.blit(startImage1, (320, 440))

def startDisplay():
    screen.blit(gameImage, (0, 0))

    if pygame.Rect(80, 80, 430, 160).collidepoint(pygame.mouse.get_pos()):
        screen.blit(playImage2, (80, 80))
    else:
        screen.blit(playImage1, (80, 80))

    if pygame.Rect(80, 250, 430, 160).collidepoint(pygame.mouse.get_pos()):
        screen.blit(shopImage2, (80, 250))
    else:
        screen.blit(shopImage1, (80, 250))

    if pygame.Rect(80, 420, 430, 160).collidepoint(pygame.mouse.get_pos()):
        screen.blit(equipImage2, (80, 420))
    else:
        screen.blit(equipImage1, (80, 420))

def statDisplay():
    screen.blit(lostImage, (800, 20))
    screen.blit(barImage, (800, 20), (0, 0, 300*((p.stats[0]/p.maxhp)), 60))
    screen.blit(heartImage, (780, 20))
    screen.blit(shieldImage, (780, 85))
    screen.blit(swordImage, (780, 150))

    screen.blit(pygame.font.Font('fonts/start2p.ttf', 30).render(f"{p.stats[2]}", False, (255, 255, 255)), (870, 100))
    screen.blit(pygame.font.Font('fonts/start2p.ttf', 30).render(f"{p.stats[1]}", False, (255, 255, 255)), (870, 170))

    if p.leach:
        screen.blit(leachonImage, (20, 20))
    else:
        screen.blit(leachoffImage, (20, 20))
    if p.vampire:
        screen.blit(vamponImage, (100, 20))
    else:
        screen.blit(vampoffImage, (100, 20))

def spawn_enemies(wave):
    if wave == 1:
        for i in ENEMY_LOCS:
            if randint(1,4) == 1:
                new_enemy = Enemy(i[0], i[1], 4, "ghost")
                enemylist.append(new_enemy)
                act[new_enemy] = 0

clock = pygame.time.Clock()
running = True
mode = "intro"

homeSound.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if mode != "play":
                mode = handleClick(mode, profile, clickSound, gameSound)
                if mode == "play":
                    startGame()
                    spawn_enemies(1)
            

    if mode == "intro":
        introDisplay()
    if mode == "start":
        startDisplay()
    if mode == "shop":
        profile.displayShop(screen, shopImage, slotImage)
    if mode == "equip":
        profile.displayEquipMenu(screen, equipImage, slotImage, cardImage, l1Image, l2Image, r1Image, r2Image)
    if mode == "play":
        homeSound.stop()
        tilemap.render(p.x, p.y, screen)

        keys = pygame.key.get_pressed()
        p.move(keys, pygame.time.get_ticks(), tilemap.tilemap, walkSound)
        tt = p.shoot(keys, pygame.time.get_ticks(), rockSound)
        if tt != None:
            playerProjectiles.append(tt)
        


        for npc in enemylist:
            act_t, shot = npc.move(pygame.time.get_ticks(), p.x, p.y, act[npc])
            act[npc] = act_t
            npc.render(p.x, p.y, screen)
        
            if shot != None:
                enemyProjectiles.append(shot)

        p.render(screen, hitImage)

        for i in playerProjectiles:
            enemylist, dealt, killed = i.collide(enemylist)
            if dealt:
                if p.leach:
                    p.leacher(dealt)
                if p.vampire:
                    p.vampirer(killed)
                if killed:
                    profile.coins += 1
                playerProjectiles.remove(i)
                del(i)
            else:
                if not i.update():
                    playerProjectiles.remove(i)
                    del(i)
                    continue
                i.render(p.x, p.y, screen)

            
                    
        
        for i in enemyProjectiles:
            if p.hit(i):
                enemyProjectiles.remove(i)
                del(i)
                print(p.stats[0])
                break
            if not i.update():
                del(i)
                continue
            i.render(p.x, p.y, screen)

        for i in range(len(abilities)):
            status = abilities[i].activate(pygame.key.get_pressed(), pygame.time.get_ticks())
            abilities[i].display(screen, i, pygame.time.get_ticks())
        
            if status:
                abilityUpdate(abilities[i].name, status, p)
            
        statDisplay()


    pygame.display.update()
    clock.tick(30)
