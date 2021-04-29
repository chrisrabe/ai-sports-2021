"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""

from ..utils.util_functions import get_value_map_object, get_surrounding_empty_tiles, get_world_dimension, \
    get_surrounding_tiles, dummy_bomb, get_blast_zone
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



        ###### Trapping Detection #####
        world = game_state['world']
        entities = game_state['entities']
        game_state['enemy_immediate_trapped'] = False
        game_state['enemy_onestep_trapped'] = False
        world = game_state['world']
        world_width, world_height = get_world_dimension(world)

        # # Return any tiles that are empty around enemy
        enemy_surrounding_tiles = get_surrounding_tiles(game_state['enemy_pos'], world_width, world_height)
        enemy_surrounding_empty_tiles = get_surrounding_empty_tiles(game_state['enemy_pos'], world, entities, ignore_player = False) # Needs to Include us 
        if game_state['player_pos'] in enemy_surrounding_empty_tiles: 
            enemy_surrounding_empty_tiles.remove(game_state['player_pos']) # Remove player pos from surrounding empty (why is he in there lol)
        if len(enemy_surrounding_empty_tiles) == 0:  # Dude can't move. Technically, this 'immediate trapped' isn't the real value. It's actually trapped AND player is one of the tiles.
            # check if our player is in one of the tiles: ->
            if game_state['player_pos'] in enemy_surrounding_tiles:  # Make sure
                game_state['enemy_immediate_trapped'] = True

        ###### Extended trapping detection ######
        # Dummy bomb to see if the enemy would be trapped (for 1 move: Initial + 1 move)
        virtual_bomb = dummy_bomb(game_state['player_pos'], game_state['player_diameter'])
        blast_zone = get_blast_zone(virtual_bomb['coord'], virtual_bomb['blast_diameter'], entities, world)
        if game_state['enemy_pos'] in blast_zone:
            check =  all(item in blast_zone for item in enemy_surrounding_empty_tiles) # checks if list one contains all elements of list 2
            if check:
                game_state['enemy_onestep_trapped'] = True

        # Removes player from enemy surround tiles
        if game_state['player_pos'] in enemy_surrounding_empty_tiles:
            self.stare_contest_duration += 1
            if self.stare_contest_duration == MAX_STARE_CONTEST_DURATION:
                game_state['tell_enemy_gtfo'] = True
            enemy_surrounding_empty_tiles.remove(
                game_state['player_pos'])  # Remove player pos from surround (why is he in there lol)
        else:
            self.stare_contest_duration = 0  # reset

        print("Player pos:", game_state['enemy_pos'], "Length of enem surrounding empty tiles: ",
              len(enemy_surrounding_empty_tiles), enemy_surrounding_empty_tiles,
              print(len(enemy_surrounding_empty_tiles) == 0))
