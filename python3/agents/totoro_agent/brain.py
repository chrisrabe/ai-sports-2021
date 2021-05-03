"""
Tracks the game state and decides on next strategy to execute
"""

from ..shared.trackers import FinalsTracker
from ..shared.utils.benchmark import Benchmark


class Brain:
    def __init__(self):
        self.benchmark = Benchmark()
        self.finals_tracker = FinalsTracker()

    def get_next_strategy(self, game_state) -> str:
        self.benchmark.start('tracker')
        """Conditionals to decide which strategy to execute. Returns string"""
        self.finals_tracker.update(game_state)
        self.benchmark.end('tracker')
        self.finals_tracker.update_path(game_state)
        self.finals_tracker.update_onestep(game_state)
        self.finals_tracker.update_trap(game_state)

        """
        # Highest Prio (base state): Collect + Stay away from immediate danger (fire + potential blast zones)
        # 2nd highest Destroy walls
        # --> If possible; KILL.

        # For destroy strats:
        # -> If it's at the highest spot on the value map and there's a destroyable next to it,
        # kill (then map is update 'oh no bomb!!' and run)

        # Basic Decision Making:
        
        Strats:
        Stalk by default -> 'stalk';
        If there is ammo: go get it -> 'pickup';
        If there is bomb: 'retreat'; 
        """
        print("I'm the totoro agent algo bot!!")
        if game_state['player_pos'] in game_state['all_hazard_zones']:
            return 'basic_avoid'

        self.benchmark.start('detonate')
        if not game_state['enemy_is_invulnerable'] and game_state['enemy_pos'] in game_state['detonation_zones']:
            return 'detonate'
        self.benchmark.end('detonate')

        # # Killing strategies
        if game_state['player_inv_bombs'] > 0:
            self.benchmark.start('trap')
            self.finals_tracker.update_trap(game_state)
            self.benchmark.end('trap')
            if game_state['enemy_immediate_trapped']:
                return 'simple_bomb'

            self.benchmark.start('onestep')
            self.finals_tracker.update_onestep(game_state)
            self.benchmark.end('onestep')
            if game_state['enemy_onestep_trapped']:
                return 'simple_bomb'

        self.benchmark.start('path')
        self.finals_tracker.update_path(game_state)
        self.benchmark.end('path')

        if len(game_state['pickup_list']) != 0:
            return 'pickup'
        elif not game_state['clear_path_to_enemy'] and game_state['player_inv_bombs'] > 2:
            return 'block_destroy'
        else:
            return 'stalk'

        # if game_state['player_pos'] in game_state['all_hazard_zones']:
        #     print('HOLY RUN FOR YOUR LIFE YOU ARE GONNA GET RAILED')
        #     return 'basic_avoid'  # Basic avoid vs retreat. Retreat value based, basic avoid is coded.


        # if not game_state['enemy_is_invulnerable'] and (game_state['enemy_pos'] in game_state['detonation_zones']):
        #     # Check if either we're not in the det zone, or if this is the killing blow (and we'll live):
        #     if (game_state['player_pos'] not in game_state['detonation_zones']) or (
        #             game_state['enemy_health'] == 1 and game_state['player_health'] > 1):
        #         print("KABOOM!!! Detonation Time!")
        #         return 'detonate'
            
        # # Hard-coding immediate trap (can put in a strategy later)
        # ## Check if enemy is trapped: ->check if player can place a bomb that attacks enemy: -> do it.
        # elif game_state['enemy_onestep_trapped'] and (game_state['player_inv_bombs'] > 0 and not game_state[
        #     'enemy_near_bomb']):  # Immediate trapped also takes into account whether the player is there.
        #     print("I think the enemy is trapped so I'm placing a bomb right now!!", game_state['tick'])
        #     # print(game_state['enemy_immediate_trapped'],game_state['player_inv_bombs'] > 0 and not game_state['enemy_near_bomb'])
        #     return "simple_bomb"  # place bomb

        # # Pickup if ammo, stalk if none on map.
        # elif len(game_state['pickup_list']) != 0:  # "Any pickups on the map?"
        #     print('me gusta I smell some pickups')
        #     return 'pickup'
        # elif not game_state['clear_path_to_enemy'] and game_state['player_inv_bombs'] > 2:
        #     return 'block_destroy'
        # else:
        #     print("I'ma stalk.")
        #     return 'stalk'
        # print("Why would you print this? YOu royally fucked up. How is this even possible?")
