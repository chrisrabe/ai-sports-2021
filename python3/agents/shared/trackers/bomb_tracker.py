"""
Used for tracking lifecycle of bombs and explosion areas
"""

from ..utils.util_functions import get_blast_zone, get_safe_tiles, get_surrounding_tiles, get_world_dimension, \
    get_surrounding_empty_tiles, dummy_bomb, get_shortest_path, get_nearest_tile, get_reachable_tiles
from ..utils.constants import ENTITIES


class BombTracker:
    def __init__(self):
        self.enemy_reachable_tiles = 6
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
            # Adds blast tiles to hazards so he doesn't walk on them. He CANNOT walk on them (from shortest paths)
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
                    if ttl <= (game_state['player_diameter'] // 2) + 1:  # it's about to explode! GTFO!
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
        game_state['zoning'] = False

        # # Return any tiles that are empty around enemy
        enemy_surrounding_tiles = get_surrounding_tiles(game_state['enemy_pos'], world_width, world_height)
        enemy_surrounding_empty_tiles = get_surrounding_empty_tiles(game_state['enemy_pos'], world, entities,
                                                                    ignore_player=False)  # Needs to Include us
        

        if len(enemy_surrounding_empty_tiles) == 0:  # Dude can't move. Technically, this 'immediate trapped' isn't the real value. It's actually trapped AND player is one of the tiles.
            # check if our player is in one of the tiles: ->
            if game_state['player_pos'] in enemy_surrounding_tiles:  # Make sure
                game_state['enemy_immediate_trapped'] = True

        ###### Extended trapping detection ######
        # Dummy bomb to see if the enemy would be trapped (for 1 move: Initial + 1 move)
        virtual_bomb = dummy_bomb(game_state['player_pos'], game_state['player_diameter'])
        blast_zone_virt = get_blast_zone(virtual_bomb['coord'], virtual_bomb['blast_diameter'], entities, world)
        # if game_state['player_pos'] in enemy_surrounding_empty_tiles:
        #     enemy_surrounding_empty_tiles.remove(
        #         game_state['player_pos'])  # Remove player pos from surround (why is he in there lol)
        if game_state['enemy_pos'] in blast_zone_virt:
            check = all(item in blast_zone_virt for item in
                        enemy_surrounding_empty_tiles)  # checks if blast zone contains all elements of enemy surrounding tiles
            if check:
                game_state['enemy_onestep_trapped'] = True # Enemy can't move out of the way in the next tick

        ## Zoning:
        # If place a bomb here, check reachable tiles length < self.enemy_tiles
        # # If dummy bomb placed here;
        # enemy_reachable_tiles = get_reachable_tiles(enemy_pos,)
        # if len(enemy_reachable_tiles) < self.enemy_reachable_tiles:
        #     game_state['constrict'] = True
        if enemy_surrounding_empty_tiles in blast_zone_virt:
            game_state['zoning'] = True

        #Check if: The enemy surrounding empty tiles UP and (right or left) or DOWN and (right or left) in blast_zone: --> This means it'll  only work if he's 1 (x,y) away from us max.
        # place bomb 
        # Finds potential tiles to place our bombs that will kaboom the eney
        virt_bomb_on_enemy = dummy_bomb(enemy_pos, game_state['player_diameter'])
        potential_place_tiles = get_blast_zone(virt_bomb_on_enemy['coord'], virt_bomb_on_enemy['blast_diameter'], entities, world)
        reachable_tiles = get_reachable_tiles(player_pos, potential_place_tiles, world, entities, all_hazards)
        closest_bomb_tile = get_nearest_tile(player_pos, reachable_tiles)
        game_state['closest_bomb_tile'] = closest_bomb_tile
        # # Removes player from enemy surround tiles

        print("Player pos:", game_state['player_pos'], "Length of enem surrounding empty tiles: ",
              len(enemy_surrounding_empty_tiles), enemy_surrounding_empty_tiles,
              len(enemy_surrounding_empty_tiles) == 0, "\n Enemy pos:", enemy_pos, enemy_surrounding_tiles, get_surrounding_empty_tiles(enemy_pos, world, entities, False))

        # check if there's a clear path to the enemy
        path = get_shortest_path(game_state['player_pos'], game_state['enemy_pos'], world, entities)
        game_state['clear_path_to_enemy'] = path is not None


