from typing import List
import random
from . import strategy
from ..utils.util_functions import get_shortest_path, manhattan_distance, get_path_action_seq, get_blast_zone, get_nearest_tile
from ..utils.constants import ACTIONS


class PickupStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        # if power up priority is ammo_powerup
        # go for closest pickup powerup
        # else
        # go for closest ammo
        player_pos = tuple(game_state['player_pos'])
        ammo_list = game_state['ammo_list']
        powerup_list = game_state['powerup_list']
        pickup_priority = game_state['pickup_priority']
        world = game_state['world']
        entities = game_state['entities']

        if pickup_priority == "ammo_powerup":
            if ammo_list:
                global ammo_choice
                ammo_choice = random.choice(ammo_list[:])
            if powerup_list:
                global powerup_choice
                powerup_choice = random.choice(powerup_list[:])

            final_choice = random.choice(ammo_choice, powerup_choice)
            global path
            path = get_shortest_path(player_pos, final_choice, world, entities)
            print(path)
        elif pickup_priority == "ammo":
            if ammo_list:
                
                ammo_choice = random.choice(ammo_list[:])
                
                path = get_shortest_path(player_pos, ammo_choice, world, entities)
            print(path)

        return get_path_action_seq(player_pos, path)
