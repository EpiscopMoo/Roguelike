import curses
from globals import Globals


class Screen:
    def __init__(self, H, W, fromy=0, fromx=0):
        self.screen = Globals.default_screen
        self.H = H
        self.W = W
        curses.curs_set(False)
        self.pad = curses.newpad(self.H+1, self.W+1)
        self.bordery = H
        self.borderx = W
        self.fromx = fromx
        self.fromy = fromy

    def refresh(self):
        self.pad.refresh(0, 0, self.fromy, self.fromx+1, self.fromy+self.bordery, self.fromx+self.borderx)

    def clear(self):
        self.pad.clear()

    def get_pad(self):
        return self.pad

    def get_borders(self):
        return self.bordery, self.borderx