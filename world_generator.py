__author__ = 'mark'
# TODO: make a better random with probability
import random

import block

class WorldGenerator(object):
    size = None

    def __init__(self, size):
        self.size = size



    def generate_world(self):
        x_size, y_size = self.size
        world = [[0 for x in xrange(x_size)] for y in xrange(y_size)]

        height_air = xrange(0, int(x_size / 8) + 4)
        height_stone = xrange(int(x_size / 8) + 5, x_size)
        for x2 in xrange(x_size):
            for y2 in xrange(y_size):
                if not y2 in height_air:
                    if y2 == y_size - 1:
                        world[x2][y2] = block.BLOCK_BEDROCK
                    elif y2 in height_stone:
                        if random.randint(0, 5) == 5:
                         world[x2][y2] = block.BLOCK_DIRT
                        elif random.randint(0, 150) == 50:
                            world[x2][y2] = block.BLOCK_DIAMOND
                        elif random.randint(0, 285) == 285:
                            world[x2][y2] = block.BLOCK_LAVA_FLOWING
                        else:
                            world[x2][y2] = block.BLOCK_STONE

                    else:
                        if random.randint(0, 5) == 5:
                            world[x2][y2] = block.BLOCK_WATER_FLOWING
                        else:
                            world[x2][y2] = block.BLOCK_GRASS
            if x2 % 6  == 0 and random.randint(0, 1):
                for trunk_y in xrange(5, height_air[-1] + 1):
                    world[x2][trunk_y] = block.BLOCK_LOG

                world[x2][4] = block.BLOCK_LEAVES
                world[x2][5] = block.BLOCK_LEAVES
                world[x2 - 1][5] = block.BLOCK_LEAVES
                world[x2 + 1][5] = block.BLOCK_LEAVES
                world[x2 - 1][6] = block.BLOCK_LEAVES
                world[x2 + 1][6] = block.BLOCK_LEAVES
                world[x2 - 1][7] = block.BLOCK_LEAVES
                world[x2 + 1][7] = block.BLOCK_LEAVES
                world[x2 - 2][7] = block.BLOCK_LEAVES
                world[x2 + 2][7] = block.BLOCK_LEAVES

        return world
