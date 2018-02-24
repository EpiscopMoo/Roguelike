import curses


from controller.handler import Handler
from engine.instances.menu_instance import MenuInstance
from engine.screen import Screen
from globals import Globals


class MainMenuHandler(Handler):
    def __init__(self):
        super().__init__()
        if Globals.MAIN_MENU in Globals.instances:
            self.instance = Globals.instances[Globals.MAIN_MENU]
        else:
            self.instance = MenuInstance(Screen(curses.LINES-1, curses.COLS-1), ["Новая игра", "Загрузить", "Об игре", "Выход"], 'Fix ignore in neigh4')
            Globals.instances[Globals.MAIN_MENU] = self.instance

    def process_key_event(self, key):
        choice = self.instance.process_key_event(key)
        NEW_GAME = 0
        LOAD_GAME = 1
        ABOUT = 2
        EXIT = 3
        if choice == NEW_GAME:
            from controller.splash_screen_handler import SplashScreenHandler
            from engine.instances.splash.intro_instance import IntroInstance
            return SplashScreenHandler(IntroInstance()), False
        elif choice == LOAD_GAME:
            return self, False
        elif choice == ABOUT:
            return self, False
        elif choice == EXIT:
            return None, None
        else:
            return self, False

