from engine.guiengine import *
from globals import Messages


class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.pad = screen.get_pad()
        self.name = ''
        self.description = ''
        self.mode = "default"
        self.pic = None
        self.selection = None
        self.x1 = 0
        self.x2 = screen.W // 3
        self.x3 = screen.W // 3 * 2
        self.w1 = self.x2-self.x1 - 1
        self.w2 = self.x3-self.x2 - 1
        self.w3 = screen.W-self.x3 - 1
        self.h = screen.H
        self.w = screen.W

    def _print_stats(self, player):
        draw_window(self.pad, 0, self.x2, self.h, self.w2, 'Характеристики')
        draw_hero_stats(self.pad, 1, self.x2+2, player)

    def print_pic(self):
        if self.pic is not None:
            draw_pic(self.pad, 1, self.x3, self.pic)

    def print(self, player):
        if self.mode == "description":
            draw_window(self.pad, 0, self.x1, self.h, self.w-1, 'Описание')
            draw_text(self.pad, 1, self.x1+2, self.h, self.w1, "Нажмите [Enter] для отмены")
            self._print_description()
        else:
            draw_window(self.pad, 0, self.x1, self.h, self.w2, 'Статус')
            if self.mode == "combat":
                draw_window(self.pad, 0, self.x3, self.h, self.w3, 'Враг')
                draw_text(self.pad, 1, self.x1+2, self.h, self.w1, "Нажмите [Пробел] для атаки, [А] для отмены")
                self._print_stats(player)
                self._print_enemy_stats()
            elif self.mode == "default":
                self._print_stats(player)
            self._print_messages(Messages.get_info_messages())

    def show_description(self, selection):
        self.mode = "description"
        self.selection = selection

    def _print_description(self):
        cell = self.selection.target_cell()
        if cell is not None:
            self.name = '[' + cell.get_name() + ']'
            self.description = cell.get_description()
            self.pic = cell.get_pic()
            self.pad.addstr(3, 2, self.name)
            draw_text(self.pad, 4, self.x1+2, self.h, self.w1+self.w2-1, self.description)
            self.print_pic()

    def show_combat_data(self, selection):
        self.mode = "combat"
        self.selection = selection

    def show_default(self):
        self.mode = "default"
        self.name = ''
        self.description = ''
        self.pic = None
        self.selection = None

    def _print_enemy_stats(self):
        if self.selection is not None:
            cell = self.selection.target_cell()
            if cell.entity is not None and cell.entity.type == "enemy":
                draw_enemy_stats(self.pad, 1, self.x3+2, cell.entity)

    def _print_messages(self, messages):
        draw_messages(self.pad, 2, self.x1+2, self.h-1, self.w1, messages)
