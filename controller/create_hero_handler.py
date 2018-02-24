import curses

from controller.handler import Handler
from engine.screen import Screen


class CreateHeroHandler(Handler):
    def __init__(self, instance=None):
        super().__init__(instance)
        if self.instance is None:
            from engine.instances.create_hero_instance import CreateHeroInstance
            screen = Screen(curses.LINES-1, curses.COLS-1)
            self.instance = CreateHeroInstance(screen)