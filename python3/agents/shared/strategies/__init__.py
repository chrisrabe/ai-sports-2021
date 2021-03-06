"""
Contains different strategies used in the game
"""

from .random_strategy import RandomStrategy
from .retreat_strategy import RetreatStrategy
from .pickup_strategy import PickupStrategy
from .stalk_strategy import StalkStrategy, StalkTwoStrategy
from .basic_avoid_strategy import BasicAvoidStrategy
from .adv_kill_strategy import AdvKillStrategy
from .block_destroying import BlockDestroyingStrategy
from .detonate_strategy import DetonateStrategy
from .bomb_strategy import BombStrategy
from .simple_bomb import SimpleBombStrategy
from .wait_strategy import WaitStrategy
from .adv_block_destroy import AdvBlockStrategy
from .lurk_strategy import LurkStrategy
from .playzone_strategy import PlayzoneStrategy
from .dodge_flame_strategy import DodgeFlameStrategy
