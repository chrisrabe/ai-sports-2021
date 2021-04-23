"""
Used to track all information about the enemy such as its health,
ammo, etc.
"""


class EnemyTracker:
    def __init__(self):
        self.pos = [0, 0] # Don't need to be called 'enemy pos' -> it's in the enemytracker lol
		self.health = 3 #fix these you bitch.  etc.
    def update(self, game_state):
        # TODO Yuv
        # own position
        # own health
        # own ammo
        # own diameter
        # own invulnerable (we don't worry about our own stuff -- this'll be easily reflected)

        # enemy ammo
        # enemy position
        # enemy health
        # enemy diameter
        # enemy is invulnerable
		is_invulnerable = #got hit or some shit in the past 5 ticks.? / set the ticks to when he is able to be hit again (similar to the website agent stats)

        pass
