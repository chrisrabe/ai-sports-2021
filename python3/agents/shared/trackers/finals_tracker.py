from ..utils.constants import ENTITIES
from ..utils.util_functions import is_dangerous, get_entity_coords, get_blast_zone, get_surrounding_tiles, \
    get_world_dimension, get_safe_tiles, get_shortest_path, death_trap, get_surrounding_empty_tiles, get_empty_tiles, get_num_escape_paths


class FinalsTracker:
    """
    Tracker optimised for the finals
    """

    def update(self, game_state: dict):
        player_id = str(game_state["connection"]["agent_number"])
        enemy_id = str(1 - int(player_id))
        player_state = game_state["agent_state"][player_id]
        enemy_state = game_state['agent_state'][enemy_id]
        tick = game_state['tick']

        player_pos = tuple(player_state["coordinates"])
        enemy_pos = tuple(enemy_state["coordinates"])

        world_width, world_height = get_world_dimension(game_state['world'])
        enemy_surrounding_tiles = get_surrounding_tiles(enemy_pos, world_width, world_height)

        # Flatten agent states

        game_state['player_id'] = player_id
        game_state['player_pos'] = player_pos
        game_state['player_inv_bombs'] = player_state["inventory"]["bombs"]
        game_state['player_health'] = player_state["hp"]
        game_state['player_diameter'] = player_state["blast_diameter"]  # girthy boi
        game_state['player_is_invulnerable'] = (player_state['invulnerability'] - tick) > 1

        game_state['enemy_id'] = enemy_id
        game_state['enemy_inv_bombs'] = enemy_state["inventory"]["bombs"]
        game_state['enemy_pos'] = enemy_pos
        game_state['enemy_health'] = enemy_state["hp"]
        game_state['enemy_diameter'] = enemy_state["blast_diameter"]  # girthy boi
        game_state['enemy_is_invulnerable'] = (enemy_state['invulnerability'] - tick) > 1
        game_state['enemy_near_player'] = player_pos in enemy_surrounding_tiles

        # Append player and enemies into game state entities
        game_state['entities'].append({
            'x': player_pos[0],
            'y': player_pos[1],
            'type': ENTITIES['player']
        })
        game_state['entities'].append({
            'x': enemy_pos[0],
            'y': enemy_pos[1],
            'type': ENTITIES['enemy']
        })

        # pickups
        ammo_list = []
        powerup_list = []
        pickup_list = []

        # map blocks
        destroyable_blocks = []
        wall_blocks = []
        blast_blocks = []

        # bombs
        player_on_bomb = False
        enemy_on_bomb = False
        enemy_near_bomb = False
        own_bombs = []
        player_hazards = []
        detonation_zone = []
        all_hazards = []

        entities = game_state['entities']

        # Loop through each entity once and do evaluation on each item type
        for entity in entities:
            entity_type = entity['type']
            if entity_type == ENTITIES['blast']:
                coord = get_entity_coords(entity)
                all_hazards.append(coord)
                player_hazards.append(coord)
                wall_blocks.append(entity)
                blast_blocks.append(entity)
            elif entity_type == ENTITIES['ore'] or entity_type == ENTITIES['wood']:
                destroyable_blocks.append(entity)
            elif entity_type == ENTITIES['metal']:
                wall_blocks.append(entity)
            elif entity_type == ENTITIES['ammo']:
                if is_dangerous(entity, player_pos, enemy_pos, game_state['world'], entities):
                    continue  # filter dangerous pickups
                ammo_list.append(entity)
                pickup_list.append(entity)
            elif entity_type == ENTITIES['powerup']:
                if is_dangerous(entity, player_pos, enemy_pos, game_state['world'], entities):
                    continue  # filter dangerous pickups
                powerup_list.append(entity)
                pickup_list.append(entity)
            elif entity_type == ENTITIES['bomb']:
                bomb_coords = get_entity_coords(entity)
                bomb = {
                    'coord': bomb_coords,
                    'expires': entity['expires'],
                    'blast_diameter': entity['blast_diameter']
                }
                blast_zone = get_blast_zone(bomb_coords, bomb['blast_diameter'], entities, game_state['world'])
                if entity['owner'] == int(player_id):
                    if bomb_coords == player_pos:
                        player_on_bomb = True
                    own_bombs.append(bomb)
                else:
                    if bomb_coords == enemy_pos:
                        enemy_on_bomb = True
                    elif bomb_coords in enemy_surrounding_tiles:
                        enemy_near_bomb = True
                # append blast zone
                for tile in blast_zone:
                    all_hazards.append(tile)
                    if entity['owner'] == int(player_id):
                        ttl = bomb['expires'] - game_state['tick']
                        if ttl <= (game_state['player_diameter'] // 2) + 1:
                            player_hazards.append(tile)
                        detonation_zone.append(tile)
                    else:
                        player_hazards.append(tile)

        game_state['safe_zones'] = get_safe_tiles(all_hazards, game_state['world'], game_state['entities'])
        game_state['player_on_bomb'] = player_on_bomb
        game_state['enemy_on_bomb'] = enemy_on_bomb
        game_state['enemy_near_bomb'] = enemy_near_bomb
        game_state['ammo_list'] = ammo_list
        game_state['powerup_list'] = powerup_list
        game_state['pickup_list'] = pickup_list
        game_state['own_active_bombs'] = own_bombs
        game_state['hazard_zones'] = player_hazards
        game_state['detonation_zones'] = detonation_zone
        game_state['all_hazard_zones'] = all_hazards
        game_state['wall_blocks'] = wall_blocks
        game_state['destroyable_blocks'] = destroyable_blocks
        game_state['blast_blocks'] = blast_blocks

    def update_path(self, game_state: dict):
        path = get_shortest_path(game_state['player_pos'], game_state['enemy_pos'], game_state['world'],
                                 game_state['entities'])
        game_state['clear_path_to_enemy'] = path is not None

    def update_trap(self, game_state: dict):
        game_state['enemy_immediate_trapped'] = death_trap(game_state['enemy_pos'], game_state['world'],
                                                           game_state['entities']) and game_state['enemy_near_player']

    def update_onestep(self, game_state: dict):
        """
        Onestep trapping: Returns true if there is an escape path, and placing a bomb at 
        player position will mean the enemy can't escape its blast zone in the next tick
        """
        
        player_pos = game_state['player_pos']
        player_diameter = game_state['player_diameter']
        entities = game_state['entities']
        world = game_state['world']
        num_escape = get_num_escape_paths(player_pos, player_pos, player_diameter, entities, world)
        if num_escape <= 1:
            game_state['enemy_onestep_trapped'] = False  # not worth it trapping yourself
            return
        enemy_pos = game_state['enemy_pos']
        virt_blast_zone = get_blast_zone(player_pos, player_diameter, entities, world)
        enemy_empty_neighbours = get_surrounding_empty_tiles(enemy_pos, world, entities, False)
        if enemy_empty_neighbours:
            game_state['enemy_onestep_trapped'] = all(item in virt_blast_zone for item in enemy_empty_neighbours)
        else:
            game_state['enemy_onestep_trapped'] = False

    def update_enemy_free_space(self, game_state: dict):
        """
        Return number of empty tiles in enemy surrounding area (as proxy of its future movement limitation)
        """
        entities = game_state['entities']
        world = game_state['world']
        enemy_pos = game_state['enemy_pos']

        enemy_empty_neighbours = get_surrounding_empty_tiles(enemy_pos, world, entities, False)
        enemy_empty_area = []
        for empty_tile in enemy_empty_neighbours:
            empty_surround = get_surrounding_empty_tiles(empty_tile, world, entities, False)
            empty_surround_uniques = [tile for tile in empty_surround if tile not in enemy_empty_area]
            for tile in empty_surround_uniques:
                enemy_empty_area.append(tile)
        
        game_state['enemy_free_space'] = len(enemy_empty_area)