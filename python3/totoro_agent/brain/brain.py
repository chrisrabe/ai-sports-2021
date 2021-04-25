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
        self.enemy_tracker.update(game_state)
        self.bomb_tracker.update(game_state)
        self.map_tracker.update(game_state)
        self.pickup_tracker.update(game_state)

        # enemy is trapped

        # TODO Make decisions in terms on what strategy to do next: Return string 

		# Highest Prio (base state): Collect + Stay away from immediate danger (fire + potential blast zones)
		# 2nd highest Destroy walls
		# --> If possible; KILL.

		#For destroy strats:
		# -> If it's at the highest spot on the value map and there's a destroyable next to it,
		#kill (then map is update 'oh no bomb!!' and run)


		"""By default: 
		Stalk. 
		If ammo on map, Pickup"""

        return "stalk"
