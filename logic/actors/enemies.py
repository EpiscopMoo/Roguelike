from globals import Globals
from logic.actors.actor import Behaviour
from logic.actors.enemy import EnemyActor
from logic.path_finding import get_direction_towards_target
from logic.strategies.strategy_executor import CStrategyPassiveAggressive, StrategyRoam, CStrategyAggressive


class Guano(EnemyActor):
    def __init__(self, container, cells):
        super().__init__(container, cells)
        self.skin = 'G'
        self.exp_gain = 1
        self.behave = Behaviour.PASSIVE
        self.pic = [
            '           ___        Фырх!',
            '         _/ @@\  Фырх!     ',
            '        ( \  O/__          ',
            '         \    \__)         ',
            '   /^^^^^     /            ',
            '  Ж \\\_____/\ \           ',
            '    IL       LLL           '
        ]
        self.strategy = StrategyRoam().feed_params(self, self.cells)
        self.name = "Гуано"
        self.description = "Почти безобидное травоядное шестилапое создание, коренной житель планеты Уитне. \"Почти\" " \
                           "- потому что в случае опасности гуано может вполне уверенно дать обидчику сдачи. Подобно " \
                           "слонам, гуано очень злопамятны, поэтому если вы сумели разозлить животное, то повторно " \
                           "приближаться не стоит, ибо извинения скорее всего не будут приняты."

    def hit_it(self, attack):
        if attack.damage > 0:
            self.last_attacker = attack.attacker
            self.hp -= attack.damage
            if type(self.strategy) == StrategyRoam:
                self.strategy = CStrategyPassiveAggressive().feed_params(self, self.cells, self.last_attacker)
        if self.hp < 1:
            self.kill_it(attack.attacker)

    def kill_it(self, attacker):
        attacker.exp += self.exp_gain
        super().kill_it(attacker)

    def make_move(self):
        self.strategy.execute()
        return True


class Fahgro(EnemyActor):
    def __init__(self, container, cells):
        super().__init__(container, cells)
        self.skin = 'F'
        self.exp_gain = 2
        self.strategy = CStrategyAggressive().feed_params(self, self.cells, Globals.player)
        self.acquisition_range = 8
        self.name = "Фагро"
        self.description = "Злобное создание размером с земную собаку, предположительно созданное гергонами для подавления " \
                           "наземных сил противника. По одиночке фагро не представляет угрозы для вооружённого человека, " \
                           "но стая таких тварей способна разорвать в клочья даже пехотинца в тяжёлой броне. В оперативных " \
                           "инструкциях Содружества настоятельно рекомендуется избегать любого контакта с ними."
        self.pic = [
            '                   ',
            '                   ',
            '                _   ',
            '       __,,,   / o\  ',
            '      /     \_//````  Фррх ',
            ' -====E______ /      ',
            '      ((     )\      '
        ]

    def hit_it(self, attack):
        self.hp -= attack.damage
        if self.hp < 1:
            self.kill_it(attack.attacker)

    def kill_it(self, attacker):
        attacker.exp += self.exp_gain
        super().kill_it(attacker)

    def make_move(self):
        self.strategy.execute()
        return True

