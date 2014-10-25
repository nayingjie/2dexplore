from player_entity import PlayerEntity
# TODO: make a better random with probability
__author__ = 'mark'
import pygame
import sys
import os
from pygame.locals import *
import world
import block


TILESIZE = 32
MAP_X = 20
MAP_Y = 20

god_mode = False
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'grey': (127, 127, 127)
}






def game_over():
    gameover_font = pygame.font.SysFont("FreeSansBold", 38)
    gameover_label = gameover_font.render("GAME OVER :(, Press [SpaceBar]", True, COLORS['red'], COLORS['black'])
    DISPLAY.blit(gameover_label, (int(TILESIZE * MAP_X / 4), int(TILESIZE * MAP_Y / 2)))
    pygame.display.update()
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    game_world.new_world(MAP_X, MAP_Y)
                    return
            elif evt.type == QUIT:
                game_world.save("explore_save.gz")
                pygame.quit()
                sys.exit()


def main_loop():
    global DISPLAY, start_time, falling, fall_delay, god_mode,\
        block_above, block_under, block_index, game_world
    font = pygame.font.SysFont("FreeSansBold", 18)  # Fonts should be inited after pygame.init()
    start_time = 0
    clk = pygame.time.Clock()
    while True:
        clk.tick(20)
        if pygame.time.get_ticks() - start_time >= 50:
            game_world.tick()
        start_time = pygame.time.get_ticks()
        px = game_world.entities[0].coords[1]
        py = game_world.entities[0].coords[0]
        block_under = game_world.level[px][py]
        block_above = game_world.level[px][py - 1] if py < 0 else -1
        prev_pos = game_world.entities[0].coords[:]  # lists are mutable
        for event in pygame.event.get():
            if event.type == QUIT:
                game_world.save("explore_save.gz")
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == K_w and game_world.entities[0].coords[0] in range(1, MAP_X) and (not falling or god_mode):
                    game_world.entities[0].coords[0] -= 1
                    if not game_world.level[game_world.entities[0].coords[1]][game_world.entities[0].coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT] and\
                            not god_mode:
                        game_world.entities[0].coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = game_world.entities[0].coords[1], game_world.entities[0].coords[0]
                        game_world.destroy_block(bx, by)
                elif event.key == K_s and game_world.entities[0].coords[0] in range(0, MAP_X - 1):
                    game_world.entities[0].coords[0] += 1
                    if not game_world.level[game_world.entities[0].coords[1]][game_world.entities[0].coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT]:
                        game_world.entities[0].coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = game_world.entities[0].coords[1], game_world.entities[0].coords[0]
                        game_world.destroy_block(bx, by)
                elif event.key == K_a and game_world.entities[0].coords[1] in range(1, MAP_Y):
                    falling = False
                    fall_delay = 0
                    game_world.entities[0].coords[1] -= 1
                    if not game_world.level[game_world.entities[0].coords[1]][game_world.entities[0].coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT]:
                        game_world.entities[0].coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = game_world.entities[0].coords[1], game_world.entities[0].coords[0]
                        game_world.destroy_block(bx, by)
                elif event.key == K_d and game_world.entities[0].coords[1] in range(0, MAP_Y - 1):
                    falling = False
                    fall_delay = 0
                    game_world.entities[0].coords[1] += 1
                    if not game_world.level[game_world.entities[0].coords[1]][game_world.entities[0].coords[0]] in block.BLOCK_NONSOLID and not keys[K_LSHIFT]:
                        game_world.entities[0].coords = prev_pos
                    if keys[K_LSHIFT]:
                        bx, by = game_world.entities[0].coords[1], game_world.entities[0].coords[0]
                        game_world.destroy_block(bx, by)
                elif event.key == K_z:
                    # print "Debug: placing block at %d %d, previous was %d" % (px, py, game_world.level[px][py])
                    if (game_world.entities[0].inventory[game_world.entities[0].current_block] > 0 or god_mode) and block_under == block.BLOCK_AIR:
                        game_world.level[px][py] = block.BLOCK_INVENTORY[game_world.entities[0].current_block]
                        if not god_mode:
                            game_world.entities[0].inventory[game_world.entities[0].current_block] -= 1
                elif event.key == K_x:
                    if game_world.level[px][py] in block.BLOCK_INVENTORY:
                        if block_under in block.BLOCK_INVENTORY:
                            block_index = block.BLOCK_INVENTORY.index(block_under)
                            game_world.entities[0].inventory[block_index] += 1
                            game_world.level[px][py] = block.BLOCK_AIR
                elif event.key == K_1:
                    game_world.entities[0].current_block = (game_world.entities[0].current_block + 1) % len(block.BLOCK_INVENTORY)
                elif event.key == K_ESCAPE:
                    game_world.new_world(MAP_X, MAP_Y)
                elif event.key == K_F1:
                    god_mode = not god_mode
                elif event.key == K_e and god_mode:
                    game_world.explode(px, py, 5, True)
                elif event.key == K_n and god_mode:
                    if len(game_world.entities) > 1:
                        game_world.remove_entity(len(game_world.entities) - 1)  # last
                elif event.key == K_m and god_mode:
                    game_world.spawn_entity(PlayerEntity(bounding_box=(0, 0, MAP_X, MAP_Y)))
                elif event.key == K_F5:
                    import datetime

                    pygame.image.save(DISPLAY, "2dexp-%s.png" % str(datetime.datetime.now()))
                    print "Saved screenshot"
        for x in range(MAP_X):
            for y in range(MAP_Y):
                DISPLAY.blit(block.BLOCK_TEXTURES[game_world.level[x][y]], (x * TILESIZE, y * TILESIZE))
                # gravity
                # newHeight = 0
                # while game_world.level[game_world.entities[0].coords[0]][newHeight] == block.BLOCK_AIR:
                # newHeight += 1
                #game_world.entities[0].coords[0] = newHeight - 1
        debug_text = "Coords: %d, %d   %d fps, block: " % (game_world.entities[0].coords[0], game_world.entities[0].coords[1], clk.get_fps()) + \
                     block.BLOCK_NAMES[block_under] + (" Entities: %d " % len(game_world.entities)) + \
                     (" GOD MODE" if god_mode else "")
        inventory_text = (" x %d" % game_world.entities[0].inventory.get(game_world.entities[0].current_block, -1)) + " " + block.BLOCK_NAMES.get(block.BLOCK_INVENTORY[game_world.entities[0].current_block], "unknown")
        debug_label = font.render(debug_text, True, COLORS['white'], COLORS['black'])
        inventory_label = font.render(inventory_text, True, COLORS['white'], COLORS['black'])
        DISPLAY.blit(debug_label, (0, 0))
        DISPLAY.fill(0, (0, MAP_X * TILESIZE, MAP_Y * TILESIZE, 37))
        DISPLAY.blit(block.BLOCK_TEXTURES[block.BLOCK_INVENTORY[game_world.entities[0].current_block]], (0, MAP_Y * TILESIZE + 5))
        DISPLAY.blit(inventory_label, (32, MAP_Y * TILESIZE + 5))
        if block_under in block.BLOCK_DEADLY and not god_mode:
            game_over()
        for ent in game_world.entities:
            ent.render(DISPLAY, TILESIZE, TILESIZE)
        pygame.display.update()


pygame.init()
DISPLAY = pygame.display.set_mode((TILESIZE * MAP_X, TILESIZE * MAP_Y + 37))
pygame.display.set_caption("2DExplore")

game_world = world.World()
if os.path.isfile("explore_save.gz"):
    game_world.load("explore_save.gz")
else:
    game_world.new_world(MAP_X, MAP_Y)

main_loop()