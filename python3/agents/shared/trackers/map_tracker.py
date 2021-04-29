"""
Used to track all information about the ores (their HP, etc)
"""
from ..utils.constants import ENTITIES
from ..utils.util_functions import convert_entities_to_coords, get_value_map_objects_from_arr, get_articulation_points


class MapTracker:

    def update(self, game_state):
        blast_blocks = []
        ore_blocks = []
        wood_blocks = []
        metal_blocks = []
        non_wall_blocks = []

        for entity in game_state.get("entities"):
            if entity.get("type") == ENTITIES.get("blast"):
                blast_blocks.append(entity)
            elif entity.get("type") == ENTITIES.get("ore"):
                ore_blocks.append(entity)
            elif entity.get("type") == ENTITIES.get("wood"):
                wood_blocks.append(entity)
            elif entity.get("type") == ENTITIES.get("metal"):
                metal_blocks.append(entity)
            else:
                non_wall_blocks.append(entity)

        game_state['destroyable_blocks'] = wood_blocks + ore_blocks
        game_state["blast_blocks"] = blast_blocks
        game_state["ore_blocks"] = ore_blocks
        game_state["wood_blocks"] = wood_blocks
        game_state["metal_blocks"] = metal_blocks
        game_state["wall_blocks"] = convert_entities_to_coords(ore_blocks + wood_blocks + metal_blocks + blast_blocks)
        game_state["non_wall_blocks"] = get_value_map_objects_from_arr(non_wall_blocks, None, True)

        pinch_points = get_articulation_points(game_state["player_pos"], game_state["world"], game_state["entities"])
        game_state["pinch_points"] = pinch_points
