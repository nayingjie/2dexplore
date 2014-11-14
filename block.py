__author__ = 'mark'
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
BLOCK_MAX = 8
BLOCK_NAMES = {
    BLOCK_AIR: 'Air', BLOCK_STONE: 'Stone', BLOCK_DIRT: 'Dirt', BLOCK_GRASS: 'Grass',
    BLOCK_DIAMOND: 'Diamond Ore', BLOCK_LAVA: 'Lava', BLOCK_WATER: 'Water',
    BLOCK_LAVA_FLOWING: 'Lava F', BLOCK_WATER_FLOWING: 'Water F'
}
BLOCK_TEXTURES = None
BLOCK_NONSOLID = [BLOCK_AIR, BLOCK_LAVA, BLOCK_WATER, BLOCK_WATER_FLOWING, BLOCK_LAVA_FLOWING]
BLOCK_DEADLY = [BLOCK_LAVA, BLOCK_LAVA_FLOWING]
BLOCK_INVENTORY = [BLOCK_STONE, BLOCK_DIRT, BLOCK_GRASS, BLOCK_DIAMOND,
                   BLOCK_LAVA, BLOCK_WATER]


def load_textures(append_path=""):
    global BLOCK_TEXTURES
    BLOCK_TEXTURES = {
        BLOCK_STONE: pygame.image.load(append_path + 'textures/stone.png'),
        BLOCK_AIR: pygame.image.load(append_path + 'textures/air.png'),
        BLOCK_DIRT: pygame.image.load(append_path + 'textures/dirt.png'),
        BLOCK_GRASS: pygame.image.load(append_path + 'textures/grass.png'),
        BLOCK_DIAMOND: pygame.image.load(append_path + 'textures/diamond_ore.png'),
        BLOCK_LAVA: pygame.image.load(append_path + 'textures/lava.png'),
        BLOCK_WATER: pygame.image.load(append_path + 'textures/water.png'),
        BLOCK_LAVA_FLOWING: pygame.image.load(append_path + 'textures/lava.png'),
        BLOCK_WATER_FLOWING: pygame.image.load(append_path + 'textures/water.png'),
    }