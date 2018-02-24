import curses


from controller.handler import Handler
from controller.pause_menu_handler import PauseMenuHandler
from engine.screen import Screen
from globals import Globals


class DungeonHandler(Handler):
    def __init__(self, clazz=None, instance=None, overlay=None):
        super().__init__(instance, overlay)
        if instance is None:
            if Globals.DUNGEON in Globals.instances:
                self.instance = Globals.instances[Globals.DUNGEON]
            else:
                from engine.instances.dungeon_instance import DungeonInstance
                self.instance = DungeonInstance(Screen(curses.LINES - 11, curses.COLS - 1), clazz)
                Globals.instances[Globals.DUNGEON] = self.instance

    def process_key_event(self, key):
        if self.overlay is not None:
            return self.overlay.process_key_event(key)
        if key == ord('q'):
            return PauseMenuHandler(), False
        handler, moved = self.instance.process_key_event(key)
        if moved:
            super().invoke()
            self.instance.enemy_action()
            gameover = self.instance.is_game_over()
            if gameover:
                from controller.main_menu_handler import MainMenuHandler
                return MainMenuHandler(), moved
            self.instance.apply_buffs()
        return handler, moved

    def invoke(self):
        Globals.enemy_attack_delay()
        super().invoke()
        if self.overlay is not None:
            self.overlay.invoke()
        Globals.reset_attack_delay()