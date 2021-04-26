"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""

from ..utils.util_functions import get_value_map_object

class EnemyTracker:
    def __init__(self):
        # Enemy Tracker. Using enemy_ammo etc. even though it's THIS GUYS AMMO. we're not doubling reverse card. Enemy
        # is OUR enemy. Global english, not relative. Nothing to init because there's no reason to keep track of any
        # objects over time (we just yoink it from the game_state).
        pass

    def update(self, game_state):
        # US THE HOMEBOIS
        player_id = str(game_state["connection"]["agent_number"])
        player_state = game_state['agent_state'][player_id]

        player_x, player_y = player_state["coordinates"]
        game_state['player_id'] = player_id
        game_state['player_inv_bombs'] = player_state["inventory"]["bombs"]
        game_state['player_pos'] = (player_x, player_y)
        game_state['player_health'] = player_state["hp"]
        game_state['player_diameter'] = player_state["blast_diameter"]  # girthy boi
        game_state['player_invulnerable_until'] = player_state['invulnerability']  # INCLUSIVE -> Vulnerable @ tick + 1

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
        game_state['enemy_invulnerable_until'] = enemy_state['invulnerability']  # INCLUSIVE -> Vulnerable @ tick + 1
        # is_invulnerable = #got hit or some shit in the past 5 ticks.? / set the ticks to when he is able to be hit
    # again (similar to the website agent stats)
