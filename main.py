from player_entity import PlayerEntity
# TODO: make a better random with probability
__author__ = 'mark'
import pygame
import sys
import os
from pygame.locals import *
import world
import block
block.load_textures()  # ...
SAVE_FILE = "explore_save.gz"
TILESIZE = 32
MAP_X = 52
MAP_Y = 52
screen=pygame.display.set_mode((800,800))
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'grey': (127, 127, 127)
}
sx = 0
sy = 0
def load(filename):
    import cPickle, gzip
    global wrl
    try:
        world_file = gzip.open(filename, "rb")
        wrl = cPickle.load(world_file)
    except IOError as err:
        print "Unable to open the file! \n %s" % err.message
    except cPickle.UnpicklingError as err:
        print "Error unpickling! \n %s" % err.message


def save(filename):
    import cPickle, gzip
    global wrl
    try:
        world_file = gzip.open(filename, "wb")
        cPickle.dump(wrl, world_file, cPickle.HIGHEST_PROTOCOL)
    except IOError as err:
        print "Unable to open the file! \n %s" % err.message
    except cPickle.PicklingError as err:
        print "Error pickling! \n %s" % err.message
        
def game_over():
    gameover_font = pygame.font.SysFont("FreeSansBold", 38)
    gameover_label = gameover_font.render("GAME OVER, press space bar", True, COLORS['red'], COLORS['black'])
    DISPLAY.blit(gameover_label, (800, 800))
    pygame.display.update()
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    wrl.new_world(MAP_X, MAP_Y)
                    return
            elif evt.type == QUIT:
                save(SAVE_FILE)
                pygame.quit()
                sys.exit()


def main_loop():
    global DISPLAY, start_time, fall_delay, displae, block_above, block_under, block_index, wrl, xs, ys
    ys = 0
    xs = 0
    font = pygame.font.SysFont("UbuntuMono", 13)  # Fonts should be inited after pygame.init()
    start_time = 0
    clk = pygame.time.Clock()
    while True:
        clk.tick(20)
        if pygame.time.get_ticks() - start_time >= 50:
            wrl.tick()
        start_time = pygame.time.get_ticks()
        px = wrl.player.coords[1]
        py = wrl.player.coords[0]
        block_under = wrl.level[px][py]
        block_above = wrl.level[px][py - 1] if py < 0 else -1
        prev_pos = wrl.player.coords[:]  # lists are mutable
        for event in pygame.event.get():
            if event.type == QUIT:
                save(SAVE_FILE)
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == K_LEFT:
                    xs += 32
                if event.key == K_RIGHT:
                    xs += -32
                if event.key == K_UP:
                    ys += 32
                if event.key == K_DOWN:
                    ys += -32


                #W KEY - UP
                if event.key == K_w and wrl.player.coords[0] in range(1, MAP_X) and (not wrl.player.falling or wrl.player.god_mode):
                    wrl.player.coords[0] -= 1
                    playerUp = True
                    if not wrl.level[wrl.player.coords[1]][wrl.player.coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT] and\
                            not wrl.player.god_mode:
                        wrl.player.coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = wrl.player.coords[1], wrl.player.coords[0]
                        wrl.destroy_block(bx, by)
                            #S KEY - DOWN
                elif event.key == K_s and wrl.player.coords[0] in range(0, MAP_X - 1):
                    wrl.player.coords[0] += 1
                    if not wrl.level[wrl.player.coords[1]][wrl.player.coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT]:
                        wrl.player.coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = wrl.player.coords[1], wrl.player.coords[0]
                        wrl.destroy_block(bx, by)
                            #A KEY - LEFT
                elif event.key == K_a and wrl.player.coords[1] in range(1, MAP_Y):
                    wrl.player.falling = False
                    fall_delay = 0
                    wrl.player.coords[1] -= 1
                    if wrl.player.coords[1] > 0:
                        xs += 32
                    if not wrl.level[wrl.player.coords[1]][wrl.player.coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT]:
                        wrl.player.coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = wrl.player.coords[1], wrl.player.coords[0]
                        wrl.destroy_block(bx, by)
                            #D KEY - RIGHT
                elif event.key == K_d and wrl.player.coords[1] in range(0, MAP_Y - 1):
                    wrl.player.falling = False
                    fall_delay = 0
                    wrl.player.coords[1] += 1
                    if wrl.player.coords[1] > 24:
                        xs = (-32*(wrl.player.coords[1] - 24))
                    if not wrl.level[wrl.player.coords[1]][wrl.player.coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT]:
                        wrl.player.coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = wrl.player.coords[1], wrl.player.coords[0]
                        wrl.destroy_block(bx, by)
                            #Z KEY - PLACE BLOCK
                elif event.key == K_z:
                    # print "Debug: placing block at %d %d, previous was %d" % (px, py, wrl.level[px][py])
                    if (wrl.player.inventory[wrl.player.current_block] > 0 or wrl.player.god_mode) and block_under == block.BLOCK_AIR:
                        wrl.level[px][py] = block.BLOCK_INVENTORY[wrl.player.current_block]
                        if not wrl.player.god_mode:
                            wrl.player.inventory[wrl.player.current_block] -= 1
                            #X KEY - DESTROY BLOCK STANDING ON
                elif event.key == K_x:
                    if wrl.level[px][py] in block.BLOCK_INVENTORY:
                        if block_under in block.BLOCK_INVENTORY:
                            block_index = block.BLOCK_INVENTORY.index(block_under)
                            wrl.player.inventory[block_index] += 1
                            wrl.level[px][py] = block.BLOCK_AIR
                            #1 KEY - SCROLL INVENTORY
                elif event.key == K_1:
                    wrl.player.current_block = (wrl.player.current_block + 1) % len(block.BLOCK_INVENTORY)
                            #ESC KEY - RESET
                elif event.key == K_ESCAPE:
                    wrl.new_world(MAP_X, MAP_Y)
                            #F1 KEY - GODMODE
                elif event.key == K_F1:
                    wrl.player.god_mode = not wrl.player.god_mode
                            #E KEY - EXPLODE
                elif event.key == K_e and wrl.player.god_mode:
                    wrl.explode(px, py, 5, False)
                            #N KEY - DESPAWN ENTITY
                elif event.key == K_n and wrl.player.god_mode:
                    if len(wrl.entities) > 1:
                        wrl.remove_entity(len(wrl.entities) - 1)  # last
                            #M KEY - SPAWN ENTITY
                elif event.key == K_m and wrl.player.god_mode:
                    wrl.spawn_entity(PlayerEntity(bounding_box=(0, 0, MAP_X, MAP_Y)))
                            #F5 KEY - SCREENSHOT (possibly bugged)
                elif event.key == K_F5:
                    import datetime
                    filename = "2dexp-%s.png" % str(datetime.datetime.now()).replace(":", "-")
                    # Dirty fix of bug where pygame says that it can't open png for reading
                    f = open(filename, "w")  # Create the file
                    f.close()
                    pygame.image.save(DISPLAY, filename)
                    print "Saved screenshot"
        for x in range(MAP_X):
            for y in range(MAP_Y):
                displae.blit(block.BLOCK_TEXTURES[wrl.level[x][y]], (x*32, y*32))
                # gravity
                # newHeight = 0
                # while wrl.level[wrl.player.coords[0]][newHeight] == block.BLOCK_AIR:
                # newHeight += 1
                #wrl.player.coords[0] = newHeight - 1
        debug_text = "Coords: %d, %d   %d fps, block: " % (wrl.player.coords[0], wrl.player.coords[1], clk.get_fps()) + "**%d, %d**" % (xs, ys)
        inventory_text = (" x %d" % wrl.player.inventory.get(wrl.player.current_block, -1)) + " " + block.BLOCK_NAMES.get(block.BLOCK_INVENTORY[wrl.player.current_block], "unknown")
        debug_label = font.render(debug_text, True, COLORS['white'], COLORS['black'])
        inventory_label = font.render(inventory_text, True, COLORS['white'], COLORS['black'])
        DISPLAY.blit(debug_label, (0, 0))
        DISPLAY.blit(block.BLOCK_TEXTURES[block.BLOCK_INVENTORY[wrl.player.current_block]], (0, 25 * TILESIZE + 5))
        DISPLAY.blit(inventory_label, (32, MAP_Y * TILESIZE + 5))
        if block_under in block.BLOCK_DEADLY and not wrl.player.god_mode:
            game_over()
        for ent in wrl.entities:
            ent.render(displae, TILESIZE, TILESIZE)
        pygame.display.update()
        DISPLAY.blit(displae, (xs, ys))
        DISPLAY.fill(0, (0, 25 * TILESIZE, 25 * TILESIZE, 37))
        DISPLAY.blit(block.BLOCK_TEXTURES[block.BLOCK_INVENTORY[wrl.player.current_block]], (0, 25 * TILESIZE + 5))
        DISPLAY.blit(inventory_label, (32, 25 * TILESIZE + 5))

pygame.init()
DISPLAY = pygame.display.set_mode((800, 800))
displae = pygame.Surface((MAP_X * 32, MAP_Y * 32))
pygame.display.set_caption("2DExplore")

wrl = world.World()
if os.path.isfile(SAVE_FILE):
    load(SAVE_FILE)
else:
    wrl.new_world(MAP_X, MAP_Y)

main_loop()
