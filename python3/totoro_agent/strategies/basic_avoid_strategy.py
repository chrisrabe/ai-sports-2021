from typing import List
from . import strategy

class BasicAvoidStrategy(strategy.Strategy):

    def execute(self, game_state: object) -> List[str]:
        """
        Execute the strategy
        If the player is in a hazard_zones tile:
        move to nearest tile that isn't in hazard_zones
        """

        path = None
        player_pos = (game_state['player_pos']) # Tuple
        hazard_zones = game_state['hazard_zones'] # List of tuples 

        # for tile in hazard_zones
        if player_pos in hazard_zones: # Checks if player is on hazard tile (potential blast zone)
            # Move to the nearest tile that isn't in the hazard_zone:

            # min value of manhattan distance of tiles?
            print("YOU'RE IN DANGER DUDE")
        

        # if path is None:
        # print("shat myself inside basic_avoid")
        # return [ACTIONS['none']]



        
            #print(type(player_pos), print(type_hazard_zones))

        # if ammo_list:
        #     reachable_ammo = get_reachable_tiles(player_pos, ammo_list, world, entities)
        #     nearest_ammo = get_nearest_tile(player_pos, reachable_ammo)
        #     path = get_shortest_path(player_pos, nearest_ammo, world, entities)
        # elif powerup_list:
        #     reachable_powerup = get_reachable_tiles(player_pos, powerup_list, world, entities)
        #     nearest_powerup = get_nearest_tile(player_pos, reachable_powerup)
        #     path = get_shortest_path(player_pos, nearest_powerup, world, entities)

        # if path is None:
        #     return [ACTIONS['none']]
        # else:
        #     return get_path_action_seq(player_pos, path)

        # pass
