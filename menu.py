import pygame
from stats import Profile

def handleClick(mode, profile, clickSound, gameSound, homeSound):
    clickSound.set_volume(0.4)
    clickSound.play()

    if mode == "end":
        if pygame.Rect(335, 482, 439, 105).collidepoint(pygame.mouse.get_pos()):
            gameSound.stop()
            homeSound.play(-1)
            profile.fillShop()
            return "start"
    if mode == "win":
        if pygame.Rect(335, 482, 439, 105).collidepoint(pygame.mouse.get_pos()):
            gameSound.stop()
            homeSound.play(-1)
            profile.fillShop()
            return "intro"
    if mode == "intro":
        if pygame.Rect(320, 440, 287, 99).collidepoint(pygame.mouse.get_pos()):
            return "start"
    if mode == "start":
        if pygame.Rect(80, 80, 430, 160).collidepoint(pygame.mouse.get_pos()):
            gameSound.set_volume(0.5)
            gameSound.play(-1)
            homeSound.stop()
            return "play"
        if pygame.Rect(80, 250, 430, 160).collidepoint(pygame.mouse.get_pos()):
            # profile.fillShop()
            return "shop"
        if pygame.Rect(80, 420, 430, 160).collidepoint(pygame.mouse.get_pos()):
            profile.select = -1
            return "equip"
    if mode == "shop":
        if pygame.Rect(65, 68, 95, 89).collidepoint(pygame.mouse.get_pos()):
            return "start"
        
        for i in range(5):
            if pygame.Rect(197+(i*150), 50, 125, 175).collidepoint(pygame.mouse.get_pos()) and profile.shop[i]:
                if profile.coins >= profile.shop[i].cost:
                    profile.coins -= profile.shop[i].cost
                    profile.getCard(profile.shop[i])
                    profile.shop[i] = None

        for i in range(5):
            if pygame.Rect(197+(i*150), 250, 125, 175).collidepoint(pygame.mouse.get_pos()) and profile.shop[i+5]:
                if profile.coins >= profile.shop[i+5].cost:
                    profile.coins -= profile.shop[i+5].cost
                    profile.getCard(profile.shop[i+5])
                    profile.shop[i+5] = None

    if mode == "equip":
        if pygame.Rect(65, 68, 95, 89).collidepoint(pygame.mouse.get_pos()):
            return "start"

        if profile.select == -1:
            if  pygame.Rect(20, 450, 80, 175).collidepoint(pygame.mouse.get_pos()):
                profile.inventoryIndex = max(0, profile.inventoryIndex-1)
            if pygame.Rect(1020, 450, 80, 175).collidepoint(pygame.mouse.get_pos()):
                profile.inventoryIndex = min(profile.inventoryIndex+1, max(0, Profile.totalCards-6))

            for i in range(6):
                if pygame.Rect(122+(i*150), 450, 125, 175).collidepoint(pygame.mouse.get_pos()) and i+profile.inventoryIndex < len(profile.inventory):
                    if profile.inventory[i+profile.inventoryIndex].using == 0:
                        profile.select = i + profile.inventoryIndex    

        else:
            for i in range(5):
                if pygame.Rect(197+(i*150), 25, 125, 175).collidepoint(pygame.mouse.get_pos()):
                    if profile.active[i]:
                        profile.active[i].using = 0
                    profile.active[i] = profile.inventory[profile.select]
                    profile.inventory[profile.select].using = 1
                    profile.updateStats()
                    
            for i in range(5):
                if pygame.Rect(197+(i*150), 225, 125, 175).collidepoint(pygame.mouse.get_pos()):
                    if profile.active[i+5]:
                        profile.active[i+5].using = 0
                    profile.active[i+5] = profile.inventory[profile.select]
                    profile.inventory[profile.select].using = 1
                    profile.updateStats()

            profile.select = -1

    return mode