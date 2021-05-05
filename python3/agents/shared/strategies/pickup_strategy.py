from typing import List
from . import strategy
from ..utils.util_functions import get_shortest_path, get_path_action_seq, get_nearest_tile, get_reachable_tiles, \
    move_results_in_ouchie, manhattan_distance, convert_entities_to_coords, player_has_control, get_articulation_points
from ..utils.constants import ACTIONS


class PickupStrategy(strategy.Strategy):

    def update(self, game_state: dict):
        game_state['player_has_control'] = player_has_control(game_state['player_pos'], game_state['enemy_pos'], game_state['world'])
        game_state['dangerous_pickups'] = []  # no need to check this for finals
        game_state['ammo_list'] = convert_entities_to_coords(game_state['ammo_list'])
        game_state['powerup_list'] = convert_entities_to_coords(game_state['powerup_list'])

    def execute(self, game_state: object) -> List[str]:
        path = None
        player_pos = tuple(game_state['player_pos'])
        ammo_list = game_state['ammo_list']
        powerup_list = game_state['powerup_list']
        world = game_state['world']
        entities = game_state['entities']

        if not game_state['player_on_bomb'] and game_state['player_inv_bombs'] > 0 and game_state['player_has_control'] and game_state['enemy_near_player']:
            pinch_points = get_articulation_points(player_pos, world, entities)
            if player_pos in pinch_points:
                return [ACTIONS['bomb']]

        # Removes any ammo that is dangerous from pathfinding --> If enemy is too close, don't bother getting it.
        for element in game_state['dangerous_pickups']:
            if manhattan_distance(player_pos, game_state['enemy_pos']) < 2:
                if element in powerup_list:
                    powerup_list.remove(element)

                if element in ammo_list:
                    ammo_list.remove(element)

        if ammo_list:
            reachable_ammo = get_reachable_tiles(player_pos, ammo_list, world, entities, game_state['hazard_zones'])
            nearest_ammo = get_nearest_tile(player_pos, reachable_ammo)
            path = get_shortest_path(player_pos, nearest_ammo, world, entities, game_state['hazard_zones'],
                                     game_state['player_is_invulnerable'])
        elif powerup_list:
            reachable_powerup = get_reachable_tiles(player_pos, powerup_list, world, entities)
            nearest_powerup = get_nearest_tile(player_pos, reachable_powerup)
            path = get_shortest_path(player_pos, nearest_powerup, world, entities, game_state['hazard_zones'],
                                     game_state['player_is_invulnerable'])

        # make it more responsive
        action_seq = get_path_action_seq(player_pos, path)
        if len(action_seq) > 0:
            next_action = action_seq.pop(0)
            if move_results_in_ouchie(player_pos, next_action, game_state['hazard_zones']):
                return [ACTIONS['none']]  # do nothing
            else:
                return [next_action]
        else:
            return action_seq
