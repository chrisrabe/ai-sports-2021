"""
Used for tracking lifecycle of bombs and explosion areas
"""

from ..utils.util_functions import get_blast_zone
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

        # Get game entities
        entities = game_state['entities']
        world = game_state['world']

        # Get active bombs - coordinates, expiry, blast diameter
        for entity in entities:
            if entity['type'] == ENTITIES['bomb']:
                bomb = {
                    'coord': [entity['x'], entity['y']],
                    'expires': entity['expires'],
                    'blast_diameter': entity['blast_diameter']
                }
                if entity['owner'] == own_id:
                    ttl = bomb['expires'] - game_state['tick']
                    if ttl - 1: # it's about to explode! GTFO!
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

        # Save values into game state
        game_state['own_active_bombs'] = own_active_bombs
        game_state['enemy_active_bombs'] = enemy_active_bombs
        game_state['all_active_bombs'] = all_active_bombs
        game_state['hazard_zones'] = hazards
