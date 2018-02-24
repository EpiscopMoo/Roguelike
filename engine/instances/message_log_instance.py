from engine.guiengine import draw_window, draw_messages
from engine.instances.instance import Instance
from globals import Messages


class MessageLogInstance(Instance):
    def __init__(self, screen):
        self.screen = screen
        self.pad = screen.pad

    def invoke(self):
        self.screen.clear()
        self._print_borders()
        self._print_messages()
        self.screen.refresh()

    def process_key_event(self, key):
        from controller.dungeon_handler import DungeonHandler
        if key == ord('m') or key == ord('q'):
            return DungeonHandler(), False
        return DungeonHandler(overlay=self), False

    def _print_borders(self):
        draw_window(self.pad, 0, 0, self.screen.H-1, self.screen.W-1, 'История сообщений (новые - выше)',
                    '[PgUp] - Вверх [PgDn] - Вниз [M] - Выход')

    def _print_messages(self):
        messages = Messages.get_full_info_messages()
        draw_messages(self.pad, 2, 3, self.screen.H-5, self.screen.W-7, messages)