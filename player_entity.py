import pygame
from entity import GenericEntity
from PIL import Image

__author__ = 'mark'
player=Image.open('textures/player.png')

class PlayerEntity(GenericEntity):
    def __init__(self, texture=None, bounding_box=None):
        self.falling, self.fall_delay, self.god_mode = False, 0, False
        self.inventory = {}
        self.current_block = 0
        GenericEntity.__init__(self, player.tobytes() if not texture else texture,
                               bounding_box)

    def render(self, surface, tile_x, tile_y):
        if self.alive:
            surface.blit(pygame.image.fromstring(self.texture, (32,32), "RGBA"), (self.coords[1] * tile_x, self.coords[0] * tile_y))

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
