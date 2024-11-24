import pygame, random
from ability import Ability

class Profile:
    totalCards = 0
    def __init__(self):
        self.hp = 100
        self.dmg = 100
        self.armor = 0
        self.speed = 5
        self.coins = 0
        self.active = [None for i in range(10)]
        self.inventory = []
        self.shop = [None for i in range(10)]
        self.inventoryIndex = 0
        self.select = -1

    def getCard(self, card):
        self.inventory.append(card)
        Profile.totalCards += 1
    
    def updateStats(self):
        self.hp = 100
        self.dmg = 100
        self.armor = 0
        self.speed = 5

        for i in range(10):
            if self.active[i]:
                self.hp += self.active[i].hp
                self.dmg += self.active[i].dmg
                self.armor += self.active[i].armor
                self.speed += self.active[i].speed
            
        print(self.hp, self.dmg, self.armor, self.speed)

    def fillShop(self):
        cards = random.sample(range(0, 12), 10)

        for i in range(10):
            self.shop[i] = Card.cardFromNum(cards[i])
            for j in range(Profile.totalCards):
                if self.inventory[j].ability and self.inventory[j].ability == self.shop[i].ability:
                    self.shop[i] = None
                    break

    def displayEquipMenu(self, screen, equipImage, slotImage, cardImage, l1Image, l2Image, r1Image, r2Image):
        screen.blit(equipImage, (0, 0))

        if self.select != -1:
            pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(112+((self.select-self.inventoryIndex)*150), 440, 145, 195))

        for i in range(5):
            if self.active[i]:
                screen.blit(self.active[i].image,(197+(i*150), 25))
            else:
                screen.blit(slotImage,(197+(i*150), 25))
        
        for i in range(5):
            if self.active[i+5]:
                screen.blit(self.active[i+5].image,(197+(i*150), 225))
            else:
                screen.blit(slotImage,(197+(i*150), 225))

        for i in range(6):
            if 0 <= i+self.inventoryIndex < Profile.totalCards:
                if self.inventory[i+self.inventoryIndex].using:
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(112+(i*150), 440, 145, 195))
                screen.blit(self.inventory[i+self.inventoryIndex].image, (122+(i*150), 450))
            else:
                screen.blit(cardImage,(122+(i*150), 450))

        if self.inventoryIndex == 0:
            screen.blit(l2Image, (20, 475))
        else:
            screen.blit(l1Image, (20, 475))
        if self.inventoryIndex ==  max(0, Profile.totalCards-6):
            screen.blit(r2Image, (1020, 475))
        else:
            screen.blit(r1Image, (1020, 475))

    def displayShop(self, screen, shopImage, slotImage):
        screen.blit(shopImage, (0,0))

        for i in range(5):
            if self.shop[i]:
                screen.blit(self.shop[i].image, (197+(i*150), 50))
            else:
                screen.blit(slotImage,(197+(i*150), 50))
        for i in range(5):
            if self.shop[i+5]:
                screen.blit(self.shop[i+5].image, (197+(i*150), 250))
            else:
                screen.blit(slotImage,(197+(i*150), 250))

        screen.blit(pygame.font.Font('fonts/start2p.ttf', 35).render(f"{self.coins}", False, (255, 255, 255)), (900, 515))

class Card:
    cardList = []
    def __init__(self, cost, hp, dmg, speed, armor, ability, image, using=0):
        self.cost = cost
        self.hp = hp
        self.dmg = dmg
        self.speed = speed
        self.armor = armor
        self.ability = ability
        self.image = image
        self.using = using

    @classmethod
    def cardFromNum(cls, num):
        return cls(Card.cardList[num][0], Card.cardList[num][1], Card.cardList[num][2], Card.cardList[num][3], Card.cardList[num][4], Card.cardList[num][5], Card.cardList[num][6])
    