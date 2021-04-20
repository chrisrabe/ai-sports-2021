from typing import List
import operator
from . import strategy
from .utils import util_functions as utils, constants


class SmartBombStrategy(strategy.Strategy):
    def __init__(self):
        self.ore_states = {}
        self.prev_bombs = []
        self.game_state = None
        self.player_state = None
        # value between 0-1, closer to 1 means it's more likely to go to tile
        self.ore_priority = 0.5
        self.soft_priority = 1
        self.reachable_priority = 1
        self.urgent_priority = 1

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        location = player_state.location
        ore_blocks = game_state.ore_blocks
        soft_blocks = game_state.soft_blocks
        bombs = game_state.bombs

        # update ore state
        exploded_bombs = self.get_exploded_bombs(bombs)
        self.update_ore_state(ore_blocks, exploded_bombs)
        self.prev_bombs = bombs

        empty_near_soft = self.get_empty_near_blocks(soft_blocks)
        empty_near_ore = self.get_empty_near_blocks(ore_blocks)
        all_empty = empty_near_soft + empty_near_ore
        urgent_ores = self.get_urgent_ores()

        # retrieve the best tile
        ideal_tile = self.get_ideal_tile(all_empty, empty_near_soft, empty_near_ore, urgent_ores, location)

        # navigate to ideal tile
        if ideal_tile is not None:
            safe_tile_to_escape_to = utils.safe_escape(ideal_tile, game_state)
            path = utils.get_shortest_path(location, ideal_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            action_seq.append(constants.ACTIONS["bomb"])
            escape_path = utils.get_shortest_path(ideal_tile, safe_tile_to_escape_to, game_state)
            escape_seq = utils.get_path_action_seq(ideal_tile, escape_path)
            action_seq = action_seq + escape_seq
            return action_seq

        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state

        location = player_state.location
        ammo = player_state.ammo
        ore_blocks = game_state.ore_blocks
        soft_blocks = game_state.soft_blocks
        bombs = game_state.bombs
        empty_near_soft = self.get_empty_near_blocks(soft_blocks)
        empty_near_ore = self.get_empty_near_blocks(ore_blocks)
        all_empty = empty_near_soft + empty_near_ore
        # reachable_tiles = utils.get_reachable_tiles(location, all_empty, game_state) --> safe_escape checked for reachability
        urgent_ores = self.get_urgent_ores()

        # retrieve the best tile
        ideal_tile = self.get_ideal_tile(all_empty, empty_near_soft, empty_near_ore, urgent_ores, location)
        
        safe = False
        safe_tile_to_escape_to = False
        if ideal_tile is not None:
            safe = utils.is_safe_path(location, ideal_tile, bombs, game_state)
            safe_tile_to_escape_to = utils.safe_escape(ideal_tile, game_state)
        
        return ammo > 0 and ideal_tile and safe and safe_tile_to_escape_to

    def get_ideal_tile(self, all_empty, empty_near_soft, empty_near_ore, urgent_ores, location):
        opponent_list = self.game_state.opponents(self.player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        tile_map = self.get_tile_map(all_empty, empty_near_soft, empty_near_ore, urgent_ores, location)
        p_tile_map = dict(sorted(tile_map.items(), key=operator.itemgetter(1), reverse=True))
        possible_tiles = list(p_tile_map.keys())
        ideal_tile = None
        while len(possible_tiles) > 0:
            tile = possible_tiles.pop(0)
            path = utils.get_shortest_path(location, tile, self.game_state)
            if path and not utils.is_opponent_closer(location, opponent, tile):
                ideal_tile = tile
                break
        return ideal_tile

    def get_tile_map(self, all_empty, empty_near_soft, empty_near_ore, urgent_ores, location):
        tile_map = {}
        for tile in all_empty:
            score = self.get_score(tile, empty_near_soft, empty_near_ore, urgent_ores, location)
            if tile in tile_map:
                tile_map[tile] += score
            else:
                tile_map[tile] = score
        return tile_map

    def update_ore_state(self, ore_tiles, exploded_bombs):
        # initialise ore states if empty
        if not self.ore_states:
            for tile in ore_tiles:
                self.ore_states[tile] = 3
        # get danger areas
        danger_zones = []
        for bomb in exploded_bombs:
            blast_zone = utils.get_blast_zone(bomb, self.game_state)
            for tile in blast_zone:
                danger_zones.append(tile)
        # check if any ore tiles are in danger zone
        for tile in danger_zones:
            if tile in self.ore_states:
                self.ore_states[tile] -= 1
        # delete any tile that has no HP left
        tiles_to_delete = []
        for ore, value in self.ore_states.items():
            if value <= 0:
                tiles_to_delete.append(ore)
        for tile in tiles_to_delete:
            del self.ore_states[tile]

    def get_score(self, tile, empty_near_soft, empty_near_ore, urgent_ores, location):
        path = utils.get_shortest_path(location, tile, self.game_state)
        is_near_urgent = any(utils.manhattan_distance(tile, ore) <= 2 for ore in urgent_ores)
        score = 0

        # ensure that tile is reachable by putting reward / punishment
        if path is not None:
            score += self.reachable_priority
        else:
            score -= self.reachable_priority

        if tile in empty_near_soft:
            score += self.soft_priority
        if tile in empty_near_ore:
            score += self.ore_priority
        if is_near_urgent:
            score += self.urgent_priority
        return score

    def get_exploded_bombs(self, bombs):
        exploded_bombs = []
        for bomb in self.prev_bombs:
            if bomb not in bombs:
                exploded_bombs.append(bomb)
        return exploded_bombs

    def get_urgent_ores(self):
        urgent_ores = []
        for ore, value in self.ore_states.items():
            if value == 1:
                urgent_ores.append(ore)
        return urgent_ores

    def get_empty_near_blocks(self, blocks):
        empty_near_blocks = []
        for tile in blocks:
            empty_surround = utils.get_surrounding_empty_tiles(tile, self.game_state)
            empty_near_blocks = empty_near_blocks + empty_surround
        return empty_near_blocks
