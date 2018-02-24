import curses

from controller.dungeon_handler import DungeonHandler
from controller.inventory_handler import InventoryHandler
from engine.guiengine import draw_window, BLK_WHT, draw_text, draw_pic, draw_hero_stats
from engine.instances.instance import Instance

WEAPON = -2
ARMOR = -3
SHIELD = -4
HELMET = -5


def all_not_none(f):
    def wrapper(*args):
        ls = f(*args)
        return [x for x in ls if x is not None]
    return wrapper


def _convert_type_to_key(_type):
    if _type == 'weapon':
        return WEAPON
    if _type == 'armor':
        return ARMOR
    if _type == 'shield':
        return SHIELD
    if _type == 'helmet':
        return HELMET


class InventoryInstance(Instance):
    def __init__(self, screen, player):
        self.player = player
        self.pool = []
        self.equipped = {WEAPON: None, ARMOR: None, SHIELD: None, HELMET: None}
        self.screen = screen
        self.pad = screen.get_pad()
        self.current = 0
        self.window = 0
        self.player.inventory = self
        player.pick_up(player.clazz.get_start_items())

    def add_item_to_pool(self, item):
        matches = [it for it in self.pool if it.name == item.name]
        if len(matches) > 0:
            match = matches[0]
            match.quantity += 1
        else:
            self.pool.append(item)

    def remove_item_from_pool(self, item):
        if item.quantity > 1:
            item.quantity -= 1
        else:
            self.pool.remove(item)

    def invoke(self):
        self.screen.clear()
        self._print_borders()
        self._print_pool()
        self._print_info()
        self._print_equipped()
        self._print_stats()
        self.screen.refresh()

    def process_key_event(self, key):
        if self._move_selection(key):
            return InventoryHandler(), False
        if key == ord('i'):
            return DungeonHandler(), False
        if key == ord('\t'):
            self._switch_window()
        if key == ord('\n'):
            self._select_item()
        return InventoryHandler(), False

    def _print_borders(self):
        fh, fw = self.screen.get_borders()
        h, w = fh, fw
        w -= 2
        draw_window(self.pad, 0, 0, h, w, 'Инвентарь')
        h = h//2 - 2
        w = w//2 - 2
        draw_window(self.pad, 1,        2,          h, w - 1,   'Предметы')
        draw_window(self.pad, 1,        2 + w + 1,  h, w,       'Экипированные предметы')
        draw_window(self.pad, h + 2,    2,          h, w - 1,   'Характеристики предмета')
        draw_window(self.pad, h + 2,    w + 3,      h, w,       'Персонаж')
        self.pad.addstr(fh-1, 3, '[Enter] - одеть/снять [Tab] - переключиться между окнами [i] - назад в игру')

    def _print_pool(self):
        y = 3
        for i, item in enumerate(self.pool):
            if i==self.current:
                self.pad.addstr(i+y, 4, item.get_name(), curses.color_pair(BLK_WHT))
            else:
                self.pad.addstr(i + y, 4, item.get_name())

    def _print_info(self):
        if self.current == -1:
            return
        item = None
        if self.current < 0:
            item = self.equipped[self.current]
        else:
            if len(self.pool) > 0:
                item = self.pool[self.current]
        if item is None:
            return
        descritems = item.get_printout()
        fh, fw = self.screen.get_borders()
        y = fh//2 + 1
        x = 4
        self.pad.addstr(y, x, item.name)
        y += 2
        for i, info in enumerate(descritems):
            self.pad.addstr(y, x, info)
            y += 1
        draw_text(self.pad, y, x, fh-y, (fw-2)//2-6, item.description)
        if 'pic' in item.stats:
            draw_pic(self.pad, 3, (fw-2)//2-fw//4, item.stats['pic'])

    def _select_item(self):
        if self.current < 0:
            item = self.equipped[self.current]
            #self.pool.append(item)
            self.add_item_to_pool(item)
            self.equipped[self.current] = None

        elif self.current < len(self.pool):
            item = self.pool[self.current]
            if item.consumable:
                buffs = item.stats['buffs']
                self.player.add_buffs(buffs)
                #self.pool.remove(item)
                self.remove_item_from_pool(item)
            else:
                self.equip(item)
        self._clamp_idx()

    def _print_equipped(self):
        _, w = self.screen.get_borders()
        w = w // 2 - 2
        x = 2 + w + 1

        item_w = 16
        item_small_h = 8
        item_large_h = 13

        overall_width = item_w*3 + 8
        x = x + w//2 - overall_width//2
        y = 3

        weapon_selected = True if self.current == WEAPON else False
        armor_selected = True if self.current == ARMOR else False
        helmet_selected = True if self.current == HELMET else False
        shield_selected = True if self.current == SHIELD else False

        y_weapon = y + item_small_h + 2
        x_weapon = x
        draw_window(self.pad, y_weapon, x_weapon, item_large_h, item_w, 'Оружие', selected=weapon_selected)
        if self.equipped[WEAPON] is not None:
            draw_pic(self.pad, y_weapon+1, x_weapon+1, self.equipped[WEAPON].stats['pic'])

        y_helmet = y
        x_helmet = x + item_w + 3
        draw_window(self.pad, y_helmet, x_helmet, item_small_h, item_w, 'Шлем', selected=helmet_selected)
        if self.equipped[HELMET] is not None:
            draw_pic(self.pad, y_helmet+1, x_helmet+1, self.equipped[HELMET].stats['pic'])

        y_armor = y_weapon
        x_armor = x_weapon + 3 + item_w
        draw_window(self.pad, y_armor, x_armor, item_large_h, item_w, 'Броня', selected=armor_selected)
        if self.equipped[ARMOR] is not None:
            draw_pic(self.pad, y_armor+1, x_armor+1, self.equipped[ARMOR].stats['pic'])

        y_shield = y_armor
        x_shield = x_armor + 3 + item_w
        draw_window(self.pad, y_shield, x_shield, item_large_h, item_w, 'Щит', selected=shield_selected)
        if self.equipped[SHIELD] is not None:
            draw_pic(self.pad, y_shield+1, x_shield+1, self.equipped[SHIELD].stats['pic'])

    def _get_equipped_by_type(self, type):
        if type == 'weapon':
            return self.equipped[WEAPON]
        if type == 'armor':
            return self.equipped[ARMOR]
        if type == 'shield':
            return self.equipped[SHIELD]
        if type == 'helmet':
            return self.equipped[HELMET]
        return -1

    def _clamp_idx(self):
        if self.current < 0:
            self.current = 0
        else:
            if self.current >= len(self.pool):
                self.current = len(self.pool)-1

    def _switch_window(self):
        if self.current < 0:
            self._clamp_idx()
        else:
            self.current = WEAPON

    def _move_selection(self, key):
        if self.current < 0:
            if self.current == WEAPON:
                if key == curses.KEY_RIGHT:
                    self.current = ARMOR
                    return True
            if self.current == SHIELD:
                if key == curses.KEY_LEFT:
                    self.current = ARMOR
                    return True
            if self.current == HELMET:
                if key == curses.KEY_DOWN:
                    self.current = ARMOR
                    return True
            if self.current == ARMOR:
                if key == curses.KEY_UP:
                    self.current = HELMET
                    return True
                elif key == curses.KEY_LEFT:
                    self.current = WEAPON
                    return True
                elif key == curses.KEY_RIGHT:
                    self.current = SHIELD
                    return True
        else:
            if key == curses.KEY_UP and self.current > 0:
                self.current -= 1
                return True
            elif key == curses.KEY_DOWN and self.current < len(self.pool) - 1:
                self.current += 1
                return True
        return False

    def equip(self, item):
        key = _convert_type_to_key(item.type)
        if self.equipped[key] is not None:
            #self.pool.append(self.equipped[key])
            self.add_item_to_pool(self.equipped[key])
        self.equipped[key] = item
        if item in self.pool:
            #self.pool.remove(item)
            self.remove_item_from_pool(item)

    def _print_stats(self):
        h, w = self.screen.get_borders()
        h = h // 2 - 2
        w = (w-2) // 2 - 2
        y = h + 2
        x = w + 3
        draw_hero_stats(self.pad, y+1, x+2, self.player)

    @all_not_none
    def get_weapons(self):
        if self.equipped[SHIELD] is not None and self.equipped[SHIELD].type == 'weapon':
            return [self.equipped[WEAPON], self.equipped[SHIELD]]
        return [self.equipped[WEAPON]]

    @all_not_none
    def get_armors(self):
        if self.equipped[SHIELD] is not None and self.equipped[SHIELD].type == 'weapon':
            return [self.equipped[HELMET], self.equipped[ARMOR]]
        return [self.equipped[HELMET], self.equipped[ARMOR], self.equipped[SHIELD]]
