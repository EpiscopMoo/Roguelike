from enum import Enum
from random import random

from engine.guiengine import RED_BLK, BLK_WHT, WHT_BLK
from globals import Messages, Message
from logic.attacks import MeleeAttack
from logic.loot import Loot
from logic.path_finding import dist, validate_visual_range
from logic.resources import ACTORS


class Behaviour(Enum):
    FOLLOWING = -2  # friendly units who follow the player and offer aid in combat
    FRIENDLY = -1  # friendly units who mind their own business, but offer aid in combat if they see the opportunity
    NEUTRAL = 0  # unit that does nothing at all
    PASSIVE = 1  # unit that moves randomly and does nothing more
    PASSIVE_AGGRESSIVE = 2  # unit that moves randomly and attacks nearby enemies, never chasing anybody
    AGGRESSIVE = 3  # units who always chase player down
    BERSERK = 4  # berserks attack anything within range. If all targets are too far, they look for the nearest one and chase it down


class Actor:
    def __init__(self, container, cells):
        self.x = 0
        self.y = 0
        self.hp = 10
        self.mp = 10
        self.maxhp = self.hp
        self.maxmp = self.mp
        self.base_damage = 1
        self.base_range = 1
        self.exp = 0
        self.container = container
        self.cells = cells
        self.pic = None
        self.type = 'npc'
        self.buffs = []
        self.static_drop = []
        self.name = None
        self.description = None
        self.color = WHT_BLK

    def current_cell(self):
        return self.cells[self.y][self.x]

    def neigh8(self):
        cells = self.cells
        y = self.y
        x = self.x
        neighs = [
            cells[y - 1][x - 1], cells[y - 1][x], cells[y - 1][x + 1],
            cells[y][x - 1], cells[y][x + 1],
            cells[y + 1][x - 1], cells[y + 1][x], cells[y + 1][x + 1]
        ]
        return neighs

    def left(self):
        current_cell = self.current_cell()
        target_cell = self.cells[self.y][self.x - 1]
        if target_cell.walkable() is False or self.x == 0:
            return False
        self.x -= 1
        current_cell.entity = None
        target_cell.entity = self
        return True

    def right(self):
        current_cell = self.current_cell()
        target_cell = self.cells[self.y][self.x + 1]
        if target_cell.walkable() is False or self.x == len(self.cells[0]) - 1:
            return False
        self.x += 1
        current_cell.entity = None
        target_cell.entity = self
        return True

    def up(self):
        current_cell = self.current_cell()
        target_cell = self.cells[self.y - 1][self.x]
        if target_cell.walkable() is False or self.y == 0:
            return False
        self.y -= 1
        current_cell.entity = None
        target_cell.entity = self
        return True

    def down(self):
        current_cell = self.current_cell()
        target_cell = self.cells[self.y + 1][self.x]
        if target_cell.walkable() is False or self.y == len(self.cells) - 2:
            return False
        self.y += 1
        current_cell.entity = None
        target_cell.entity = self
        return True

    def wait(self):
        return True

    def random_move(self):
        r = random()
        if r < 0.2:
            return self.wait()
        r = random()
        if r < 0.25:
            return self.left()
        if r < 0.5:
            return self.right()
        if r < 0.75:
            return self.up()
        return self.down()

    def can_attack(self, target_cell):
        if target_cell.entity is not None and target_cell.entity != self:
            dx = abs(target_cell.entity.x - self.x)
            dy = abs(target_cell.entity.y - self.y)
            if validate_visual_range(self.cells, (self.y, self.x), (target_cell.y, target_cell.x),
                                     self.get_self_range()):
                return True
        return False

    def attack(self, target_cell):
        if self.can_attack(target_cell):
            target = target_cell.entity
            attack = MeleeAttack({'damage': self.get_self_damage(), 'attacker': self})
            target.hit_it(attack)
            return True
        return False

    def make_move(self):
        pass

    def kill_it(self, attacker):
        self.container.remove(self)
        if self.current_cell().loot is None:
            self.current_cell().loot = Loot(self.static_drop) if len(self.static_drop) > 0 else None
        else:
            self.current_cell().loot.extend(self.static_drop)
        self.current_cell().entity = None
        Messages.add_info_message(Message("%s умирает." % self.name, RED_BLK))

    def apply_buffs(self):
        for buff in self.buffs:
            buff.apply(self)
        self.buffs = [buff for buff in self.buffs if buff.duration > 0]

    def add_buffs(self, buffs):
        self.buffs.extend(buffs)
        for buff in buffs:
            buff.apply_message()

    def get_self_damage(self):
        return self.base_damage

    def get_self_range(self):
        return self.base_range

    def add_static_drop(self, items):
        self.static_drop.extend(items)
