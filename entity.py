__author__ = 'mark'

"""
    Abstract class, defining entity.
"""


class Entity(object):
    def __init__(self, texture=None, bounding_box=None):
        pass

    def render(self, surface, tile_x, tile_y):
        pass

    def move(self, coords):
        pass

    def tick(self):
        pass

    def removed_hook(self):
        pass

    def spawn_hook(self):
        pass

    def _test_bounding_box(self, x, y):
        pass

"""
    Generic Entity, anything that is a real entity.
"""


class GenericEntity(Entity):
    def __init__(self, texture=None, bounding_box=None):
        self.texture = texture
        self.coords = None
        self.alive = False
        self.bounding_box = bounding_box
        Entity.__init__(self, texture, bounding_box)

    def removed_hook(self):
        self.alive = False

    def spawn_hook(self):
        self.alive = True
        self.coords = [0, 0]

    def move(self, coords):
        self.coords = coords

    def _test_bounding_box(self, x, y):
        if not self.bounding_box:
            return True
        if x in xrange(self.bounding_box[0], self.bounding_box[2]):
            if y in xrange(self.bounding_box[1], self.bounding_box[3]):
                return True
        return False


