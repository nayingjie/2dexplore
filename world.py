__author__ = 'mark'

import world_generator, block, player_entity


class World(object):
    def __init__(self):
        self.level = None
        self.entities = None
        self.inventory = None

    def save(self, file_name):
        import cPickle
        import gzip

        entities_save = [cPickle.dumps(ent) for ent in self.entities]
        save_file = None

        try:
            try:
                save_file = gzip.open(file_name, "wb")
            except IOError as err:
                print "Can not open file: \n %s" % err.message
            cPickle.dump({'world': self.level, 'entities': entities_save}, save_file,
                         cPickle.HIGHEST_PROTOCOL)
        except cPickle.PicklingError as err:
            print "Error pickling: \n %s" % err.message
        finally:
            save_file.close()

    def load(self, file_name):
        import cPickle
        import gzip

        try:
            save_file = gzip.open(file_name, "rb")
            try:
                data = cPickle.load(save_file)
                try:
                    self.level = data['world']
                    self.entities = [cPickle.loads(pickled_ent) for pickled_ent in data['entities']]
                except ValueError as err:
                    print "Error parsing world data: \n %s" % err.message
            except cPickle.UnpicklingError as err:
                print "Error unpickling: \n %s" % err.message
        except IOError as ex:
            print "Unable to open save file: \n %s" % ex.message

    def get_entities(self):
        return self.entities

    def set_entities(self, entities):
        self.entities = entities

    def new_world(self, x_size, y_size):
        self.level = world_generator.generate_world(x_size, y_size)
        self.entities = [player_entity.PlayerEntity()]
        self.entities[0].spawn_hook()
        self.entities[0].inventory = {x: 0 for x in xrange(block.BLOCK_MAX)}

    def tick(self):
        level_x, level_y = self.get_level_size()
        for en in self.entities:
            en.tick()
        if self.entities[0].god_mode:
            self.entities[0].falling = False
        if self.entities[0].falling:
            self.entities[0].fall_delay += 1

        checky = self.entities[0].coords[0] + 1
        if checky <= level_y - 1 and self.level[self.entities[0].coords[1]][checky] in block.BLOCK_NONSOLID:
            self.entities[0].falling = True
        if self.entities[0].fall_delay == 3:
            self.entities[0].coords[0] += 1
            self.entities[0].fall_delay = 0
            self.entities[0].falling = False

        for x2 in range(level_x):
            for y2 in range(level_y):
                if self.level[x2][y2] == block.BLOCK_LAVA_FLOWING:
                    if 0 < x2 < level_x - 1:
                        if self.level[x2 - 1][y2] == block.BLOCK_AIR:
                            self.level[x2 - 1][y2] = block.BLOCK_LAVA
                            break
                        elif self.level[x2 + 1][y2] == block.BLOCK_AIR:
                            self.level[x2 + 1][y2] = block.BLOCK_LAVA
                            break
                        elif 0 < y2 < level_y - 1 and self.level[x2][y2 + 1] == block.BLOCK_AIR:
                            self.level[x2][y2 + 1] = block.BLOCK_LAVA_FLOWING
                            break
                elif self.level[x2][y2] == block.BLOCK_WATER_FLOWING:
                    if 0 < x2 < level_x - 1:
                        if self.level[x2 - 1][y2] == block.BLOCK_AIR:
                            self.level[x2 - 1][y2] = block.BLOCK_WATER
                            break
                        elif self.level[x2 + 1][y2] == block.BLOCK_AIR:
                            self.level[x2 + 1][y2] = block.BLOCK_WATER
                            break
                        elif 0 < y2 < level_y - 1 and self.level[x2][y2 + 1] == block.BLOCK_AIR:
                            self.level[x2][y2 + 1] = block.BLOCK_WATER_FLOWING
                            break

    def destroy_block(self, blk_x, blk_y, add_inventory=True):
        blk = self.level[blk_x][blk_y]
        if not blk in block.BLOCK_INVENTORY:
            return
        self.level[blk_x][blk_y] = block.BLOCK_AIR
        if add_inventory:
            self.entities[0].inventory[block.BLOCK_INVENTORY.index(blk)] += 1

    def explode(self, exp_x, exp_y, exp_radius, add_inventory=False):
        import random

        for ex in range(exp_x - exp_radius, exp_x + exp_radius):
            for ey in range(exp_y - exp_radius, exp_y + exp_radius):
                if self.check_pos(ex, ey):
                    if (ey - exp_radius) > (exp_radius / 2):
                        if random.randint(0, 8) < 8:
                            self.destroy_block(ex, ey, add_inventory)
                else:
                    self.destroy_block(ex, ey, add_inventory)


    def check_pos(self, pos_x, pos_y):
        levelx, levely = self.get_level_size()
        if 0 <= pos_x <= levelx - 1:
            if 0 <= pos_y <= levely - 1:
                # print "[DBG] check_pos(%d, %d) == True" % (pos_x, pos_y)
                return True
        # print "[DBG] check_pos(%d, %d) == False" % (pos_x, pos_y)
        return False


    def spawn_entity(self, ent):
        ent.spawn_hook()
        self.entities.append(ent)
        return self.entities.index(ent)


    def remove_entity(self, ent_id):
        self.entities[ent_id].removed_hook()
        self.entities.remove(self.entities[ent_id])

    def get_level_size(self):
        if not self.level:
            raise ValueError("Cannot get size of uninitialized level")
        return len(self.level), len(self.level[0])
        

