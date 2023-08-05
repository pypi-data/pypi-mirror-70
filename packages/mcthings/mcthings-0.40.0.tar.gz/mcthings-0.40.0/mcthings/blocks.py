# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0
# Author (©): Alvaro del Castillo

from mcpi.vec3 import Vec3

from .thing import Thing
from .world import World


class Blocks(Thing):
    width = 3  # x
    height = 2  # y
    length = 4  # z

    def build(self):
        p = self.position
        World.server.setBlocks(p.x, p.y, p.z,
                               p.x + self.width - 1, p.y + self.height - 1, p.z + self.length - 1,
                               self.block)

        self._end_position = Vec3(p.x + self.width - 1, p.y + self.height - 1, p.z + self.length - 1)
