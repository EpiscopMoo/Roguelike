from enum import Enum

from controller.dungeon_handler import DungeonHandler
from controller.inventory_handler import InventoryHandler
from controller.message_log_handler import MessageLogHandler
from engine.guiengine import *
from engine.dungeon_gui import GUI
from engine.instances.instance import Instance
from engine.instances.overlay.pickup_overlay import PickUpOverlay
from engine.instances.overlay.tutorial_overlay import LookTutorialOverlay, EndTutorialOverlay, LookTutorialOverlay2, \
    AttackTutorialOverlay
from engine.screen import Screen
from engine.selection import Selection
from globals import Globals
from logic.actors.hero import Hero
from logic.map_loader_adv import MapLoader


class Action(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    MODE_MOVE = 5
    MODE_SELECT = 6
    MODE_ATTACK = 9
    MODE_INVENTORY = 10
    HURT = 7
    ATTACK = 8


#tutorial stages
TUT_MOVE = 1
TUT_LOOK = 2
TUT_LOOK2 = 3
TUT_ATTK = 4
TUT_DONE = 5

OVERLAYS = {
    TUT_MOVE: None,
    TUT_LOOK: LookTutorialOverlay(),
    TUT_LOOK2:LookTutorialOverlay2(),
    TUT_ATTK: AttackTutorialOverlay(),
    TUT_DONE: EndTutorialOverlay()
}

OVERLAYS_DELAYS = {
    TUT_MOVE: 10,
    TUT_LOOK: 30,
    TUT_LOOK2:0,
    TUT_ATTK: 10,
    TUT_DONE: 0
}


class DungeonInstance(Instance):
    def __init__(self, screen, clazz):
        self.screen = screen
        self.pad = screen.get_pad()
        self.mode = Action.MODE_MOVE
        self.gui = self._init_gui()
        self.player = Hero(clazz, None, None)
        self.__load_map()

        from engine.instances.inventory_instance import InventoryInstance
        Globals.instances[Globals.INVENTORY] = InventoryInstance(Screen(curses.LINES-1, curses.COLS-1), self.player)
        self.selection = Selection(screen, self.player)
        self.h = len(self.cells)
        self.w = len(self.cells[0])

        self.tutorial_stage = TUT_MOVE
        self.tutorial_move_count = 0
        self.overlay = None
        self.tut_updated = False

    def __load_map(self):
        info = MapLoader().process_map('logic/levels/', 'dungeon01')
        self.cells = info.cells
        (self.player.y, self.player.x) = info.player_position
        self.characters = info.characters
        self.player.cells = self.cells
        self.player.container = self.characters
        self.characters.append(self.player)
        self.cells[self.player.y][self.player.x].entity = self.player
        self.map_name = info.name


    def invoke(self):
        self.screen.clear()
        self.gui.screen.clear()
        self._print_dungeon()
        h,w = self.screen.get_borders()
        draw_window(self.pad, 0, 0, h-2, w-1, self.map_name, '[Enter] Осмотреться [A] Атака [q] Выход')
        self.gui.print(self.player)
        self.screen.refresh()
        self.gui.screen.refresh()

    def update_tutorial_stage(self, to_state=None):
        if self.tut_updated:
            return
        if to_state is not None:
            if to_state > self.tutorial_stage:
                self.tutorial_move_count = 0
                self.tutorial_stage = to_state
                self.overlay = OVERLAYS[self.tutorial_stage]
                self.tut_updated = True
        elif OVERLAYS_DELAYS[self.tutorial_stage] == 0:
            self.overlay = None
            return
        else:
            self.tutorial_move_count += 1
            self.overlay = None
            self.tut_updated = True
            if self.tutorial_move_count >= OVERLAYS_DELAYS[self.tutorial_stage]:
                self.tutorial_move_count = 0
                self.tutorial_stage += 1
                self.overlay = OVERLAYS[self.tutorial_stage]

    def process_key_event(self, key):
        self.tut_updated = False
        moved = False
        if key == ord('\n') and self.tutorial_stage > TUT_MOVE:
            self.select_mode()
            moved = False
        if key == ord('a') and self.tutorial_stage > TUT_LOOK:
            self.attack_mode()
            moved = False
        if key == ord(' ') and self.tutorial_stage > TUT_LOOK:
            moved = self.fire()
            if self.overlay is not None:
                overlay = self.overlay
                self.overlay = None
                return DungeonHandler(overlay=overlay), False
        if key == ord('i'):
            return InventoryHandler(), False
        if key == ord('m'):
            return MessageLogHandler(), False
        if key == ord('w'):
            moved = True
        if self.mode == Action.MODE_MOVE:
            if key == curses.KEY_LEFT:
                moved = self.player.left()
            elif key == curses.KEY_RIGHT:
                moved = self.player.right()
            elif key == curses.KEY_UP:
                moved = self.player.up()
            elif key == curses.KEY_DOWN:
                moved = self.player.down()
            self.selection.reset()
        elif self.mode == Action.MODE_SELECT or self.mode == Action.MODE_ATTACK:
            if key == curses.KEY_LEFT:
                self.selection.left(self.cells)
            elif key == curses.KEY_RIGHT:
                self.selection.right(self.cells)
            elif key == curses.KEY_UP:
                self.selection.up(self.cells)
            elif key == curses.KEY_DOWN:
                self.selection.down(self.cells)
        self.update_tutorial_stage()
        return DungeonHandler(overlay=self.overlay), moved

    def _init_gui(self):
        vdiff = curses.LINES - self.screen.H
        guiscreen = Screen(vdiff, curses.COLS-1, curses.LINES-vdiff-1, 0)
        return GUI(guiscreen)

    def _print_dungeon(self):
        lines, cols = self.screen.get_borders()
        posy, posx = lines // 2, cols // 2
        y, x = self.selection.y, self.selection.x
        xstart = max(0, x - posx)
        ystart = max(0, y - posy)
        xend = min(x + posx, self.w)
        yend = min(y + posy, self.h)
        for i in range(xstart, xend):
            for j in range(ystart, yend):
                coordY = j - y + posy
                coordX = i - x + posx
                self.cells[j][i].draw(self.pad, coordY, coordX)
        if self.mode == Action.MODE_SELECT or self.mode == Action.MODE_ATTACK:
            self.selection.print()

    def select_mode(self):
        if self.mode == Action.MODE_MOVE:
            self.mode = Action.MODE_SELECT
            self.gui.show_description(self.selection)
        else:
            self.mode = Action.MODE_MOVE
            self.selection.reset()
            self.gui.show_default()

    def attack_mode(self):
        if self.mode == Action.MODE_MOVE:
            self.mode = Action.MODE_ATTACK
            self.gui.show_combat_data(self.selection)
        else:
            self.mode = Action.MODE_MOVE
            self.selection.reset()
            self.gui.show_default()

    def fire(self):
        if self.mode == Action.MODE_ATTACK:
            self.update_tutorial_stage(TUT_ATTK)
            cell = self.selection.target_cell()
            if cell.entity is not None:
                return self.player.attack(cell)
        else:
            cell = self.cells[self.player.y][self.player.x]
            if cell.loot is not None:
                self.overlay = PickUpOverlay(self.player.inventory, cell)
        return False

    def enemy_action(self):
        for char in self.characters:
            if char != self.player:
                char.make_move()

    def is_game_over(self):
        if self.player.hp < 1:
            return True
        return False

    def apply_buffs(self):
        for char in self.characters:
            char.apply_buffs()

