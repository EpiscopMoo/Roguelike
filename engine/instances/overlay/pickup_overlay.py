import curses

from engine.guiengine import get_dy_dx, draw_overlay_window, WHT_BLK, draw_text, BLK_WHT
from engine.instances.overlay.overlay import Overlay
from engine.screen import Screen


class PickUpOverlay(Overlay):
    def __init__(self, inventory, cell):
        super().__init__()
        self.cell = cell
        self.loot = cell.loot
        self.inventory = inventory
        self.current = 0

        self.h = len(self.loot.items) + 5
        self.w = 82
        self.H = curses.LINES - 1
        self.W = curses.COLS - 1
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)
        self.screen = Screen(self.h, self.w, self.dy, self.dx)
        self.pad = self.screen.pad

    def print(self):
        draw_overlay_window(self.pad, 0, 0, self.h, self.w, 'Подобрать предметы', '[Enter] - Взять, [Пробел] - Выход', color=WHT_BLK)
        for i, item in enumerate(self.loot.items):
            draw_text(self.pad, 3+i, 5, self.h-4, self.w-7, item.name, BLK_WHT if i==self.current else WHT_BLK)

    def process_key_event(self, key):
        new_overlay = self
        from controller.dungeon_handler import DungeonHandler
        if key == ord('q') or key == ord(' '):
            new_overlay = None
        elif key == curses.KEY_UP:
            self._process_up()
        elif key == curses.KEY_DOWN:
            self._process_down()
        elif key == ord('\n'):
            new_overlay = self._process_enter()
        return DungeonHandler(overlay=new_overlay), False

    def _process_up(self):
        if self.current > 0:
            self.current -= 1

    def _process_down(self):
        if self.current < len(self.loot.items) - 1:
            self.current += 1

    def _process_enter(self):
        i = self.current
        items = self.loot.items
        item = items[i]
        items.remove(item)
        self.inventory.add_item_to_pool(item)
        if len(items) == 0:
            self.cell.loot = None
            return None
        elif i >= len(items):
            self.current = len(items) - 1
        return self