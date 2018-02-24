import curses

from controller.handler import Handler
from engine.screen import Screen
from globals import Globals


class MessageLogHandler(Handler):
    def __init__(self, instance=None):
        super().__init__(instance)
        if self.instance is None:
            if Globals.MESSAGE_LOG in Globals.instances:
                self.instance = Globals.instances[Globals.MESSAGE_LOG]
            else:
                from engine.instances.message_log_instance import MessageLogInstance
                #map_name = Globals.instances[Globals.DUNGEON]
                screen = Screen(curses.LINES-1, curses.COLS-1)
                self.instance = MessageLogInstance(screen)
                Globals.instances[Globals.MESSAGE_LOG] = self.instance
