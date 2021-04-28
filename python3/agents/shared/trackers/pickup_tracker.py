"""
Used to track all information about the ores (their HP, etc)
"""
from ..utils.constants import ENTITIES


class PickupTracker:
    def __init__(self):
        self.ammo = []

    def update(self, game_state):
        # TODO gaurav
        # powerup - stop picking up powerups as soon as  diameter reaches double map size
        # Couldnt do the above as we didnt have picking up functionality, and I didn't get 
        # Why we needed to do it if it reached double map size. Will do tomorrow. 
        # ammo

        # Making empty lists for ammo and powerups. Will modify tick by tick.
        ammo_list = []
        powerup_list = []

        # For loops for adding stuff to ammo_list and powerup_list 
        for entity in game_state['entities']:
            if entity['type'] == ENTITIES['ammo']:
                x = entity['x']
                y = entity['y']

                ammo_list.append((x, y))
            if entity['type'] == ENTITIES['powerup']:
                x = entity['x']
                y = entity['y']

                powerup_list.append((x, y))

        # Player A and B's blast diameter updated tick by tick.'

        # Setting the game_state parameters.
        game_state['ammo_list'] = ammo_list
        game_state['powerup_list'] = powerup_list
        game_state['pickup_list'] = ammo_list + powerup_list
