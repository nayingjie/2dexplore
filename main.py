__author__ = 'mark'
import pygame
import sys
import json
import os.path
import gzip
from pygame.locals import *

import generator
import block


TILESIZE = 32
MAP_X = 20
MAP_Y = 20
blocks = [block.BLOCK_STONE, block.BLOCK_DIRT, block.BLOCK_GRASS, block.BLOCK_DIAMOND,
          block.BLOCK_LAVA, block.BLOCK_WATER]
start_time = 0
player_pos = [5, 0]
god_mode = False
if os.path.isfile("explore_save.gz"):
    save_file = gzip.open("explore_save.gz", "r")
    try:
        savedata = json.load(save_file)
        world = savedata['world']
        inv = savedata['inventory']
        player_pos = savedata['position']
        if len(world) * len(world[0]) != MAP_X * MAP_Y:
            print "We got a world of len %d, but expected %d" % (len(world) * len(world[0]), MAP_X * MAP_Y)
            world = [[0 for x in range(MAP_X)] for y in range(MAP_Y)]
    except Exception as e:
        print "[DBG] Can't load saved world: %s" % str(e)
        world = generator.generate_world(MAP_X, MAP_Y)
        inv = [0 for x in range(0, len(blocks))]
    finally:
        save_file.close()
else:
    world = generator.generate_world(MAP_X, MAP_Y)
    inv = [0 for x in range(0, len(blocks))]
player_texture = pygame.image.load("textures/player.png")
current_block = block.BLOCK_STONE
falling = False
falldelay = 0
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'grey': (127, 127, 127)
}

non_solid = [block.BLOCK_AIR, block.BLOCK_LAVA, block.BLOCK_WATER]
textures = {
    block.BLOCK_STONE: pygame.image.load('textures/stone.png'),
    block.BLOCK_AIR: pygame.image.load('textures/air.png'),
    block.BLOCK_DIRT: pygame.image.load('textures/dirt.png'),
    block.BLOCK_GRASS: pygame.image.load('textures/grass.png'),
    block.BLOCK_DIAMOND: pygame.image.load('textures/diamond_ore.png'),
    block.BLOCK_LAVA: pygame.image.load('textures/lava.png'),
    block.BLOCK_WATER: pygame.image.load('textures/water.png')
}
pygame.init()
pygame.display.set_caption("2DExplore")
font = pygame.font.SysFont("FreeSansBold", 18)  # Fonts should be inited after pygame.init()
DISPLAY = pygame.display.set_mode((TILESIZE * MAP_X, TILESIZE * MAP_Y + 37))


def save_game():
    print "Saving game..."
    global world
    global inv
    global player_pos
    savefile = gzip.open("explore_save.gz", "w")
    try:
        json.dump({'world': world, 'inventory': inv, 'position': player_pos}, savefile)
    except Exception as ex:
        print "Error saving! %s" % str(ex)
    finally:
        savefile.close()


def new_world():
    global world, inv, player_pos
    world = generator.generate_world(MAP_X, MAP_Y)
    # noinspection PyUnusedLocal
    inv = [0 for i in range(0, len(blocks))]
    player_pos = [5, 0]


def tick():
    global player_pos, falling, falldelay
    if god_mode:
        falling = False
    lava_spread = 0
    water_spread = 0
    if falling:
        falldelay += 1

    elif player_pos[0] < MAP_X-1 and 0 < player_pos and world[player_pos[1]][player_pos[0]+1] in non_solid:
        falling = True
    if falldelay == 3:
        player_pos[0] += 1
        falldelay = 0
        falling = False
    for x2 in range(MAP_X):
        for y2 in range(MAP_Y):
            if world[x2][y2] == block.BLOCK_LAVA:
                if 0 < x2 < MAP_X - 1:
                    lava_spread += 1
                    if world[x2 - 1][y2] == block.BLOCK_AIR and lava_spread < 19:
                        world[x2 - 1][y2] = block.BLOCK_LAVA
                        lava_spread -= 8
                    elif world[x2 + 1][y2] == block.BLOCK_AIR and lava_spread < 19:
                        world[x2 + 1][y2] = block.BLOCK_LAVA
                        lava_spread -= 8
                    elif 0 < y2 < MAP_Y - 1 and world[x2][y2 + 1] == block.BLOCK_AIR:
                        world[x2][y2 + 1] = block.BLOCK_LAVA
                        lava_spread = 0
            elif world[x2][y2] == block.BLOCK_WATER:
                if 0 < x2 < MAP_X - 1:
                    water_spread += 1
                    if world[x2 - 1][y2] == block.BLOCK_AIR and water_spread < 15:
                        world[x2 - 1][y2] = block.BLOCK_WATER
                        water_spread -= 8
                    elif world[x2 + 1][y2] == block.BLOCK_AIR and water_spread < 15:
                        world[x2 + 1][y2] = block.BLOCK_WATER
                        water_spread -= 8
                    elif 0 < y2 < MAP_Y - 1 and world[x2][y2 + 1] == block.BLOCK_AIR:
                        world[x2][y2 + 1] = block.BLOCK_WATER
                        water_spread = 0
    #print "[DBG] Lava spread level: %d" % lava_spread
    #print "[DBG] Water spread level: %d" % water_spread

def destroy_block(bx, by):
    global world, inv
    blk = world[bx][by]
    if blk in blocks:
        world[bx][by] = block.BLOCK_AIR
        inv[blocks.index(blk)]+=1
clk = pygame.time.Clock()
while True:
    clk.tick(20)
    if pygame.time.get_ticks() - start_time >= 100:
        tick()
        start_time = pygame.time.get_ticks()
    game_over = False
    px = player_pos[1]
    py = player_pos[0]
    block_under = world[px][py]
    block_above = world[px][py - 1]
    prev_pos = player_pos[:]  # lists are mutable, so it's a workaround
    if block_under == block.BLOCK_LAVA and not god_mode:
        gameoverFont = pygame.font.SysFont("FreeSansBold", 38)
        gameoverLabel = gameoverFont.render("GAME OVER :(, Press [SpaceBar]", True, COLORS['red'], COLORS['black'])
        DISPLAY.blit(gameoverLabel, (200, 100))
        pygame.display.update()
        game_over = True
        while game_over:
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    if evt.key == K_SPACE:
                        new_world()
                        game_over = False
                elif evt.type == QUIT:
                    save_game()
                    pygame.quit()
                    sys.exit()
    for event in pygame.event.get():
        if event.type == QUIT:
            save_game()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if event.key == K_w and player_pos[0] in range(1, MAP_X) and (not falling or god_mode):
                player_pos[0] -= 1
                if not world[player_pos[1]][player_pos[0]] in non_solid and not keys[K_LSHIFT] and not god_mode:
                    player_pos = prev_pos
                if keys[K_LSHIFT]:
                    bx, by = player_pos[1], player_pos[0]
                    destroy_block(bx, by)
                else:
                    jumping = True
            elif event.key == K_s and player_pos[0] in range(0, MAP_X - 1):
                player_pos[0] += 1
                if not world[player_pos[1]][player_pos[0]] in non_solid and not keys[K_LSHIFT]:
                    player_pos = prev_pos
                if keys[K_LSHIFT]:
                    bx, by = player_pos[1], player_pos[0]
                    destroy_block(bx, by)
            elif event.key == K_a and player_pos[1] in range(1, MAP_Y):
                falling = False
                falldelay = 0
                player_pos[1] -= 1
                if not world[player_pos[1]][player_pos[0]] in non_solid and not keys[K_LSHIFT]:
                    player_pos = prev_pos
                if keys[K_LSHIFT]:
                    bx, by = player_pos[1], player_pos[0]
                    destroy_block(bx, by)
            elif event.key == K_d and player_pos[1] in range(0, MAP_Y - 1):
                falling = False
                falldelay = 0
                player_pos[1] += 1
                if not world[player_pos[1]][player_pos[0]] in non_solid and not keys[K_LSHIFT]:
                    player_pos = prev_pos
                if keys[K_LSHIFT]:
                    bx, by = player_pos[1], player_pos[0]
                    destroy_block(bx, by)
            elif event.key == K_z:
                # print "Debug: placing block at %d %d, previous was %d" % (px, py, world[px][py])
                if (inv[current_block] > 0 or god_mode) and block_under == block.BLOCK_AIR:
                    world[px][py] = blocks[current_block]
                    if not god_mode:
                        inv[current_block] -= 1
            elif event.key == K_x:
                if world[px][py] in blocks:
                    block_index = blocks.index(block_under)
                    inv[block_index] += 1
                    world[px][py] = block.BLOCK_AIR
            elif event.key == K_1:
                current_block = (current_block + 1) % len(blocks)
            elif event.key == K_ESCAPE:
                new_world()
            elif event.key == K_F1:
                god_mode = not god_mode
    for x in range(MAP_X):
        for y in range(MAP_Y):
            DISPLAY.blit(textures[world[x][y]], (x * TILESIZE, y * TILESIZE))
    # gravity
    # newHeight = 0
    #while world[player_pos[0]][newHeight] == block.BLOCK_AIR:
    #    newHeight += 1
    #player_pos[0] = newHeight - 1
    DISPLAY.blit(player_texture, (player_pos[1] * TILESIZE, player_pos[0] * TILESIZE))
    coordsLabel = font.render("Coords: %d, %d   %d fps" % (player_pos[0], player_pos[1], clk.get_fps())
                              , True, COLORS['white'], COLORS['black'])
    inventoryLabel = font.render(" x %d" % (inv[current_block]), True, COLORS['white'],
                                 COLORS['black'])
    DISPLAY.blit(coordsLabel, (0, 0))
    DISPLAY.fill(0, (0, MAP_X * TILESIZE, MAP_Y * TILESIZE, 37))
    DISPLAY.blit(textures[blocks[current_block]], (0, MAP_Y * TILESIZE + 5))
    DISPLAY.blit(inventoryLabel, (32, MAP_Y * TILESIZE + 5))
    pygame.display.update()
