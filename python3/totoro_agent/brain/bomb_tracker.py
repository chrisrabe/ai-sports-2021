"""
Used for tracking lifecycle of bombs and explosion areas
"""

# from ..utils.util_functions import get_blast_zone
from ..utils.constants import ENTITIES

class BombTracker:
    def __init__(self):
        self.bombs = []

    def update(self, game_state):
        # Get own and enemy id
        own_id = game_state['player_id']
        enemy_id = game_state['enemy_id']
        own_active_bombs = []
        enemy_active_bombs = []

        # Get game entities
        entities = game_state['entities']

        # Get active bombs
        for entity in entities:
            if entity['type'] == ENTITIES['bomb']:
                if entity['owner'] == own_id:
                    own_active_bombs.append(entity)
                elif entity['owner'] == enemy_id:
                    enemy_active_bombs.append(entity)

        # Save values into game state
        game_state['own_active_bombs'] = own_active_bombs
        game_state['enemy_active_bombs'] = enemy_active_bombs

        # Get bomb coordinates
        

        # Code this on Saturday
        # bombs and their lifecycle
        # Also keep track of bombs that have been recently exploded

        # our bombs
        # enemy bombs
       
        # future blast areas
