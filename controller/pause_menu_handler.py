import curses

from controller.handler import Handler
from engine.instances.menu_instance import MenuInstance
from engine.screen import Screen
from globals import Globals


class PauseMenuHandler(Handler):
    def __init__(self):
        super().__init__()
        if Globals.PAUSE_MENU in Globals.instances:
            self.instance = Globals.instances[Globals.PAUSE_MENU]
        else:
            self.instance = MenuInstance(Screen(curses.LINES-1, curses.COLS-1), ["Назад в игру", "Выход"])
            Globals.instances[Globals.PAUSE_MENU] = self.instance

    def process_key_event(self, key):
        choice = self.instance.process_key_event(key)
        BACK = 0
        EXIT = 1
        if choice == BACK:
            from controller.dungeon_handler import DungeonHandler
            return DungeonHandler(), False
        elif choice == EXIT:
            return None, None
        else:
            return self, False