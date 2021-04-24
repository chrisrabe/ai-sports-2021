"""
Used for tracking lifecycle of bombs and explosion areas
"""

from ..utils.util_functions import get_blast_zone

class BombTracker:
    def __init__(self):
        self.bombs = []
        self.own_id = None
        self.enemy_id = None

    def update(self, game_state):
        # TODO Will
        # Get own and enemy id
        self.own_id = str(game_state['connection']['agent_number'])
        self.enemy_id = str(1 - int(own_id))
        own_active_bombs = []
        enemy_active_bombs = []

        # Get game entities
        entities = game_state['entities']

        # Get active bombs
        for entity in entities:
            if entity['owner'] == self.own_id and entity['type'] == 'b':
                own_active_bombs.append([entity['x'], entity['y']])
            elif entity['owner'] == self.enemy_id and entity['type'] == 'b':
                enemy_active_bombs.append([entity['x'], entity['y']])
            else:
                pass
            
        # Get bomb coordinates
        

        # Code this on Saturday
        # bombs and their lifecycle
        # Also keep track of bombs that have been recently exploded

        # our bombs
        # enemy bombs
       
        # future blast areas
        pass
