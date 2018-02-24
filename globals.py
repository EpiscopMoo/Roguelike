import time


class Message:
    def __init__(self, text, color=None):
        self.color = color
        self.text = text


class Messages:
    combat = []
    info = []

    @staticmethod
    def add_combat_message(msg):
        Messages.combat.append(msg)

    @staticmethod
    def add_info_message(msg):
        Messages.info.append(msg)

    @staticmethod
    def get_info_messages():
        return list(reversed(Messages.info))[:10]

    @staticmethod
    def get_full_info_messages():
        return list(reversed(Messages.info))

    @staticmethod
    def get_combat_messages():
        return list(reversed(Messages.combat))

    @staticmethod
    def reset_combat_messages():
        Messages.combat = []


class Globals:
    default_screen = None
    instances = {}
    enemy_attacked = False
    player = None

    MAIN_MENU = 0
    DUNGEON = 1
    PAUSE_MENU = 2
    INVENTORY = 3
    MESSAGE_LOG = 4

    @staticmethod
    def enemy_attack_delay():
        if Globals.enemy_attacked is True:
            time.sleep(0.3)

    @staticmethod
    def reset_attack_delay():
        Globals.enemy_attacked = False