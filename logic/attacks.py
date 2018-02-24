class AttackType:
    def __init__(self, params):
        self.attacker = params['attacker']
        self.damage = params['damage']


class MeleeAttack(AttackType):
    def __init__(self, params):
        super().__init__(params)
        self.damage = params['damage']
        self.distance = 0