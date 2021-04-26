"""
Tracks the game state and decides on next strategy to execute
"""

from .bomb_tracker import BombTracker
from .enemy_tracker import EnemyTracker
from .map_tracker import MapTracker
from .pickup_tracker import PickupTracker


class Brain:
    def __init__(self):
        self.bomb_tracker = BombTracker()
        self.enemy_tracker = EnemyTracker()
        self.map_tracker = MapTracker()
        self.pickup_tracker = PickupTracker()

    def get_next_strategy(self, game_state) -> str:
        """Conditionals to decide which strategy to execute. Returns string"""
        self.enemy_tracker.update(game_state)
        self.bomb_tracker.update(game_state)
        self.map_tracker.update(game_state)
        self.pickup_tracker.update(game_state)

        # enemy is trapped

        # Highest Prio (base state): Collect + Stay away from immediate danger (fire + potential blast zones)
        # 2nd highest Destroy walls
        # --> If possible; KILL.

        # For destroy strats:
        # -> If it's at the highest spot on the value map and there's a destroyable next to it,
        # kill (then map is update 'oh no bomb!!' and run)

        # Basic Decision Making:
        """
        Strats:
        Stalk by default -> 'stalk';
        If there is ammo: go get it -> 'pickup';
        If there is bomb: 'retreat'; 
        """

        # If you're in the blast tiles, do RETREAT
        if game_state['player_pos'] in game_state['hazard_zones']: # Both tuples (well, hazard zones is a list of tuples)
            print('HOLY RUN FOR YOUR LIFE YOU ARE GONNA GET RAILED')
            print("player pos type", type(game_state['player_pos']), "hazard type", type(game_state['hazard_zones'][0]))
            return 'basic_avoid'

        # # Basic Decision Making
        # # Pickup if ammo, stalk if none on map.
        # if len(game_state['pickup_list']) != 0:  # "Any pickups on the map?"
        #     print('me gusta I smell some pickups')
        #     return 'pickup'

        else:
            return 'stalk'
