"""
Used to track all information about the ores (their HP, etc)
"""
from ..utils.util_functions import get_world_dimension 

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
        for a in game_state['entities']:
        	if a['type']=="a":
        		x = a['x']
        		y = a['y']
        		# ammo_list.append(list((x,y)))
        		ammo_list.append([x,y])
        	if a['type']=="bp":
        		x = a['x']
        		y = a['y']
        		# powerup_list.append(list((x,y)))
        		powerup_list.append([x,y])

        # Player A and B's blast diameter updated tick by tick.'

        # Gets the map width and height.
        map_width, map_height = get_world_dimension(game_state['world'])

        own_id = int(game_state['connection']['agent_number'])
        enemy_id = int(1 - int(own_id))

        # Changes pickup priority depending on 
        pickup_priority = "ammo_powerup"
        if own_id >= max(map_width, map_height):
        	pickup_priority = "ammo"

        # Setting the game_state parameters. 
        game_state['ammo_list'] = ammo_list
        game_state['powerup_list'] = powerup_list
        game_state['pickup_priority'] = pickup_priority