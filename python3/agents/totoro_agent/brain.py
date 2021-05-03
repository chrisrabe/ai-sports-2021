"""
Tracks the game state and decides on next strategy to execute
"""

from ..shared.trackers import BombTracker, EnemyTracker, MapTracker, PickupTracker
from ..shared.utils.benchmark import Benchmark


class Brain:
    def __init__(self):
        self.benchmark = Benchmark()
        self.bomb_tracker = BombTracker()
        self.enemy_tracker = EnemyTracker()
        self.map_tracker = MapTracker()
        self.pickup_tracker = PickupTracker()

    def get_next_strategy(self, game_state) -> str:
        self.benchmark.start('tracker')
        """Conditionals to decide which strategy to execute. Returns string"""
        self.enemy_tracker.update(game_state)
        self.bomb_tracker.update(game_state)
        self.map_tracker.update(game_state)
        self.pickup_tracker.update(game_state)
        self.benchmark.end('tracker')

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
        # If you have ammo, just go for the kill
        # should probably refine this to check opponent vulnerability and trappable
        # Uncomment after done with basic_avoid

        # If you're in the blast tiles, stop being in them loser.
        # print(game_state['tick'], "player pos", game_state['player_pos'], "enemy bombs", game_state['enemy_active_bombs'], "\n Game State hazard zones:", game_state['hazard_zones'], game_state['player_pos'] in game_state['hazard_zones'])

        print("I'm the totoro agent algo bot!!")
        if game_state['player_pos'] in game_state['all_hazard_zones']:
            print('HOLY RUN FOR YOUR LIFE YOU ARE GONNA GET RAILED')
            return 'basic_avoid'  # Basic avoid vs retreat. Retreat value based, basic avoid is coded.

        # if enemy in detonation zone and we aren't + if they aren't invulnerable (we'll move out of the way via
        # basic_avoid's top priority) if not game_state['enemy_is_invulnerable'] and (game_state['enemy_pos'] in
        # game_state['detonation_zones'] and ( game_state['player_pos'] not in game_state['detonation_zones'])):
        # print('KABOOOM!! DETONATION TIME!') return 'detonate'
        if not game_state['enemy_is_invulnerable'] and (game_state['enemy_pos'] in game_state['detonation_zones']):
            # Check if either we're not in the det zone, or if this is the killing blow (and we'll live):
            if (game_state['player_pos'] not in game_state['detonation_zones']) or (
                    game_state['enemy_health'] == 1 and game_state['player_health'] > 1):
                print("KABOOM!!! Detonation Time!")
                return 'detonate'

        elif game_state['zoning'] and (game_state['player_inv_bombs'] > 3 and not game_state['enemy_near_bomb']):
            print("I'm gonna zone the bot!!")
            return "simple_bomb"
            
        # Hard-coding immediate trap (can put in a strategy later)
        ## Check if enemy is trapped: ->check if player can place a bomb that attacks enemy: -> do it.
        elif game_state['enemy_onestep_trapped'] and (game_state['player_inv_bombs'] > 0 and not game_state[
            'enemy_near_bomb']):  # Immediate trapped also takes into account whether the player is there.
            print("I think the enemy is trapped so I'm placing a bomb right now!!", game_state['tick'])
            # print(game_state['enemy_immediate_trapped'],game_state['player_inv_bombs'] > 0 and not game_state['enemy_near_bomb'])
            return "simple_bomb"  # place bomb

        # Pickup if ammo, stalk if none on map.
        elif len(game_state['pickup_list']) != 0:  # "Any pickups on the map?"
            print('me gusta I smell some pickups')
            return 'pickup'
        elif not game_state['clear_path_to_enemy'] and game_state['player_inv_bombs'] > 2:
            return 'block_destroy'
        else:
            print("I'ma stalk.")
            return 'stalk'
        print("Why would you print this? YOu royally fucked up. How is this even possible?")
