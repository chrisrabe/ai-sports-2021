"""
Used to track all information about the ores (their HP, etc)
"""
from ..utils.constants import ENTITIES


class MapTracker:

    def update(self, game_state):
        blast_blocks = []
        ore_blocks = []
        wood_blocks = []
        metal_blocks = []

        for entity in game_state.get("entities"):
            if entity.get("type") == ENTITIES.get("blast"):
                blast_blocks.append(entity)
            elif entity.get("type") == ENTITIES.get("ore"):
                ore_blocks.append(entity)
            elif entity.get("type") == ENTITIES.get("wood"):
                wood_blocks.append(entity)
            elif entity.get("type") == ENTITIES.get("metal"):
                metal_blocks.append(entity)

        game_state["blast_blocks"] = blast_blocks
        game_state["ore_blocks"] = ore_blocks
        game_state["wood_blocks"] = wood_blocks
        game_state["metal_blocks"] = metal_blocks

        # TODO me and tony
        # pinch points of map - floyd warshall (research)
