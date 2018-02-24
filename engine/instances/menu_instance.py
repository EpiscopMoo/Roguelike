import curses

from engine.guiengine import BLK_WHT


class MenuInstance:
    def __init__(self, screen, options, title=''):
        self.screen = screen
        self.pad = screen.get_pad()
        self.menu_exit = False
        self.current = 0
        self.options = options
        self.dx = max(1, screen.W // 2 - len(options[0]) // 2)
        self.dy = max(1, screen.H // 2 - len(options) // 2)
        self.title = title

    def process_key_event(self, key):
        if key == curses.KEY_UP and self.current > 0:
            self.current -= 1
        elif key == curses.KEY_DOWN and self.current < len(self.options) - 1:
            self.current += 1
        elif key == ord('\n'):
            return self.current
        return -1

    def invoke(self):
        self.print()
        self.screen.refresh()

    def print(self):
        self.pad.addstr(max(0, self.dy - 2), max(0, self.dx - 2), self.title)
        i = 0
        for option in self.options:
            if self.current == i:
                self.pad.addstr(self.dy + i, self.dx, option, curses.color_pair(BLK_WHT))
            else:
                self.pad.addstr(self.dy + i, self.dx, option)
            i += 1