import math

SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 640

MIDDLE_X = SCREEN_WIDTH//2
MIDDLE_Y = SCREEN_HEIGHT//2

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_L = MIDDLE_X - PLAYER_WIDTH//2
PLAYER_T = MIDDLE_Y - PLAYER_HEIGHT//2 

TILE_SIZE = 32
MAP_LENGTH = 140
MAP_HEIGHT = 80

SOLID_TILES = [8,9,10,13]

ENEMY_LOCS = [(700 + x*280, 700 + y*280) for x in range(13) for y in range(6)]

def OFFSET(x, y, width, height, px, py):

    renderx = x - px + PLAYER_L
    rendery = y - py + PLAYER_T

    if px < PLAYER_L:
        renderx = x
    elif px > MAP_LENGTH*TILE_SIZE - MIDDLE_X - PLAYER_WIDTH:
        renderx = x - MAP_LENGTH*TILE_SIZE + SCREEN_WIDTH + PLAYER_WIDTH//2

    if py < PLAYER_T:
        rendery = y
    elif py > MAP_HEIGHT*TILE_SIZE - MIDDLE_Y - PLAYER_HEIGHT:
        rendery = y - MAP_HEIGHT*TILE_SIZE + SCREEN_HEIGHT + PLAYER_HEIGHT//2

    return renderx, rendery

def COORDTOTILE(x, y, tilemap):
    return tilemap[int(y//32)][int(x//32)]

def ANGLETOPOS(x, y, px, py):
    rel_x, rel_y = px - x, py - y
    angle = -math.radians((-180/math.pi) * math.atan2(rel_y, rel_x) - 90)
    return angle

def DIST(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y2-y1)**2)