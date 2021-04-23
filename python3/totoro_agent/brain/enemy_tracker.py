"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""


class EnemyTracker:
	def __init__(self):
		#Enemy Tracker. Using enemy_ammo etc. even though it's THIS GUYS AMMO. we're not doubling reverse card. Enemy is OUR enemy. Global english, not relative.
		# Nothing to init because there's no reason to keep track of any objects over time (we just yoink it from the game_state).
		pass
	def update(self, game_state):

		### US THE HOMEBOIS ###
		self.player_id = str(game_state["connection"]["agent_number"])

		game_state['player_id'] = self.player_id
		game_state['player_id'] = game_state["agent_state"][self.player_id]["inventory"]["bombs"]
		game_state['player_pos'] = game_state["agent_state"][self.player_id]["coordinates"]
		game_state['player_health']  = game_state["agent_state"][self.player_id]["hp"]
		game_state['player_diameter']  = game_state["agent_state"][self.player_id]["blast_diameter"] # girthy boi
		game_state['player_invulnerable_until'] = game_state['agent_state'][self.player_id]['invulnerability'] # INCLUSIVE -> Vulnerable @ tick + 1 




		### ENEMY ###
		#############
		self.enemy_id = str((game_state["connection"]["agent_number"]+1)%2) 

		game_state['enemy_id'] = str(game_state["connection"]["agent_number"])
		game_state['enemy_id'] = game_state["agent_state"][self.enemy_id]["inventory"]["bombs"]
		game_state['enemy_pos'] = game_state["agent_state"][self.enemy_id]["coordinates"]
		game_state['enemy_health']  = game_state["agent_state"][self.enemy_id]["hp"]
		game_state['enemy_diameter']  = game_state["agent_state"][self.enemy_id]["blast_diameter"] # girthy boi
		game_state['enemy_invulnerable_until'] = game_state['agent_state'][self.enemy_id]['invulnerability'] # INCLUSIVE -> Vulnerable @ tick + 1 
#	is_invulnerable = #got hit or some shit in the past 5 ticks.? / set the ticks to when he is able to be hit again (similar to the website agent stats)

		pass