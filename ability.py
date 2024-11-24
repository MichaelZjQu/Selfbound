import pygame

d = {"Rage": 0, "Flame Trail": 1, "Shockwave": 2, "Chaos Storm": 3, "Life Leach": 4, "Vampire": 5}
images = [pygame.image.load("imgs/abil/Rage.png"), pygame.image.load("imgs/abil/Flame.png"), pygame.image.load("imgs/abil/Shockwave.png"),
          pygame.image.load("imgs/abil/Storm.png"), pygame.image.load("imgs/abil/Leach.png"), pygame.image.load("imgs/abil/Vampire.png"),]

def abilityUpdate(name, status, p):
    print(name, status)

    if name == "Rage":
        if status == "s":
            p.stats[1] *= 1.5
        if status == "e":
            p.stats[1] /= 1.5

    if name == "Flame Trail":
        if status == "s":
            p.stats[1] *= 1.5
        if status == "e":
            p.stats[1] /= 1.5

    if name == "Shockwave":
        if status == "s":
            p.stats[1] *= 1.5
        if status == "e":
            p.stats[1] /= 1.5

    if name == "Chaos Storm":
        if status == "s":
            p.stats[1] *= 1.5
        if status == "e":
            p.stats[1] /= 1.5

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    shape_surf.set_alpha(70)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

class Ability:
    def __init__(self, name, cd, key):
        self.name = name
        self.cd = cd
        self.key = key
        # self.image = pygame.image.load('imgs/abil/' + name + '.png')

        self.canUse = True
        self.start = 0

    def activate(self, keys, tick):
        if keys[ord(self.key)] and self.canUse == True:
            self.canUse = False
            self.start = tick
            return "s"

        if not self.canUse and tick - self.start >= self.cd:
            self.canUse = True
            return "e"

    def display(self, screen, index, tick):
        if self.canUse:
            screen.blit(images[d[self.name]], (20+(120*index), 540))
        if not self.canUse:
            screen.blit(images[d[self.name]], (20+(120*index), 540))
            draw_rect_alpha(screen, (255, 255, 255), pygame.Rect(20+(120*index), 540, 100, 100-100*(tick - self.start)/self.cd))