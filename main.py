__author__ = 'mark'
import pygame
import sys
import os
import gzip
import cPickle
from pygame.locals import *
import random

import generator
import block
import entity


TILESIZE = 32
MAP_X = 20
MAP_Y = 20
world = []
inv = []
entities = []
inventory_blocks = [block.BLOCK_STONE, block.BLOCK_DIRT, block.BLOCK_GRASS, block.BLOCK_DIAMOND,
                    block.BLOCK_LAVA, block.BLOCK_WATER]
player_pos = [5, 0]
god_mode = False

player_texture = pygame.image.load("textures/player.png")
current_block = block.BLOCK_STONE
falling = False
fall_delay = 0
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'grey': (127, 127, 127)
}


def load_game(filename):
    global world
    global inv
    global player_pos
    global entities
    try:
        save_file = gzip.open(filename, "rb")
        try:
            data = cPickle.load(save_file)
            try:
                world = data['world']
                inv = data['inventory']
                player_pos = data['position']
                entities = data['entities']
            except ValueError as err:
                print "Error parsing world data: \n %s" % err.message
        except cPickle.UnpicklingError as err:
            print "Error unpickling: \n %s" % err.message
    except IOError as ex:
        print "Unable to open save file: \n %s" % ex.message


def save_game(filename):
    global world
    global inv
    global player_pos
    global entities
    print "len of entities %d" % len(entities)
    entities_save = [cPickle.dumps(ent) for ent in entities]
    save_file = None

    try:
        try:
            save_file = gzip.open(filename, "wb")
        except IOError as err:
            print "Can not open file: \n %s" % err.message
        cPickle.dump({'world': world, 'inventory': inv, 'position': player_pos, 'entities': entities_save}, save_file,
                     cPickle.HIGHEST_PROTOCOL)
    except cPickle.PicklingError as err:
        print "Error pickling: \n %s" % err.message
    finally:
        save_file.close()


def new_world():
    global world, inv, player_pos, entities
    world = generator.generate_world(MAP_X, MAP_Y)
    # noinspection PyUnusedLocal
    inv = [0 for i in range(0, len(inventory_blocks))]
    player_pos = [5, 0]
    # We aren't going to call removed_hook(), because we are creating a new world
    entities = []


def tick():
    global player_pos, falling, fall_delay
    for en in entities:
        en.tick()
    if god_mode:
        falling = False
    if falling:
        fall_delay += 1

    elif player_pos[0] < MAP_X - 1 and 0 < player_pos and world[player_pos[1]][player_pos[0] + 1] in block.non_solid:
        falling = True
    if fall_delay == 3:
        player_pos[0] += 1
        fall_delay = 0
        falling = False

    for x2 in range(MAP_X):
        for y2 in range(MAP_Y):
            if world[x2][y2] == block.BLOCK_LAVA_FLOWING:
                if 0 < x2 < MAP_X - 1:
                    if world[x2 - 1][y2] == block.BLOCK_AIR:
                        world[x2 - 1][y2] = block.BLOCK_LAVA
                        break
                    elif world[x2 + 1][y2] == block.BLOCK_AIR:
                        world[x2 + 1][y2] = block.BLOCK_LAVA
                        break
                    elif 0 < y2 < MAP_Y - 1 and world[x2][y2 + 1] == block.BLOCK_AIR:
                        world[x2][y2 + 1] = block.BLOCK_LAVA_FLOWING
                        break
            elif world[x2][y2] == block.BLOCK_WATER_FLOWING:
                if 0 < x2 < MAP_X - 1:
                    if world[x2 - 1][y2] == block.BLOCK_AIR:
                        world[x2 - 1][y2] = block.BLOCK_WATER
                        break
                    elif world[x2 + 1][y2] == block.BLOCK_AIR:
                        world[x2 + 1][y2] = block.BLOCK_WATER
                        break
                    elif 0 < y2 < MAP_Y - 1 and world[x2][y2 + 1] == block.BLOCK_AIR:
                        world[x2][y2 + 1] = block.BLOCK_WATER_FLOWING
                        break
                        # elif world[x2][y2] == block.BLOCK_WATER_FLOWING:
                        #    if 0 < x2 < MAP_X - 1:
                        #        if world[x2 - 1][y2] == block.BLOCK_AIR:
                        #            world[x2 - 1][y2] = block.BLOCK_WATER_FLOWING
                        #            break
                        #        elif world[x2 + 1][y2] == block.BLOCK_AIR:
                        #            world[x2 + 1][y2] = block.BLOCK_WATER_FLOWING
                        #            break
                        #elif world[x2][y2] == block.BLOCK_LAVA_FLOWING:
                        #    if 0 < x2 < MAP_X - 1:
                        #        if world[x2 - 1][y2] == block.BLOCK_AIR:
                        #            world[x2 - 1][y2] = block.BLOCK_LAVA_FLOWING
                        #            break
                        #        elif world[x2 + 1][y2] == block.BLOCK_AIR:
                        #            world[x2 + 1][y2] = block.BLOCK_LAVA_FLOWING
                        #            break

                        #print "[DBG] Lava spread level: %d" % lava_spread
                        #print "[DBG] Water spread level: %d" % water_spread


def destroy_block(blk_x, blk_y, add_inventory=True):
    global world, inv
    blk = world[blk_x][blk_y]
    world[blk_x][blk_y] = block.BLOCK_AIR
    if add_inventory and blk in inventory_blocks:
        inv[inventory_blocks.index(blk)] += 1


def explode(exp_x, exp_y, exp_radius, add_inventory=False):
    for ex in range(exp_x - exp_radius, exp_x + exp_radius):
        for ey in range(exp_y - exp_radius, exp_y + exp_radius):
            if check_pos(ex, ey):
                if (ey - exp_radius) > (exp_radius / 2):
                    if random.randint(0, 8) < 8:
                        destroy_block(ex, ey, add_inventory)
                else:
                    destroy_block(ex, ey, add_inventory)


def check_pos(pos_x, pos_y):
    if 0 <= pos_x <= MAP_X - 1:
        if 0 <= pos_y <= MAP_Y - 1:
            # print "[DBG] check_pos(%d, %d) == True" % (pos_x, pos_y)
            return True
    # print "[DBG] check_pos(%d, %d) == False" % (pos_x, pos_y)
    return False


def spawn_entity(ent):
    ent.spawn_hook()
    entities.append(ent)
    return entities.index(ent)


def remove_entity(ent_id):
    entities[ent_id].removed_hook()
    entities.remove(entities[ent_id])


def game_over():
    gameover_font = pygame.font.SysFont("FreeSansBold", 38)
    gameover_label = gameover_font.render("GAME OVER :(, Press [SpaceBar]", True, COLORS['red'], COLORS['black'])
    DISPLAY.blit(gameover_label, (int(TILESIZE * MAP_X / 4), int(TILESIZE * MAP_Y / 2)))
    pygame.display.update()
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    new_world()
                    return
            elif evt.type == QUIT:
                save_game("explore_save.gz")
                pygame.quit()
                sys.exit()


def main_loop():
    global DISPLAY, player_pos, start_time, falling, fall_delay, god_mode, current_block, block_above, block_under,\
        font, block_index
    start_time = 0
    clk = pygame.time.Clock()
    while True:
        clk.tick(20)
        if pygame.time.get_ticks() - start_time >= 50:
            tick()
        start_time = pygame.time.get_ticks()

        px = player_pos[1]
        py = player_pos[0]
        block_under = world[px][py]
        block_above = world[px][py - 1] if py < 0 else -1
        prev_pos = player_pos[:]  # lists are mutable
        for event in pygame.event.get():
            if event.type == QUIT:
                save_game("explore_save.gz")
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == K_w and player_pos[0] in range(1, MAP_X) and (not falling or god_mode):
                    player_pos[0] -= 1
                    if not world[player_pos[1]][player_pos[0]] in block.non_solid and not keys[K_LSHIFT] and\
                            not god_mode:
                        player_pos = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = player_pos[1], player_pos[0]
                        destroy_block(bx, by)
                elif event.key == K_s and player_pos[0] in range(0, MAP_X - 1):
                    player_pos[0] += 1
                    if not world[player_pos[1]][player_pos[0]] in block.non_solid and not keys[K_LSHIFT]:
                        player_pos = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = player_pos[1], player_pos[0]
                        destroy_block(bx, by)
                elif event.key == K_a and player_pos[1] in range(1, MAP_Y):
                    falling = False
                    fall_delay = 0
                    player_pos[1] -= 1
                    if not world[player_pos[1]][player_pos[0]] in block.non_solid and not keys[K_LSHIFT]:
                        player_pos = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = player_pos[1], player_pos[0]
                        destroy_block(bx, by)
                elif event.key == K_d and player_pos[1] in range(0, MAP_Y - 1):
                    falling = False
                    fall_delay = 0
                    player_pos[1] += 1
                    if not world[player_pos[1]][player_pos[0]] in block.non_solid and not keys[K_LSHIFT]:
                        player_pos = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = player_pos[1], player_pos[0]
                        destroy_block(bx, by)
                elif event.key == K_z:
                    # print "Debug: placing block at %d %d, previous was %d" % (px, py, world[px][py])
                    if (inv[current_block] > 0 or god_mode) and block_under == block.BLOCK_AIR:
                        world[px][py] = inventory_blocks[current_block]
                        if not god_mode:
                            inv[current_block] -= 1
                elif event.key == K_x:
                    if world[px][py] in inventory_blocks:
                        if block_under in inventory_blocks:
                            block_index = inventory_blocks.index(block_under)
                            inv[block_index] += 1
                            world[px][py] = block.BLOCK_AIR
                elif event.key == K_1:
                    current_block = (current_block + 1) % len(inventory_blocks)
                elif event.key == K_ESCAPE:
                    new_world()
                elif event.key == K_F1:
                    god_mode = not god_mode
                elif event.key == K_e and god_mode:
                    explode(px, py, 5, True)
                elif event.key == K_n and god_mode:
                    if len(entities):
                        remove_entity(len(entities) - 1)  # last
                elif event.key == K_m and god_mode:
                    spawn_entity(entity.PlayerEntity(bounding_box=(0, 0, MAP_X, MAP_Y)))
                elif event.key == K_F5:
                    import datetime

                    pygame.image.save(DISPLAY, "2dexp-%s.png" % str(datetime.datetime.now()))
                    print "Saved screenshot"
        for x in range(MAP_X):
            for y in range(MAP_Y):
                DISPLAY.blit(block.textures[world[x][y]], (x * TILESIZE, y * TILESIZE))
                # gravity
                # newHeight = 0
                # while world[player_pos[0]][newHeight] == block.BLOCK_AIR:
                # newHeight += 1
                #player_pos[0] = newHeight - 1
        DISPLAY.blit(player_texture, (player_pos[1] * TILESIZE, player_pos[0] * TILESIZE))
        debug_text = "Coords: %d, %d   %d fps, block: " % (player_pos[0], player_pos[1], clk.get_fps()) + \
                     block.BLOCK_NAMES[block_under] + (" Entities: %d " % len(entities)) + \
                     (" GOD MODE" if god_mode else "")
        inventory_text = (" x %d" % inv[current_block]) + " " + block.BLOCK_NAMES.get(inventory_blocks[current_block],
                                                                                      "unknown")
        debug_label = font.render(debug_text, True, COLORS['white'], COLORS['black'])
        inventory_label = font.render(inventory_text, True, COLORS['white'], COLORS['black'])
        DISPLAY.blit(debug_label, (0, 0))
        DISPLAY.fill(0, (0, MAP_X * TILESIZE, MAP_Y * TILESIZE, 37))
        DISPLAY.blit(block.textures[inventory_blocks[current_block]], (0, MAP_Y * TILESIZE + 5))
        DISPLAY.blit(inventory_label, (32, MAP_Y * TILESIZE + 5))
        if block_under in block.deadly and not god_mode:
            game_over()
        for ent in entities:
            ent.render(DISPLAY, TILESIZE, TILESIZE)
        pygame.display.update()


pygame.init()
DISPLAY = pygame.display.set_mode((TILESIZE * MAP_X, TILESIZE * MAP_Y + 37))
pygame.display.set_caption("2DExplore")
font = pygame.font.SysFont("FreeSansBold", 18)  # Fonts should be inited after pygame.init()

if os.path.isfile("explore_save.gz"):
    load_game("explore_save.gz")
else:
    new_world()

main_loop()