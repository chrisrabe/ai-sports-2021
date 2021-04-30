"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""

from ..utils.util_functions import get_value_map_object, get_surrounding_tiles, get_world_dimension
from ..utils.constants import MAX_STARE_CONTEST_DURATION


class EnemyTracker:
    def __init__(self):
        self.stare_contest_duration = 0

    def update(self, game_state):
        # US THE HOMEBOIS
        player_id = str(game_state["connection"]["agent_number"])
        player_state = game_state['agent_state'][player_id]
        tick = game_state['tick']

        game_state['tell_enemy_gtfo'] = False

        player_x, player_y = player_state["coordinates"]
        game_state['player_id'] = player_id
        game_state['player_inv_bombs'] = player_state["inventory"]["bombs"]
        game_state['player_pos'] = (player_x, player_y)
        game_state['player_health'] = player_state["hp"]
        game_state['player_diameter'] = player_state["blast_diameter"]  # girthy boi
        game_state['player_is_invulnerable'] = (player_state['invulnerability'] - tick) > 1

        # ENEMY
        enemy_id = str(1 - int(player_id))
        enemy_state = game_state['agent_state'][enemy_id]

        enemy_x, enemy_y = enemy_state["coordinates"]
        game_state['enemy_obj'] = get_value_map_object(enemy_x, enemy_y, 'enemy')
        game_state['enemy_id'] = enemy_id
        game_state['enemy_inv_bombs'] = enemy_state["inventory"]["bombs"]
        game_state['enemy_pos'] = (enemy_x, enemy_y)
        game_state['enemy_health'] = enemy_state["hp"]
        game_state['enemy_diameter'] = enemy_state["blast_diameter"]  # girthy boi
        game_state['enemy_is_invulnerable'] = (enemy_state['invulnerability'] - tick) > 1

        world_width, world_height = get_world_dimension(game_state['world'])
        player_neighbours = get_surrounding_tiles(game_state['player_pos'], world_width, world_height)

        if self.stare_contest_duration >= MAX_STARE_CONTEST_DURATION:
            game_state['tell_enemy_gtfo'] = True

        if game_state['enemy_pos'] in player_neighbours:
            self.stare_contest_duration += 1
        else:
            self.stare_contest_duration = 0  # reset
