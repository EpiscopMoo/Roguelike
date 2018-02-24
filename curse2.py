import curses

from engine.guiengine import init_colors
from engine.interaction import Interaction
from engine.logger import Logger
from globals import Globals


def main(stdscr):
    Logger.initialize()
    stdscr.refresh()
    init_colors()
    Globals.default_screen = stdscr
    Interaction().invoke()  # main game loop


curses.wrapper(main)
