__author__ = 'mark'
import pygame.image
BLOCK_AIR = 0
BLOCK_STONE = 1
BLOCK_DIRT = 2
BLOCK_GRASS = 3
BLOCK_DIAMOND = 4
BLOCK_LAVA = 5
BLOCK_WATER = 6
BLOCK_LAVA_FLOWING = 7
BLOCK_WATER_FLOWING = 8
#BLOCK_GLASS = 9
BLOCK_NAMES = {BLOCK_AIR: 'Air', BLOCK_STONE: 'Stone', BLOCK_DIRT: 'Dirt', BLOCK_GRASS: 'Grass',
               BLOCK_DIAMOND: 'Diamond Ore', BLOCK_LAVA: 'Lava', BLOCK_WATER: 'Water',
               BLOCK_LAVA_FLOWING: 'Lava', BLOCK_WATER_FLOWING: 'Water', #BLOCK_GLASS: 'glass',
            }
non_solid = [BLOCK_AIR, BLOCK_LAVA, BLOCK_WATER, BLOCK_WATER_FLOWING, BLOCK_LAVA_FLOWING]
deadly = [BLOCK_LAVA, BLOCK_LAVA_FLOWING]
textures = {
    BLOCK_STONE: pygame.image.load('textures/stone.png'),
    BLOCK_AIR: pygame.image.load('textures/air.png'),
    BLOCK_DIRT: pygame.image.load('textures/dirt.png'),
    BLOCK_GRASS: pygame.image.load('textures/grass.png'),
    BLOCK_DIAMOND: pygame.image.load('textures/diamond_ore.png'),
    BLOCK_LAVA: pygame.image.load('textures/lava.png'),
    BLOCK_WATER: pygame.image.load('textures/water.png'),
    BLOCK_LAVA_FLOWING: pygame.image.load('textures/lava.png'),
    BLOCK_WATER_FLOWING: pygame.image.load('textures/water.png'),
}