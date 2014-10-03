__author__ = 'mark'
import generator, block
import pygame
import sys
import json
import os.path
import gzip
from pygame.locals import *
TILESIZE = 32
MAP_X = 16
MAP_Y = 16
blocks = [block.BLOCK_STONE, block.BLOCK_DIRT, block.BLOCK_GRASS]
if os.path.isfile("explore_save.gz"):
    save_file = gzip.open("explore_save.gz", "r")
    try:
        savedata = json.load(save_file)
        world = savedata[0]
        inv = savedata[1]
    except:
        world = generator.generate_world(MAP_X, MAP_Y)
        inv = [0 for x in range(0, len(blocks))]
    finally:
        save_file.close()
else:
    world = generator.generate_world(MAP_X, MAP_Y)
    inv = [0 for x in range(0, len(blocks))]
player_texture = pygame.image.load("textures/player.png")
player_pos = [0, 0]
current_block = block.BLOCK_STONE
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'grey': (127, 127, 127)
}
textures = {
    block.BLOCK_STONE: pygame.image.load('textures/stone.png'),
    block.BLOCK_AIR: pygame.image.load('textures/air.png'),
    block.BLOCK_DIRT: pygame.image.load('textures/dirt.png'),
    block.BLOCK_GRASS: pygame.image.load('textures/grass.png')
}
pygame.init()
font = pygame.font.SysFont("FreeSansBold", 18) # Fonts should be inited after pygame.init()
DISPLAY = pygame.display.set_mode((TILESIZE * MAP_X, TILESIZE * MAP_Y + 37))

def save_game():
    print "Saving game..."
    global world
    global inv
    savefile = gzip.open("explore_save.gz", "w")
    try:
        json.dump([world, inv], savefile)
    except Exception as e:
        print "Error saving! %s" % str(e)
    finally:
        savefile.close()

def new_world():
    global world, inv
    world = generator.generate_world(MAP_X, MAP_Y)
    inv = [0 for x in range(0, len(blocks))]

while True:
    px = player_pos[1]
    py = player_pos[0]
    block_under = world[px][py]
    for event in pygame.event.get():
        if event.type == QUIT:
            save_game()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_w and player_pos[0] in range(1, MAP_X):
                player_pos[0] -= 1
            elif event.key == K_s and player_pos[0] in range(0, MAP_X - 1):
                player_pos[0] += 1
            elif event.key == K_a and player_pos[1] in range(1, MAP_Y):
                player_pos[1] -= 1
            elif event.key == K_d and player_pos[1] in range(0, MAP_Y - 1):
                player_pos[1] += 1
            elif event.key == K_z:
                #print "Debug: placing block at %d %d, previous was %d" % (px, py, world[px][py])
                if inv[current_block] > 0 and block_under == block.BLOCK_AIR:
                    world[px][py] = blocks[current_block]
                    inv[current_block] -= 1
            elif event.key == K_x:
                if world[px][py] in blocks:
                    block_index = blocks.index(block_under)
                    inv[block_index] += 1
                    world[px][py] = block.BLOCK_AIR
            elif event.key == K_1:
                current_block = (current_block+1) % len(blocks)
            elif event.key == K_ESCAPE:
                new_world()

    for x in range(MAP_X):
        for y in range(MAP_Y):
            DISPLAY.blit(textures[world[x][y]], (x*TILESIZE, y*TILESIZE))
    # gravity
    #newHeight = 0
    #while world[player_pos[0]][newHeight] == block.BLOCK_AIR:
    #    newHeight += 1
    #player_pos[0] = newHeight - 1
    DISPLAY.blit(player_texture, (player_pos[1]*TILESIZE, player_pos[0]*TILESIZE))
    coordsLabel = font.render("Coords: %d, %d" % (player_pos[0], player_pos[1]), True, COLORS['white'],
                              COLORS['black'])
    inventoryLabel = font.render(" x %d" % (inv[current_block]), True, COLORS['white'],
                              COLORS['black'])
    DISPLAY.blit(coordsLabel, (0, 0))
    DISPLAY.fill(0, (0, MAP_X*TILESIZE, MAP_Y*TILESIZE, 37))
    DISPLAY.blit(textures[blocks[current_block]], (0, MAP_Y*TILESIZE+5))
    DISPLAY.blit(inventoryLabel, (32, MAP_Y*TILESIZE+5))
    pygame.display.update()