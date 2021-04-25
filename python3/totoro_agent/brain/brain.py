"""
Tracks the game state and decides on next strategy to execute
"""

from .bomb_tracker import BombTracker
from .enemy_tracker import EnemyTracker
from .map_tracker import MapTracker
from .pickup_tracker import PickupTracker
from ..utils.util_functions import get_blast_zone

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

        # TODO Make decisions in terms on what strategy to do next Return string 

        # Highest Prio (base state): Collect + Stay away from immediate danger (fire + potential blast zones)
        # 2nd highest Destroy walls
        # --> If possible; KILL.

        #For destroy strats:
        # -> If it's at the highest spot on the value map and there's a destroyable next to it,
        #kill (then map is update 'oh no bomb!!' and run)

        """Strats:
        Stalk by default -> 'stalk';
        If there is ammo: go get it -> 'pickup';
        If there is bomb: 'retreat';
        # If 
        #"""
                # Will need something to check if in potential blast zone (from, enemy bombs), then retreat
        #

        ### Basic Decision Making

        # If you're in the blast tiles, do RETREAT
        for bomb in game_state['enemy_active_bombs']: # Bomb is a dict
            bomb_loc = bomb['coord'] 
            potential_blast_tiles = get_blast_zone(bomb_loc, bomb['blast_diameter'], game_state['entities'], game_state['world'])
            print('bomb loc', bomb_loc, 'blast tiles:', potential_blast_tiles, 'player', game_state['player_pos'])

            if tuple(game_state['player_pos']) in potential_blast_tiles:
                print('HOLY RUN FOR YOUR LIFE YOU ARE GONNA GET RAILED')
                return 'retreat'

        ### Basic Decision Making
        # Pickup if ammo, stalk if none on map.
        if len(game_state['pickup_list']) != 0: # "Any pickups on the map?"
            print('me gusta I smell some pickups')
            return 'pickup'

        else:
            return 'stalk'
