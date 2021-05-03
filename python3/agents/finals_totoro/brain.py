"""
Tracks the game state and decides on next strategy to execute
"""
from ..shared.utils.benchmark import Benchmark
from ..shared.trackers import FinalsTracker


class Brain:
    def __init__(self):
        self.benchmark = Benchmark()
        self.finals_tracker = FinalsTracker()

    def get_next_strategy(self, game_state) -> str:
        self.benchmark.start('tracker')
        self.finals_tracker.update(game_state)
        self.benchmark.end('tracker')

        print("I am totoro finals bot")

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
        elif not game_state['clear_path_to_enemy']:
            return 'block_destroy'
        else:
            return 'stalk'
