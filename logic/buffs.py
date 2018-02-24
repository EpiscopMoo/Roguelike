from engine.guiengine import GRN_BLK
from globals import Message, Messages


class Buff:
    def __init__(self, duration, params):
        self.params = params
        self.duration = duration
        self.initial_duration = duration

    def apply(self, target):
        if self.duration > 0:
            self._effect(target)
            self.duration -= 1
        if self.duration == 0:
            self.wear_off_message()

    def _effect(self, target):
        pass

    def apply_message(self):
        pass

    def wear_off_message(self):
        pass


class HealBuff(Buff):
    def _effect(self, target):
        target.hp = min(target.hp+self.params['heal'], target.maxhp)

    def apply_message(self):
        Messages.add_info_message(Message('Вы кушаете мясики.', GRN_BLK))

    def wear_off_message(self):
        Messages.add_info_message(Message('Действие мясиков иссякло.'))
