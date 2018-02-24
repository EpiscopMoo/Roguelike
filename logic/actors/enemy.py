from globals import Globals
from logic.actors.actor import Actor


class EnemyActor(Actor):
    def __init__(self, container, cells):
        super().__init__(container, cells)
        self.last_attacker = None
        self.type = 'enemy'
        self.acquisition_range = 1
        self.strategy = None

    def attack(self, target_cell):
        attacked = super().attack(target_cell)
        if target_cell.entity is not None:
            Globals.enemy_attacked = True
        return attacked