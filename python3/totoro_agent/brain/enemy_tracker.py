"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""

from ..utils.util_functions import get_value_map_object, get_surrounding_empty_tiles, get_world_dimension, get_surrounding_tiles, death_trap

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
        tick = game_state['tick']

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

        # Is the enemy immediately trapped?
        # Hard-coding immediate trap (can put in a strategy later)
        ## Check if enemy can't move: ->check if player can place a bomb that attacks enemy: -> do it.
        world = game_state['world']
        entities = game_state['entities']
        game_state['enemy_immediate_trapped'] = death_trap(game_state['enemy_pos'], world, entities)
        # world = game_state['world']
        # world_width, world_height = get_world_dimension(world)

        # # Return any tiles that are empty around enemy
        # enemy_surrounding_tiles = get_surrounding_tiles(game_state['enemy_pos'], world_width, world_height)
        # enemy_surrounding_empty_tiles = get_surrounding_empty_tiles(game_state['enemy_pos'], world, game_state['entities']) + (player_x, player_y) # Include player 
        # print("Length of enem surrounding empty tiles: ",  len(enemy_surrounding_empty_tiles))
        
        # if len(enemy_surrounding_empty_tiles) == 0: # Dude can't move. Technically, this 'immediate trapped' isn't the real value. It's actually trapped AND player is one of the tiles.
        #     #check if our player is in one of the tiles: -> 
        #     if game_state['player_pos'] in enemy_surrounding_tiles:
        #         game_state['enemy_immediate_trapped'] = True
        

