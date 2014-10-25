import pygame
from entity import GenericEntity

__author__ = 'mark'


class PlayerEntity(GenericEntity):
    def __init__(self, texture=None, bounding_box=None):
        self.falling, self.fall_delay = False, 0
        self.inventory = {}
        self.current_block = 0
        GenericEntity.__init__(self, 'textures/player.png' if not texture else texture,
                               bounding_box)

    def render(self, surface, tile_x, tile_y):
        if self.alive:
            surface.blit(pygame.image.load(self.texture), (self.coords[1] * tile_x, self.coords[0] * tile_y))

    def removed_hook(self):
        GenericEntity.removed_hook(self)

    def spawn_hook(self):
        GenericEntity.spawn_hook(self)

    def tick(self):
        pass

    def set_inventory(self, inventory):
        self.inventory = inventory

    def get_inventory(self):
        return self.inventory