from ..utils.constants import ENTITIES
from ..utils.util_functions import is_dangerous, get_entity_coords, get_blast_zone, get_surrounding_tiles, \
    get_world_dimension


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
                if entity['owner'] == player_id:
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
                    if entity['owner'] == player_id:
                        ttl = bomb['expires'] - game_state['tick']
                        if ttl <= (game_state['player_diameter'] // 2) + 1:
                            player_hazards.append(tile)
                        detonation_zone.append(tile)
                    else:
                        player_hazards.append(tile)

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

