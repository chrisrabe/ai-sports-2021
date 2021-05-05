"""
Tracks the game state and decides on next strategy to execute
"""

from ..shared.trackers import FinalsTracker
from ..shared.utils.benchmark import Benchmark
from ..shared.utils.util_functions import player_in_playzone


class Brain:
    def __init__(self):
        self.benchmark = Benchmark()
        self.finals_tracker = FinalsTracker()
        self.has_seen_enemy = False

    def get_next_strategy(self, game_state) -> str:
        """Conditionals to decide which strategy to execute. Returns string"""
        self.benchmark.start('tracker')
        self.finals_tracker.update(game_state)
        self.benchmark.end('tracker')

        print("I'm the totoro agent algo bot!!")

        if game_state['player_pos'] in game_state['all_hazard_zones']:
            print("Basic avoiding! Not getting me today, I'm FUCKING ORBITAL TOTORO")
            return 'basic_avoid'

        self.benchmark.start('detonate')
        if not game_state['enemy_is_invulnerable'] and game_state['enemy_pos'] in game_state['detonation_zones']:
            print("Say bye bye :) kabooom! Orbital totoro gonna ICBM your sorry state!")
            return 'detonate'
        self.benchmark.end('detonate')

        # # Killing strategies
        if game_state['player_inv_bombs'] > 0:

            self.benchmark.start('trap')
            self.finals_tracker.update_trap(game_state)
            self.benchmark.end('trap')

            if game_state['enemy_immediate_trapped']:
                print("I think the enemy's immediately trapped.")
                return 'simple_bomb'

            self.benchmark.start('onestep')
            self.finals_tracker.update_onestep(game_state)
            self.benchmark.end('onestep')
            if game_state['enemy_onestep_trapped']:
                print("I think the enemy is onestep trapped!")
                return 'simple_bomb'

            self.benchmark.start('controlzone')
            self.finals_tracker.update_enemy_control_zone(game_state)
            self.benchmark.end('controlzone')
            if game_state['enemy_control_zone'] <= 4:
                print("I think the enemy is running out of space to move.")
                return 'simple_bomb'
        else:
            if game_state['enemy_immediate_trapped'] and game_state['enemy_near_player'] and game_state['enemy_near_bomb']:
                return 'wait'  # stand there until enemy bombs themself

        self.benchmark.start('path')
        self.finals_tracker.update_path(game_state)
        self.benchmark.end('path')
        self.benchmark.start('danger')
        self.finals_tracker.update_danger(game_state)
        self.benchmark.end('danger')

        if not player_in_playzone(game_state['player_pos'], game_state['tick']):
            return 'playzone'

        # Toggle this so we don't run block destroy after seeing enemy for first time
        # The goal of block destroy was to just get ourselves our of the prison
        if game_state['clear_path_to_enemy']:
            self.has_seen_enemy = True

        if len(game_state['pickup_list']) != 0:
            print("Shiny pickup! Me collect!")
            return 'pickup'
        elif not game_state['clear_path_to_enemy'] and self.has_seen_enemy:
            return 'lurk'
        elif not game_state['clear_path_to_enemy'] and not self.has_seen_enemy:
            print("Eh.. There's no clear victory here, so I'm just gonna kill some blocks")
            return 'block_destroy'
        else:
            print("I'm gonna stalk!")
            return 'stalk'
