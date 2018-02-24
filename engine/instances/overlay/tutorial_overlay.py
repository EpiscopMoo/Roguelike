import curses

from engine.guiengine import get_dy_dx, draw_text, draw_overlay_window, BLU_WHT
from engine.instances.overlay.overlay import Overlay
from engine.screen import Screen
from globals import Globals


class MoveTutorialOverlay(Overlay):
    def __init__(self):
        super().__init__()
        self.h = 9
        self.w = 82
        self.H = curses.LINES - 1
        self.W = curses.COLS - 1
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)
        self.screen = Screen(self.h, self.w, self.dy, self.dx)
        self.pad = self.screen.pad
        self.text = 'Для перемещения используйте стрелки. Одно перемещение обычно тратит один ход. Пока вы стоите, ' \
                    'время не идёт, так что вы всегда можете как следует обдумать свои действия. Попробуйте подвигаться' \
                    ' с помощью стрелок.'

    def print(self):
        draw_overlay_window(self.pad, 0, 0, self.h, self.w, 'Обучение', '[Enter] - OK, [C] - Пропустить обучение')
        draw_text(self.pad, 3, 5, self.h-4, self.w-7, self.text, BLU_WHT)

    def process_key_event(self, key):
        from controller.dungeon_handler import DungeonHandler
        if key == ord('c'):
            from engine.instances.dungeon_instance import TUT_DONE
            Globals.instances[Globals.DUNGEON].tutorial_stage = TUT_DONE
            return DungeonHandler(overlay=EndTutorialOverlay()), False
        if key == ord('\n'):
            return DungeonHandler(), False
        else:
            return DungeonHandler(overlay=self), False


class LookTutorialOverlay(Overlay):
    def __init__(self):
        super().__init__()
        self.h = 9
        self.w = 82
        self.H = curses.LINES - 1
        self.W = curses.COLS - 1
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)
        self.screen = Screen(self.h, self.w, self.dy, self.dx)
        self.pad = self.screen.pad
        self.text = 'Отлично! А теперь попробуем осмотреться. Для того, чтобы переключиться в режим обзора, нажмите ' \
                    '[Enter]. В этом режиме с помощью стрелочек вы можете двигать курсор по всему уровню, получая при ' \
                    'этом подробную информацию о любом объекте под курсором. Для выхода из режима обзора нажмите [Enter].'

    def print(self):
        draw_overlay_window(self.pad, 0, 0, self.h, self.w, 'Обучение', '[Enter] - OK')
        draw_text(self.pad, 3, 5, self.h-4, self.w-7, self.text, BLU_WHT)

    def process_key_event(self, key):
        from controller.dungeon_handler import DungeonHandler
        if key == ord('\n'):
            return DungeonHandler(), False
        else:
            return DungeonHandler(overlay=self), False


class LookTutorialOverlay2(Overlay):
    def __init__(self):
        super().__init__()
        self.h = 11
        self.w = 82
        self.H = curses.LINES - 1
        self.W = curses.COLS - 1
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)
        self.screen = Screen(self.h, self.w, self.dy, self.dx)
        self.pad = self.screen.pad
        self.text = 'Помните, что движение курсора в любом режиме не отнимает игровых ходов. ' \
                    'А теперь опробуйте боевой режим. Подойдите вплотную к Гуано (G) и нажмите [A]. Активируется режим ' \
                    'атаки. Он очень похож на режим обзора с той лишь разницей, что отображается подробная информация о ' \
                    'противнике и имеется возможность атаковать. Затем наведите курсор на цель и нажмите [Пробел] для атаки. '

    def print(self):
        draw_overlay_window(self.pad, 0, 0, self.h, self.w, 'Обучение', '[Enter] - OK')
        draw_text(self.pad, 3, 5, self.h-4, self.w-7, self.text, BLU_WHT)

    def process_key_event(self, key):
        from controller.dungeon_handler import DungeonHandler
        if key == ord('\n'):
            return DungeonHandler(), False
        else:
            return DungeonHandler(overlay=self), False


class AttackTutorialOverlay(Overlay):
    def __init__(self):
        super().__init__()
        self.h = 9
        self.w = 82
        self.H = curses.LINES - 1
        self.W = curses.COLS - 1
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)
        self.screen = Screen(self.h, self.w, self.dy, self.dx)
        self.pad = self.screen.pad
        self.text = 'Продолжайте атаковать противника, нажимая клавишу [Пробел], пока он не умрёт. После этого нажмите ' \
                    '[A] для выхода из режима боя.'

    def print(self):
        draw_overlay_window(self.pad, 0, 0, self.h, self.w, 'Обучение', '[Enter] - OK')
        draw_text(self.pad, 3, 5, self.h-4, self.w-7, self.text, BLU_WHT)

    def process_key_event(self, key):
        from controller.dungeon_handler import DungeonHandler
        if key == ord('\n'):
            return DungeonHandler(), False
        else:
            return DungeonHandler(overlay=self), False


class EndTutorialOverlay(Overlay):
    def __init__(self):
        super().__init__()
        self.h = 9
        self.w = 82
        self.H = curses.LINES - 1
        self.W = curses.COLS - 1
        self.dy, self.dx = get_dy_dx(self.H, self.W, self.h, self.w)
        self.screen = Screen(self.h, self.w, self.dy, self.dx)
        self.pad = self.screen.pad
        self.text = 'Базовое обучение завершено. Если Вы забыли нужную клавишу, то нажмите [H] для вызова помощи. Удачи!'

    def print(self):
        draw_overlay_window(self.pad, 0, 0, self.h, self.w, 'Обучение', '[Enter] - OK')
        draw_text(self.pad, 3, 5, self.h-4, self.w-7, self.text, BLU_WHT)

    def process_key_event(self, key):
        from controller.dungeon_handler import DungeonHandler
        if key == ord('\n'):
            return DungeonHandler(), False
        else:
            return DungeonHandler(overlay=self), False