import curses

from engine.guiengine import BLK_WHT, WHT_BLK
from logic.resources import CELLS


class Cell:
    def __init__(self, skin, y, x):
        self.skin = skin
        self.y = y
        self.x = x
        if self.skin not in CELLS:
            self.skin = ' '
        self.stats = CELLS[self.skin]
        self.name = self.stats['name']
        self.description = self.stats['description']
        self.entity = None
        self.loot = None
        self.pic = self.stats['pic'] if 'pic' in self.stats else None

    def walkable(self, ignore_player=False):
        if ignore_player:
            return self.stats['walkable'] and (self.entity is None or self.entity.type == 'player')
        else:
            return self.stats['walkable'] and self.entity is None

    def get_skin(self):
        if self.entity is not None:
            return self.entity.skin
        elif self.loot is not None:
            return self.loot.skin
        else:
            return self.skin

    def get_name(self):
        if self.entity is not None:
            return self.entity.name
        elif self.loot is not None:
            return self.loot.name
        else:
            return self.name

    def get_description(self):
        if self.entity is not None:
            return self.entity.description
        elif self.loot is not None:
            return self.loot.description
        else:
            return self.description

    def get_pic(self):
        if self.entity is not None:
            if self.entity.pic is not None:
                return self.entity.pic
        return self.pic

    def draw(self, pad, y, x):
        pad.addstr(y, x, self.get_skin(), self.get_color())

    def get_color(self):
        if self.entity is not None:
            return curses.color_pair(self.entity.color)
        elif self.loot is not None:
            return curses.color_pair(self.loot.color)
        else:
            return curses.color_pair(WHT_BLK)