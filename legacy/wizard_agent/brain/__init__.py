from . import random_strategy
from . import flee_strategy
from . import move_strategy
from . import basic_bomb_strategy
from . import reload_strategy
from . import treasure_strategy
from . import ore_bomb_strategy
from . import bomb_placement_strategy
from . import kill_strategy
from . import combo_kill_strategy
from . import retreat_strategy
from . import smart_bomb_strategy
from . import smart_collection_strategy

def RandomStrategy():
    return random_strategy.RandomStrategy()


def FleeStrategy():
    return flee_strategy.FleeStrategy()


def MoveStrategy():
    return move_strategy.MoveStrategy()


def BasicBombStrategy():
    return basic_bomb_strategy.BasicBombStrategy()

def BombPlacementStrategy():
    return bomb_placement_strategy.BombPlacementStrategy()

def OreBombStrategy():
    return ore_bomb_strategy.OreBombStrategy()


def KillStrategy():
    return kill_strategy.KillStrategy()

def ComboKillStrategy():
    return combo_kill_strategy.ComboKillStrategy()


def RetreatStrategy():
    return retreat_strategy.RetreatStrategy()


def SmartBombStrategy():
    return smart_bomb_strategy.SmartBombStrategy()

def SmartCollectionStrategy():
    return smart_collection_strategy.SmartCollectionStrategy()
