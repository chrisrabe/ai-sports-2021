"""
Used to track all information about the ores (their HP, etc)
"""


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
        		ammo_list.append((x,y))

        for b in game_state['entities']:
        	if b['type']=="bp":
        		x = b['x']
        		y = b['y']
        		powerup_list.append((x,y))

        # Player A and B's blast diameter updated tick by tick.'
        player_a_wizard_diameter = game_state['agent_state']['0']['blast_diameter']
        player_b_knight_diameter = game_state['agent_state']['1']['blast_diameter']
        
        # Gets the map width and height.
        map_width = game_state['world']['width']
        map_height = game_state['world']['height']

        # Checks if diameter of either playerA or playerB is greater than diameter. 
        # If it is, it sets a variable to True, and if not False, and prints it to console.
        if player_a_wizard_diameter > map_width or player_a_wizard_diameter > map_height:
        	playerA_greater = True
        	print("Player A's diameter is greater than Map.")
        else:
        	playerA_greater = False
        	# print("Player A's diameter is smaller than the map.")

        if player_b_knight_diameter > map_width or player_b_knight_diameter > map_height:
        	playerB_greater = True
        	print("Player B's diameter is greater than Map.")
        else:
        	playerB_greater = False
        	# print("Player B's diameter is smaller than the map.")


        # Print statements that print the above stuff to the console. 
        # Uncomment the top two for seeing stuff about diameters and the else statements to see more.

        # print(f"Wizard or PlayerA's diameter is: {player_a_wizard_diameter}\n")
        # print(f"Knight or PlayerB's diameter is: {player_b_knight_diameter}\n")
        


        print(f"There is ammo at: {ammo_list}\n")
        print(f"There is powerups at: {powerup_list}\n")

