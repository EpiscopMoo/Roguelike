from engine.guiengine import RED_BLK
from globals import Globals
from logic.actors.actor import *
from logic.items import *


class Class:
    def __init__(self):
        self.strength = 5
        self.dexterity = 5
        self.endurance = 5
        self.knowledge = 5
        self.charisma = 5
        self.spiritual = 5

    def class_name(self):
        return 'Class'

    def get_start_items(self):
        return []


class Soldier(Class):
    def __init__(self):
        super().__init__()
        self.strength = 10
        self.dexterity = 6
        self.endurance = 8
        self.charisma = 6

    def class_name(self):
        return 'Солдат Содружества'


class Engineer(Class):
    def __init__(self):
        super().__init__()
        self.knowledge = 10
        self.strength = 7
        self.endurance = 7
        self.charisma = 6

    def class_name(self):
        return 'Инженер Содружества'


class PsiClassA(Class):
    def __init__(self):
        super().__init__()
        self.strength = 8
        self.endurance = 10
        self.spiritual = 7

    def class_name(self):
        return 'Псионик А-класса'

    def get_start_items(self):
        return [
            Item(aeowe_sword),
            Item(hp_potion),
            Item(buckler),
            Item(stunner),
            Item(jackle_pistol)
        ]


class PsiClassB(Class):
    def __init__(self):
        super().__init__()
        self.dexterity = 8
        self.knowledge = 8
        self.spiritual = 9
        self.strength = 4
        self.charisma = 6

    def class_name(self):
        return 'Псионик Б-класса'


class Solest(Class):
    def __init__(self):
        super().__init__()
        self.strength = 3
        self.endurance = 4
        self.knowledge = 6
        self.charisma = 10
        self.spiritual = 12

    def class_name(self):
        return 'Солест'


class ClanTau(Class):
    def __init__(self):
        super().__init__()
        self.strength = 3
        self.endurance = 4
        self.knowledge = 6
        self.charisma = 10
        self.spiritual = 12

    def class_name(self):
        return 'Клан Тау'


class Hero(Actor):
    def __init__(self, clazz, container, cells):
        super().__init__(container, cells)
        Globals.player = self
        self.name = "Нил Порго"
        self.clazz = clazz
        self.hp = 10 + self.clazz.endurance - 5
        self.mp = 10 + self.clazz.spiritual - 5
        self.base_damage = max(0, 1 + self.clazz.strength - 5)
        self.maxhp = self.hp
        self.maxmp = self.mp
        self.class_name = self.clazz.class_name()
        self.skin = '@'
        self.type = 'player'
        self.inventory = None
        self.description = "Это Вы."
        self.pic = [
            '            |',
            '           j|',
            '     /=|  _jl',
            ' __/.="==.{/',
            '    -\T/-\'',
            '     /_\ ',
            '    // \\\\_',
            '   _I    /'
        ]

    def hit_it(self, attack):
        self.hp -= attack.damage
        Messages.add_info_message(Message("%s наносит %s единиц урона." % (
            attack.attacker.name,
            attack.damage
        ), RED_BLK))
        if self.hp < 1:
            self.kill_it(attack.attacker)

    def kill_it(self, _):
        pass

    def pick_up(self, items):
        if items is not None:
            self.inventory.pool.extend(items)

    def get_self_damage(self):
        weapons = self.inventory.get_weapons()
        return self.base_damage + sum([roll_damage(x) for x in weapons])

    def get_self_range(self):
        weapons = self.inventory.get_weapons()
        if weapons is None or len(weapons) < 1:
            return self.base_range
        weapon = weapons[0]
        return weapon.stats['range'].value

    def attack(self, target_cell):
        success = super().attack(target_cell)
        if not success:
            Messages.add_info_message(Message('Цель слишком далеко или заблокирована.'))
        return success