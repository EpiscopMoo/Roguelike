import curses

from engine.guiengine import RED_BLK


class Selection:
    def __init__(self, screen, player, skin='+'):
        self.screen = screen
        self.pad = screen.get_pad()
        self.player = player
        self.skin = skin
        self.x = player.x
        self.y = player.y
        self.cells = player.cells
        lines, cols = self.screen.get_borders()
        self.posy, self.posx = lines // 2, cols // 2

    def print(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        cell = self.cells[self.y][self.x]
        if cell.get_skin() == ' ':
            self.pad.addstr(self.posy, self.posx, self.skin)
        else:
            self.pad.addstr(self.posy, self.posx, cell.get_skin(), curses.color_pair(RED_BLK))

    def left(self, cells):
        if self.x == 0:
            return False
        self.x -= 1
        return True

    def right(self, cells):
        if self.x == len(cells[0])-1:
            return False
        self.x += 1
        return True

    def up(self, cells):
        if self.y == 0:
            return False
        self.y -= 1
        return True

    def down(self, cells):
        if self.y == len(cells)-2:
            return False
        self.y += 1
        return True

    def target_cell(self):
        return self.cells[self.y][self.x]

    def reset(self):
        self.x = self.player.x
        self.y = self.player.y