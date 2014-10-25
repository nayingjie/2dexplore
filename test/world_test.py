__author__ = 'mark'
import world
import entity

wrl = world.World()
wrl.new_world(64, 64)
wrl.spawn_entity(entity.GenericEntity())
wrl.tick()

