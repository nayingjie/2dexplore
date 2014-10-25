__author__ = 'mark'
# TODO: make a better random with probability
import random

import block


def generate_world(x_size=64, y_size=64):
    # noinspection PyUnusedLocal
    world = [[0 for x in xrange(x_size)] for y in xrange(y_size)]
    height_air = xrange(0, int(x_size / 8) + 4)
    height_stone = xrange(int(x_size / 8) + 5, x_size)
    for x2 in xrange(x_size):
        for y2 in xrange(y_size):
            if y2 in height_air:
                world[x2][y2] = block.BLOCK_AIR
            else:
                if y2 in height_stone:
                    if random.randint(0, 5) == 5:
                        world[x2][y2] = block.BLOCK_DIRT
                    elif random.randint(0, 150) == 50:
                        world[x2][y2] = block.BLOCK_DIAMOND
                    elif random.randint(0, 285) == 285:
                        world[x2][y2] = block.BLOCK_LAVA_FLOWING
                    else:
                        world[x2][y2] = block.BLOCK_STONE
                elif y2 in height_air:
                    world[x2][y2] = block.BLOCK_AIR
                else:
                    if random.randint(0, 5) == 5:
                        world[x2][y2] = block.BLOCK_WATER_FLOWING
                    else:
                        world[x2][y2] = block.BLOCK_GRASS


    return world