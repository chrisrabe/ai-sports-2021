"""
Tracks the game state and decides on next strategy to execute
"""

from ..shared.trackers import BombTracker, EnemyTracker, MapTracker, PickupTracker


class Brain:
    def __init__(self):
        self.bomb_tracker = BombTracker()
        self.enemy_tracker = EnemyTracker()
        self.map_tracker = MapTracker()
        self.pickup_tracker = PickupTracker()

    def get_next_strategy(self, game_state) -> str:
        """Conditionals to decide which strategy to execute. Returns string"""
        self.enemy_tracker.update(game_state)
        self.bomb_tracker.update(game_state)
        self.map_tracker.update(game_state)
        self.pickup_tracker.update(game_state)

        """
        Highest Prio (base state): Collect + Stay away from immediate danger (fire + potential blast zones)
        2nd highest Destroy walls
        --> If possible; KILL.

        For destroy strats:
        -> If it's at the highest spot on the value map and there's a destroyable next to it,
        kill (then map is update 'oh no bomb!!' and run)

        Basic Decision Making:
        Strats:
        Stalk by default -> 'stalk';
        If there is ammo: go get it -> 'pickup';
        If there is bomb: 'retreat'; 
        """

        # If you're in the blast tiles, do RETREAT
        print("I'm the vm totoro agent!!")
        if game_state['player_pos'] in game_state['all_hazard_zones'] or game_state['player_on_bomb']:
            print('HOLY RUN FOR YOUR LIFE YOU ARE GONNA GET RAILED')
            return 'retreat'

        # Tell enemy to go away by placing bomb down
        if game_state['tell_enemy_gtfo'] and game_state['player_inv_bombs'] > 0 and not game_state['enemy_near_bomb']:
            # Tell enemy to GTFO by placing bomb down
            print('Totoro screams at enemy to GTFO')
            return 'simple_bomb'

        # Killing strategies
        if not game_state['enemy_is_invulnerable'] and not game_state['player_on_bomb']:
            # if enemy is standing in detonation zone
            if game_state['enemy_pos'] in game_state['detonation_zones']:
                print('Time to detonate!')
                return 'detonate'

            if game_state['enemy_onestep_trapped'] and game_state['player_inv_bombs'] != 0:
                print("I think the enemy is trapped s I'm placing the bomb right now!!")
                return 'bomb'

            # If you have ammo, just go for the kill
            # should probably refine this to check opponent vulnerability and trappable
            if game_state['player_inv_bombs'] != 0 and not game_state['enemy_near_bomb'] and game_state['clear_path_to_enemy']:
                return 'kill'

        # Basic Decision Making
        # Pickup if ammo, stalk if none on map.
        if len(game_state['pickup_list']) != 0:  # "Any pickups on the map?"
            print('me gusta I smell some pickups')
            return 'pickup'
        elif not game_state['clear_path_to_enemy']:
            return 'block_destroy'
        else:
            return 'stalk'
