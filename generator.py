__author__ = 'mark'
import random

import block


def generate_world(x_size=64, y_size=64):
    # noinspection PyUnusedLocal
    world = [[0 for x in range(x_size)] for y in range(y_size)]
    height_air = range(0, int(x_size / 8) + 4)
    height_stone = range(int(x_size / 8) + 5, x_size)
    for x2 in range(x_size):
        for y2 in range(y_size):
            if y2 in height_air:
                world[x2][y2] = block.BLOCK_AIR
            else:
                if y2 in height_stone:
                    if random.randint(0, 5) == 5:
                        world[x2][y2] = block.BLOCK_DIRT
                    elif random.randint(0, 150) == 50:
                        world[x2][y2] = block.BLOCK_DIAMOND
                    elif random.randint(0, 285) == 285:
                        world[x2][y2] = block.BLOCK_LAVA
                    else:
                        world[x2][y2] = block.BLOCK_STONE
                elif y2 in height_air:
                    world[x2][y2] = block.BLOCK_AIR
                else:
                    if random.randint(0, 5) == 5:
                        world[x2][y2] = block.BLOCK_WATER
                    #elif random.randint(0, 50) == 50:
                    #    world[x2][y2] = block.BLOCK_LAVA
                    #    if 0 < x2 < x_size - 1:
                    #        world[x2-1][y2] = block.BLOCK_LAVA
                    #        world[x2+1][y2] = block.BLOCK_LAVA
                    else:
                     world[x2][y2] = block.BLOCK_GRASS


    return world