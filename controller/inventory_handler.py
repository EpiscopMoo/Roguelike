import curses

from controller.handler import Handler
from engine.screen import Screen
from globals import Globals


class InventoryHandler(Handler):
    def __init__(self, instance=None):
        super().__init__(instance)
        if self.instance is None:
            if Globals.INVENTORY in Globals.instances:
                self.instance = Globals.instances[Globals.INVENTORY]
            else:
                from engine.instances.inventory_instance import InventoryInstance
                dungeon = Globals.instances[Globals.DUNGEON]
                screen = Screen(curses.LINES-1, curses.COLS-1)
                self.instance = InventoryInstance(screen, dungeon.player)
                Globals.instances[Globals.INVENTORY] = self.instance
