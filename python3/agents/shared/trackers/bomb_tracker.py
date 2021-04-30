"""
Used for tracking lifecycle of bombs and explosion areas
"""
import math

from ..utils.util_functions import get_blast_zone, get_safe_tiles, get_surrounding_tiles, get_world_dimension, get_surrounding_empty_tiles, dummy_bomb, get_shortest_path
from ..utils.constants import ENTITIES

class BombTracker:
    def __init__(self):
        self.bombs = []

    def update(self, game_state):
        """ 
        Adds bombs to game_state for player, enemy, and total. game_state['enemy_active_bombs'] is a list of dictionaries.
        game_state['hazard_zones'] provides a list of tiles that are dangerous (blast zone for danger bombs)
        """
        # Get own and enemy id
        own_id = int(game_state['player_id'])
        enemy_id = int(game_state['enemy_id'])
        own_active_bombs = []
        enemy_active_bombs = []
        all_active_bombs = []
        danger_bombs = []

        player_pos = game_state['player_pos']
        enemy_pos = game_state['enemy_pos']
        enemy_on_bomb = False
        player_on_bomb = False
        enemy_near_bomb = False

        # Get game entities
        entities = game_state['entities']
        world = game_state['world']
        hazards = []
        world_width, world_height = get_world_dimension(world)

        surrounding_enemy_tiles = get_surrounding_tiles(enemy_pos, world_width, world_height)

        # Get active bombs - coordinates, expiry, blast diameter
        for entity in entities:
            #Adds blast tiles to hazards so he doesn't walk on them. He CANNOT walk on them (from shortest paths)
            if entity['type'] == ENTITIES['blast']:
                hazards.append((entity['x'], entity['y']))

            if entity['type'] == ENTITIES['bomb']:
                bomb = {
                    'coord': (entity['x'], entity['y']),
                    'expires': entity['expires'],
                    'blast_diameter': entity['blast_diameter']
                }

                if bomb['coord'] == player_pos:
                    player_on_bomb = True
                    danger_bombs.append(bomb)
                elif bomb['coord'] == enemy_pos:
                    enemy_on_bomb = True
                elif bomb['coord'] in surrounding_enemy_tiles:
                    enemy_near_bomb = True

                if entity['owner'] == own_id:
                    ttl = bomb['expires'] - game_state['tick']
                    if ttl == (math.floor(game_state['player_diameter'] / 2) + 1):  # it's about to explode! GTFO!
                        danger_bombs.append(bomb)
                    own_active_bombs.append(bomb)
                elif entity['owner'] == enemy_id:
                    danger_bombs.append(bomb)
                    enemy_active_bombs.append(bomb)
                all_active_bombs.append(bomb)


        # calculate hazard zones
        for bomb in danger_bombs:
            blast_zone = get_blast_zone(bomb['coord'], bomb['blast_diameter'], entities, world)
            hazards += blast_zone
        # if len(game_state['blast_blocks']) != 0:

        #     hazards.append(game_state['blast_blocks'])

        # potential detonation zones
        enemy_hazards = []
        for bomb in own_active_bombs:
            blast_zone = get_blast_zone(bomb['coord'], bomb['blast_diameter'], entities, world)
            enemy_hazards += blast_zone

        all_hazards = hazards + enemy_hazards
        safe_zones = get_safe_tiles(all_hazards, world, entities)

        # Save values into game state
        game_state['own_active_bombs'] = own_active_bombs
        game_state['enemy_active_bombs'] = enemy_active_bombs
        game_state['all_active_bombs'] = all_active_bombs
        game_state['hazard_zones'] = hazards
        game_state['player_on_bomb'] = player_on_bomb
        game_state['enemy_on_bomb'] = enemy_on_bomb
        game_state['detonation_zones'] = enemy_hazards
        game_state['safe_zones'] = safe_zones
        game_state['enemy_near_bomb'] = enemy_near_bomb
        game_state['all_hazard_zones'] = all_hazards

        # append new entities (used for kill strats)
        player_x, player_y = player_pos
        if player_on_bomb:
            game_state['entities'].append({
                'x': player_x,
                'y': player_y,
                'type': ENTITIES['player_on_bomb']
            })
        else:
            game_state['entities'].append({
                'x': player_x,
                'y': player_y,
                'type': ENTITIES['player']
            })

        enemy_x, enemy_y = enemy_pos
        if enemy_on_bomb:
            game_state['entities'].append({
                'x': enemy_x,
                'y': enemy_y,
                'type': ENTITIES['enemy_on_bomb']
            })
        else:
            game_state['entities'].append({
                'x': enemy_x,
                'y': enemy_y,
                'type': ENTITIES['enemy']
            })

      ###### Trapping Detection #####
        game_state['enemy_immediate_trapped'] = False
        game_state['enemy_onestep_trapped'] = False

        # # Return any tiles that are empty around enemy
        enemy_surrounding_tiles = get_surrounding_tiles(game_state['enemy_pos'], world_width, world_height)
        enemy_surrounding_empty_tiles = get_surrounding_empty_tiles(game_state['enemy_pos'], world, entities, ignore_player = False) # Needs to Include us 
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

        # check if there's a clear path to the enemy
        path = get_shortest_path(game_state['player_pos'], game_state['enemy_pos'], world, entities)
        game_state['clear_path_to_enemy'] = path is not None
