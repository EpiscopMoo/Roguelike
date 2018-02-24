from enum import Enum
from random import random

from engine.guiengine import YLW_BLK
from globals import Messages, Message
from logic.path_finding import validate_visual_range, get_direction_towards_target


class Strategy:
    def feed_params(self, actor, cells, target=None):
        self.actor = actor
        self.cells = cells
        self.target = target
        return self

    def execute(self):
        pass


class StrategyRoam(Strategy):
    """Performs a move in a random direction on each execution call"""
    def execute(self):
        moved = self.actor.random_move()
        cnt = 0
        while not moved and cnt < 10:
            moved = self.actor.random_move()
            cnt += 1
        return True


class StrategyFollow(Strategy):
    """Performs a move in a direction towards a target on each execution call. The target is specified explicitly in feed_params"""
    def execute(self):
        my_pt = self.actor.y, self.actor.x
        player_pt = self.target.y, self.target.x
        newcell = get_direction_towards_target(self.cells, my_pt, player_pt)
        if newcell is not None:
            left = False
            right = False
            up = False
            down = False

            if newcell.x < self.actor.x:
                left = True
            elif newcell.x > self.actor.x:
                right = True
            if newcell.y < self.actor.y:
                up = True
            elif newcell.y > self.actor.y:
                down = True

            horizontal_move = left or right
            vertical_move = up or down
            if horizontal_move and vertical_move:
                r = random()
                if r < 0.5:
                    horizontal_move = False
                else:
                    vertical_move = False
            if horizontal_move:
                if left:
                    self.actor.left()
                if right:
                    self.actor.right()
            if vertical_move:
                if up:
                    self.actor.up()
                if down:
                    self.actor.down()
        return True


class StrategyAttackTarget(Strategy):
    """Performs an attack on a target on each execution call. The target is specified explicitly in feed_params"""
    def execute(self):
        y, x = self.target.y, self.target.x
        cell = self.cells[y][x]
        if cell.entity is not None:
            return self.actor.attack(cell)
        return False


### Composite strategies ###


class CStrategyChase(Strategy):
    """Perform a move towards a target or attack it, if possible."""
    def execute(self):
        attacked = StrategyAttackTarget().feed_params(self.actor, self.cells, self.target).execute()
        if not attacked:
            return StrategyFollow().feed_params(self.actor, self.cells, self.target).execute()
        return True


class CStrategyAttackWithinAqRange(Strategy):
    """If the target is within the acquisition range, move towards it until attacking is possible. Do nothing otherwise."""
    def execute(self):
        aqrange = self.actor.acquisition_range
        start = self.actor.y, self.actor.x
        finish = self.target.y, self.target.x
        can_see = validate_visual_range(self.cells, start, finish, aqrange)
        if can_see:
            return CStrategyChase().feed_params(self.actor, self.cells, self.target).execute()
        return False


class CStrategyPassiveAggressive(Strategy):
    """Roam until the target is within the acquisition range. Chase and attack it until the target leaves the
    acquisition range. On leave, continue roaming."""
    def execute(self):
        if self.target is None \
                or not CStrategyAttackWithinAqRange().feed_params(self.actor, self.cells, self.target).execute():
            return not StrategyRoam().feed_params(self.actor, self.cells).execute()
        return True


class CStrategyAggressive(Strategy):
    """Roam until pre-defined target is found. Once found, the target is chased down continuously."""
    def __init__(self):
        self.target_seen = False

    def execute(self):
        if self.target is None:
            raise Exception("None target passed to Aggressive strategy.")
        if self.target_seen:
            return CStrategyChase().feed_params(self.actor, self.cells, self.target).execute()
        self.target_seen = CStrategyPassiveAggressive().feed_params(self.actor, self.cells, self.target).execute()
        if self.target_seen:
            Messages.add_info_message(Message(self.actor.name + ' обнаружил(а) цель и готовится к атаке.', YLW_BLK))
        return self.target_seen




class StrategyEvent(Enum):
    ANY = 0
    BEING_HIT = 1
    SPOTTED_BY_PLAYER = 2
    SPOTTED_PLAYER = 3


class StrategyExecutor:
    def __init__(self, actor, cells, initial_strategy):
        self.actor = actor
        self.cells = cells
        self.strategy = initial_strategy
        self.transitions = {}
        self.target = None

    def add_transition(self, strategy_from, strategy_to, on_event):
        pass

    def feed_event(self, event):
        pass






"""

def find_target_within_aq_range(self):
    aqrange = self.actor.acquisition_range
    h = len(self.cells)
    w = len(self.cells[0])
    tly = max(0, self.actor.y - aqrange)
    tlx = max(0, self.actor.x - aqrange)
    bry = min(self.actor.y + aqrange + 1, h)
    brx = min(self.actor.x + aqrange + 1, w)
    for y in range(tly, bry):
        for x in range(tlx, brx):
            cell = self.cells[y][x]
            if cell.entity is not None and cell.entity.type == 'player':
                return StrategyAttackTarget().feed_params(self.actor, self.cells, cell.entity).execute()
    return False
"""