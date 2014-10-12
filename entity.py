__author__ = 'mark'
import pygame.image


class Entity(object):
    def __init__(self, texture=None):
        self.texture = texture
        self.coords = None
        self.alive = False

    def render(self, surface, tile_x, tile_y):
        pass

    def move(self, coords):
        self.coords = coords

    def tick(self):
        pass

    def removed_hook(self):
        self.alive = False
        pass

    def spawn_hook(self):
        self.alive = True
        self.coords = [0, 0]
        pass


class GenericEntity(Entity):
    def __init__(self, texture=None):
        Entity.__init__(self, texture)


class PlayerEntity(GenericEntity):
    def __init__(self, texture=None):
        GenericEntity.__init__(self, pygame.image.load('textures/player.png') if not texture else texture)

    def render(self, surface, tile_x, tile_y):
        if self.alive:
            surface.blit(self.texture, (self.coords[1] * tile_x, self.coords[0] * tile_y))

    def removed_hook(self):
        GenericEntity.removed_hook(self)

    def spawn_hook(self):
        GenericEntity.spawn_hook(self)

    def tick(self):
        if self.coords[0] < 12:
            self.coords[0] += 1
        else:
            self.coords[0] = 0

