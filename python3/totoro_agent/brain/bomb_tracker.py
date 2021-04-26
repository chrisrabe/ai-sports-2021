"""
Used for tracking lifecycle of bombs and explosion areas
"""
import math

from ..utils.util_functions import get_blast_zone, get_safe_tiles, get_reachable_tiles, get_surrounding_tiles, get_world_dimension
from ..utils.constants import ENTITIES


class BombTracker:
    def __init__(self):
        self.bombs = []

    def update(self, game_state):
        """ Adds bombs to game_state for player, enemy, and total. game_state['enemy_active_bombs'] is a list of dictionaries."""
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
        world_width, world_height = get_world_dimension(world)

        surrounding_enemy_tiles = get_surrounding_tiles(enemy_pos, world_width, world_height)

        # Get active bombs - coordinates, expiry, blast diameter
        for entity in entities:
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
        hazards = []
        for bomb in danger_bombs:
            blast_zone = get_blast_zone(bomb['coord'], bomb['blast_diameter'], entities, world)
            hazards += blast_zone

        # potential detonation zones
        enemy_hazards = []
        for bomb in own_active_bombs:
            blast_zone = get_blast_zone(bomb['coord'], bomb['blast_diameter'], entities, world)
            enemy_hazards += blast_zone

        safe_zones = get_safe_tiles(hazards + enemy_hazards, world, entities)
        reachable_safe = get_reachable_tiles(player_pos, safe_zones, world, entities)

        # Save values into game state
        game_state['own_active_bombs'] = own_active_bombs
        game_state['enemy_active_bombs'] = enemy_active_bombs
        game_state['all_active_bombs'] = all_active_bombs
        game_state['hazard_zones'] = hazards
        game_state['player_on_bomb'] = player_on_bomb
        game_state['enemy_on_bomb'] = enemy_on_bomb
        game_state['detonation_zones'] = enemy_hazards
        game_state['safe_zones'] = reachable_safe
        game_state['enemy_near_bomb'] = enemy_near_bomb
        game_state['all_hazard_zones'] = hazards + enemy_hazards

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
