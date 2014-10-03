__author__ = 'mark'
import block, random


def generate_world(xsize=64, ysize=64):
    world = [[0 for x in range(xsize)] for y in range(ysize)]
    height_air = range(0, int(xsize / 8) + 4)
    height_stone = range(int(xsize / 8) + 5, xsize)
    for x2 in range(xsize):
        for y2 in range(ysize):
            if y2 in height_air:
                world[x2][y2] = block.BLOCK_AIR
            else:
                if y2 in height_stone:
                    if random.randint(0, 5) == 5:
                        world[x2][y2] = block.BLOCK_DIRT
                    else:
                        world[x2][y2] = block.BLOCK_STONE
                elif y2 in height_air:
                    world[x2][y2] = block.BLOCK_AIR
                else:
                    world[x2][y2] = block.BLOCK_GRASS

    return world