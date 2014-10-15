__author__ = 'mark'
import pygame.image


class Entity(object):
    def __init__(self, texture=None, bounding_box=None):
        self.texture = texture
        self.coords = None
        self.alive = False
        self.bounding_box = bounding_box

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

    def _test_bounding_box(self, x, y):
        if not self.bounding_box:
            return True
        if x in xrange(self.bounding_box[0], self.bounding_box[2]):
            if y in xrange(self.bounding_box[1], self.bounding_box[3]):
                return True
        return False

class GenericEntity(Entity):
    def __init__(self, texture=None, bounding_box=None):
        Entity.__init__(self, texture, bounding_box)


class PlayerEntity(GenericEntity):
    def __init__(self, texture=None, bounding_box=None):
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
        import random
        x, y = random.randint(0, 19), random.randint(0, 19)
        if self._test_bounding_box(x, y):
            self.coords[0:2] = [x, y]

