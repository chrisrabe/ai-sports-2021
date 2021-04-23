"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""


class EnemyTracker:
	def __init__(self):
		#Enemy Tracker. Using enemy_ammo etc. even though it's THIS GUYS AMMO. we're not doubling reverse card. Enemy is OUR enemy. Global english, not relative.
		self.enemy_pos = [0, 0] 
		self.enemy_ammo = 3
		self.enemy_health = 3
		self.enemy_blast_radius = 2 # -> Not checking # of powerups, so just increase this by 1 whenever we pick up a powerup.
		self.enemy_invulnerable_until = 0 # Get better var name, number is inclusive.


	def update(self, game_state):
		# TODO Yuv
		self.player_id = game_state["connection"]["agent_number"]
		# own position
		# own health
		# own ammo
		# own diameter
		# own invulnerable (we don't worry about our own stuff -- this'll be easily reflected)


		self.enemy_id = not self.player_id # Could've just done 'not self.player_id' lol
		self.enemy_ammo = game_state["agent_state"][self.enemy_id]["inventory"]["bombs"]  
		self.enemy_pos = game_state["agent_state"][self.enemy_id]["coordinates"]
		self.enemy_health = game_state["agent_state"][self.enemy_id]["hp"]
		self.enemy_diameter = game_state["agent_state"][self.enemy_id]["blast_diameter"] # girthy boi
		self.enemy_invulnerable_until = game_state['agent_state'][self.enemy_id]['invulnerability'] # INCLUSIVE -> Vulnerable @ tick + 1 
	#	is_invulnerable = #got hit or some shit in the past 5 ticks.? / set the ticks to when he is able to be hit again (similar to the website agent stats)
	#
		# Shove them into game_state - Feels like there's a better way to do this but oops. Could also get rid of the above and just shove them in there.
		game_state.enemy_id = self.enemy_id 
		game_state.enemy_ammo = self.enemy_ammo 
		game_state.enemy_pos = self.enemy_pos
		game_state.enemy_health = self.enemy_health
		game_state.enemy_diameter = self.enemy_diameter
		game_state.enemy_invulnerable_until = self.enemy_diameter

		pass