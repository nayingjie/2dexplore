__author__ = 'mark'
from PIL import Image
import pygame.image
"""
    Defines constants for in-game blocks (name, texture, ID, etc)
"""
BLOCK_AIR = 0
BLOCK_STONE = 1
BLOCK_DIRT = 2
BLOCK_GRASS = 3
BLOCK_DIAMOND = 4
BLOCK_LAVA = 5
BLOCK_WATER = 6
BLOCK_LAVA_FLOWING = 7
BLOCK_WATER_FLOWING = 8

BLOCK_COUNT = 9

BLOCK_NAMES = {
    BLOCK_AIR: 'Air', BLOCK_STONE: 'Stone', BLOCK_DIRT: 'Dirt', BLOCK_GRASS: 'Grass',
    BLOCK_DIAMOND: 'Diamond Ore', BLOCK_LAVA: 'Stat Lava', BLOCK_WATER: 'Stat Water',
    BLOCK_LAVA_FLOWING: 'Lava', BLOCK_WATER_FLOWING: 'Water'
}
BLOCK_TEXTURES = None
BLOCK_NONSOLID = [BLOCK_AIR, BLOCK_LAVA, BLOCK_WATER, BLOCK_WATER_FLOWING, BLOCK_LAVA_FLOWING]
BLOCK_DEADLY = [BLOCK_LAVA, BLOCK_LAVA_FLOWING]
BLOCK_INVENTORY = [BLOCK_STONE, BLOCK_DIRT, BLOCK_GRASS, BLOCK_DIAMOND,
                   BLOCK_LAVA_FLOWING, BLOCK_WATER_FLOWING]


def load_textures(append_path=""):
    global BLOCK_TEXTURES
    stone = Image.open("textures/stone.png")
    air = Image.open("textures/air.png")
    dirt = Image.open("textures/dirt.png")
    grass = Image.open("textures/grass.png")
    diamond_ore = Image.open("textures/diamond_ore.png")
    lava = Image.open("textures/lava.png")
    water = Image.open("textures/water.png")
    print len(stone.tobytes())
    print stone
    BLOCK_TEXTURES = {
        BLOCK_STONE: pygame.image.fromstring(stone.tobytes(),(32,32),"RGBA"),
        BLOCK_AIR: pygame.image.fromstring(air.tobytes(),(32,32),"RGBA"),
        BLOCK_DIRT: pygame.image.fromstring(dirt.tobytes(),(32,32),"RGB"),
        BLOCK_GRASS: pygame.image.fromstring(grass.tobytes(),(32,32),"RGB"),
        BLOCK_DIAMOND: pygame.image.fromstring(diamond_ore.tobytes(),(32,32),"RGB"),
        BLOCK_LAVA: pygame.image.fromstring(lava.tobytes(),(32,32),"RGB"),
        BLOCK_WATER: pygame.image.fromstring(water.tobytes(),(32,32),"RGBA"),
        BLOCK_LAVA_FLOWING: pygame.image.fromstring(lava.tobytes(),(32,32),"RGB"),
        BLOCK_WATER_FLOWING: pygame.image.fromstring(water.tobytes(),(32,32),"RGBA"),
    }
