from typing import List
from collections import defaultdict
import numpy as np

from .constants import ACTIONS, DEFAULT_REWARDS, BLOCKAGES
from .structures import Node


########################################################################
#   Game / World helper functions
########################################################################

def get_entity_coords(entity) -> tuple[int, int]:
    x = entity.get("x")
    y = entity.get("y")
    return x, y


def is_in_bounds(tile, world_width, world_height) -> bool:
    """
    Checks whether the tile is within the world boundaries
    """
    return (0 <= tile[0] < world_width) and (0 <= tile[1] < world_height)


def entity_at(tile, entities) -> str or None:
    """
    Retrieves the entity item at tile
    """
    x, y = tile
    for entity in entities:
        if entity["x"] == x and entity["y"] == y:
            return entity["type"]
    return None


def get_world_dimension(world):
    world_width = world["width"]
    world_height = world["height"]
    return world_width, world_height


########################################################################
#   Navigation helpers
########################################################################


def manhattan_distance(start, end):
    """
    returns the manhattan distance between two tiles, calculated as:
    |x1 - x2| + |y1 - y2|
    """
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return distance


def get_surrounding_tiles(location, world_width, world_height):
    """Given a tile location as an (x,y) tuple, this function will return the surrounding tiles up, down, left and to
    the right as a list (i.e. [(x1,y1), (x2,y2),...]) as long as they do not cross the edge of the map """
    x = location[0]
    y = location[1]

    # find all the surrounding tiles relative to us
    # location[0] = col index; location[1] = row index
    tile_up = (x, y + 1)
    tile_down = (x, y - 1)
    tile_left = (x - 1, y)
    tile_right = (x + 1, y)

    # combine these int a list
    all_surrounding_tiles = [tile_up, tile_down, tile_right, tile_left]

    # get ones that are within bounds
    valid_surrounding_tiles = []

    for tile in all_surrounding_tiles:
        if is_in_bounds(tile, world_width, world_height):
            valid_surrounding_tiles.append(tile)

    return valid_surrounding_tiles


def get_empty_tiles(tiles, entities, ignore_player=False):
    """
    Given a list of tiles, return ones that are actually empty
    """
    empty_tiles = []

    for tile in tiles:
        if is_walkable(tile, entities, ignore_player):
            empty_tiles.append(tile)

    return empty_tiles


def move_to_tile(location, tile):
    """
    Determines the action based on the tile. The other tile must be adjacent to the location tile
    """
    diff = tuple(x - y for x, y in zip(location, tile))

    if diff == (0, 1):
        return ACTIONS["down"]
    elif diff == (1, 0):
        return ACTIONS["left"]
    elif diff == (0, -1):
        return ACTIONS["up"]
    elif diff == (-1, 0):
        return ACTIONS["right"]
    else:
        return ACTIONS["none"]


def can_enqueue(queue, neighbour):
    """
    Helper function for the A* search algorithm. Checks if neighbour is in
    the queue and if it has lower total value
    """
    for node in queue:
        if neighbour == node and neighbour.total_cost >= node.total_cost:
            return False
    return True


def get_shortest_path(start, end, world, entities, blast_tiles=None, player_invulnerable=False,
                      ignore_bomb=False) -> object:
    """
    Finds the shortest path from the start node to the end node.
    Returns an array of (x,y) tuples. Uses A* search algorithm
    """
    world_width, world_height = get_world_dimension(world)
    if blast_tiles is None:
        blast_tiles = []
    if start is None or end is None:
        return None

    # create a list for all nodes to visit and have been visited
    queue = []
    visited = []

    # create a start node and end node
    start_node = Node(start, None)
    goal_node = Node(end, None)

    queue.append(start_node)

    while len(queue) > 0:
        # sort the open list to get the node with the lowest cost first
        queue.sort()

        # get the node with the lowest cost
        current_node = queue.pop(0)

        # add the current node to the closed list
        visited.append(current_node)

        # check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            # return reversed
            return path[::-1]

        # loop through each neighbour
        neighbours = get_surrounding_tiles(current_node.position, world_width, world_height)

        for tile in neighbours:
            if (tile in blast_tiles) and not player_invulnerable:
                continue  # skip if blast tile

            if not is_walkable(tile, entities, ignore_bomb=ignore_bomb):
                continue  # skip if not walkable

            neighbour = Node(tile, current_node)

            if neighbour in visited:
                continue  # skip if visited

            # generate heuristics
            neighbour.dist_to_start = manhattan_distance(neighbour.position, start_node.position)
            neighbour.dist_to_goal = manhattan_distance(neighbour.position, goal_node.position)
            neighbour.total_cost = neighbour.dist_to_start + neighbour.dist_to_goal

            # check if neighbour is in the open list and if it has a lower total value
            if can_enqueue(queue, neighbour):
                queue.append(neighbour)

    return None  # no path found


def is_walkable(tile, entities, ignore_player=True, ignore_bomb=False):
    """
    Returns true if the tile is walkable
    """
    collectible = ["a", "bp"]  # Ammo, powerup
    player = ['p', 'e', 'eb', 'pb']  # Player, enemy,
    if ignore_bomb:
        collectible.append("b")
    entity = entity_at(tile, entities)
    if ignore_player:
        return entity in collectible or entity is None or entity in player
    else:
        return entity in collectible or entity is None


def get_path_action_seq(location: object, path: List) -> List:
    """
    Given a list of (x,y) tuples, returns the action sequence to follow the path.
    If path is not there, returns nothing
    """
    if path:
        initial_action = move_to_tile(location, path[0])
        action_seq = [initial_action]
        i = 1
        while i < len(path):
            from_tile = path[i - 1]
            to_tile = path[i]
            action = move_to_tile(from_tile, to_tile)
            action_seq.append(action)
            i += 1
        return action_seq
    return [ACTIONS["none"]]


def get_blast_zone(bomb_loc, diameter, entities, world):
    """
    Retrieves the tiles affected by the bomb blast
    Returns list of blast tiles [[x,y],[x2,y2], ...]
    """
    world_width, world_height = get_world_dimension(world)
    radius = int(diameter / 2)
    block_tile = ["o", "m", "w"]
    blast_tiles = [bomb_loc]
    cur_loc = bomb_loc

    for i in range(radius):
        tile = get_tile_from_move(cur_loc, ACTIONS["left"])
        if is_in_bounds(tile, world_width, world_height) and entity_at(tile, entities) not in block_tile:
            blast_tiles.append(tile)
        else:
            break
        cur_loc = tile

    cur_loc = bomb_loc

    for i in range(radius):
        tile = get_tile_from_move(cur_loc, ACTIONS["right"])
        if is_in_bounds(tile, world_width, world_height) and entity_at(tile, entities) not in block_tile:
            blast_tiles.append(tile)
        else:
            break
        cur_loc = tile

    cur_loc = bomb_loc

    for i in range(radius):
        tile = get_tile_from_move(cur_loc, ACTIONS["up"])
        if is_in_bounds(tile, world_width, world_height) and entity_at(tile, entities) not in block_tile:
            blast_tiles.append(tile)
        else:
            break
        cur_loc = tile

    cur_loc = bomb_loc

    for i in range(radius):
        tile = get_tile_from_move(cur_loc, ACTIONS["down"])
        if is_in_bounds(tile, world_width, world_height) and entity_at(tile, entities) not in block_tile:
            blast_tiles.append(tile)
        else:
            break
        cur_loc = tile

    return blast_tiles


def get_nearest_tile(location, tiles):
    """
    Returns nearest tile in a list of tiles
    """
    if tiles:
        tile_dist = 1000
        closest_tile = tiles[0]
        for tile in tiles:
            new_dist = manhattan_distance(location, tile)
            if new_dist < tile_dist:
                tile_dist = new_dist
                closest_tile = tile
        return closest_tile
    else:
        return None


def min_distance(start, tiles):
    """
    Returns the closest tile given a starting point and a range of tiles (picks the first one)
    """
    tiles.reverse()
    distances = []
    for tile in tiles:
        cur_tile_dist = manhattan_distance(start, tile)
        distances.append(cur_tile_dist)
    mindist = min(distances)  # Grabs first item that has the min dist
    index = distances.index(mindist)
    return tiles[index]


def get_reachable_tiles(location, tiles, world, entities, blast_tiles=None, ignore_bomb=False):
    """
    Returns a list of reachable tiles (will pick the last one)
    """
    if blast_tiles is None:
        blast_tiles = []

    reachable_tiles = []
    for tile in tiles:
        path = get_shortest_path(location, tile, world, entities, blast_tiles, ignore_bomb=ignore_bomb)
        if path:
            reachable_tiles.append(tile)
    return reachable_tiles


def get_surrounding_empty_tiles(location, world, entities, ignore_player=True):
    """
    Retrieves surrounding walkable tile around the location
    """
    world_width, world_height = get_world_dimension(world)
    surrounding_tiles = get_surrounding_tiles(location, world_width, world_height)
    empty_tiles = get_empty_tiles(surrounding_tiles, entities, ignore_player)
    return empty_tiles


def get_empty_locations(tiles, world, entities, ignore_player=True):
    """
    Given a list of tiles, returns a list of empty tiles surrounding them
    """
    empty_locations = []
    for tile in tiles:
        empty_tiles = get_surrounding_empty_tiles(tile, world, entities, ignore_player)
        empty_locations = empty_locations + empty_tiles
    return empty_locations


def is_opponent_closer(location, opponent_location, destination):
    """
    Returns true if the opponent is closer to the destination than us
    """
    if destination is None:
        return False

    opponent_dist = manhattan_distance(opponent_location, destination)
    our_dist = manhattan_distance(location, destination)
    if our_dist > opponent_dist:
        return True
    return False


def get_matrix_val_for_tile(tile, matrix, map_width):
    x = tile[0]
    y = tile[1]
    idx = map_width * y + x
    return matrix[idx]


def get_tile_from_move(location, move):
    """
    Takes in location and an action (string). Returns location of tile moved to.
    """
    x, y = location

    if move == ACTIONS["down"]:
        return tuple((x, y - 1))
    elif move == ACTIONS["left"]:
        return tuple((x - 1, y))
    elif move == ACTIONS["up"]:
        return tuple((x, y + 1))
    elif move == ACTIONS["right"]:
        return tuple((x + 1, y))
    else:
        return tuple((x, y))


def is_movement(action):
    actions = [
        ACTIONS["up"],
        ACTIONS["down"],
        ACTIONS["right"],
        ACTIONS["left"]
    ]
    return action in actions


# Update value map based on reward entities input
def update_rec_value_map(rval, value_map, world_dim, max_reward_spread=0,
                         OUTER_MAP_VALUES=((-100, -100), (-100, -100))):
    '''
    Updates the reward value map with mask matrix application, based on reward entity.
    Returns a numpy array representing the updated reward value map.
    '''
    # add map padding
    pad_dim = (world_dim[0] - 1, world_dim[1] - 1)
    value_map = np.pad(value_map, (pad_dim, pad_dim), 'constant', constant_values=OUTER_MAP_VALUES)
    rval_offset = pad_dim[0]  # padding offset

    reward = rval[2]
    reward_discount = reward / abs(reward)
    reward_spread = 0

    # max reward spread shall not exceed the dimension of the map
    # (mask matrices of +1 or -1 are applied in additive layers that correspond to the magnitude of the reward value)
    max_reward_spread = min(max_reward_spread, world_dim[0] - 1)

    if reward > 0:
        # positive reward value
        for i, value in enumerate(range(0, reward, 1)):
            if i <= max_reward_spread:
                reward_spread = i
            xstart = rval[1] + rval_offset - reward_spread
            xend = rval[1] + rval_offset + 1 + reward_spread
            ystart = rval[0] + rval_offset - reward_spread
            yend = rval[0] + rval_offset + 1 + reward_spread

            # Updates reward values in the map matrix.
            value_map[xstart:xend, ystart:yend] = value_map[xstart:xend, ystart:yend] + reward_discount

    elif reward < 0:
        # negative reward value
        for i, value in enumerate(range(0, reward, -1)):
            if i <= max_reward_spread:
                reward_spread = i
            xstart = rval[1] + rval_offset - reward_spread
            xend = rval[1] + rval_offset + 1 + reward_spread
            ystart = rval[0] + rval_offset - reward_spread
            yend = rval[0] + rval_offset + 1 + reward_spread

            # Updates reward values in the map matrix.
            value_map[xstart:xend, ystart:yend] = value_map[xstart:xend, ystart:yend] + reward_discount
    else:
        # reward assigned is 0
        pass

    # remove map padding
    value_map = value_map[world_dim[0] - 1:world_dim[0] + pad_dim[0], world_dim[0] - 1:world_dim[0] + pad_dim[0]]

    return value_map


def update_dia_value_map(rval, value_map, world_dim, max_reward_spread=0,
                         OUTER_MAP_VALUES=((-100, -100), (-100, -100))):
    '''
    Updates the reward value map with mask matrix application, based on reward entity.
    Returns a numpy array representing the updated reward value map.
    '''
    # add map padding
    pad_dim = (world_dim[0] - 1, world_dim[1] - 1)
    value_map = np.pad(value_map, (pad_dim, pad_dim), 'constant', constant_values=OUTER_MAP_VALUES)
    rval_offset = pad_dim[0]  # padding offset

    reward = rval[2]
    reward_discount = reward / abs(reward)
    reward_spread = 0
    decay = 0

    # max reward spread shall not exceed the dimension of the map
    max_spread = min(abs(reward), max_reward_spread, world_dim[0] - 1)

    xo = rval[1] + rval_offset
    yo = rval[0] + rval_offset

    if reward > 0:
        # positive reward value
        for i, value in enumerate(range(0, reward, 1)):
            if i <= max_spread:
                spread = i

            xs = xo - spread
            xe = xo + 1 + spread
            ys = yo - spread
            ye = yo + 1 + spread

            # decay effect applied on each concentric value dispersion
            decay = 1 - (i / abs(reward))

            value_map[xs:xe, yo - max_spread:yo + max_spread + 1] = value_map[xs:xe,
                                                                    yo - max_spread:yo + max_spread + 1] + reward_discount * decay
            value_map[xo - max_spread:xo + max_spread + 1, ys:ye] = value_map[xo - max_spread:xo + max_spread + 1,
                                                                    ys:ye] + reward_discount * decay

    elif reward < 0:
        # negative reward value
        for i, value in enumerate(range(0, reward, -1)):
            if i <= max_spread:
                spread = i

            xs = xo - spread
            xe = xo + 1 + spread
            ys = yo - spread
            ye = yo + 1 + spread

            # decay effect applied on each concentric value dispersion
            decay = 1 - (i / abs(reward))

            value_map[xs:xe, yo - max_spread:yo + max_spread + 1] = value_map[xs:xe,
                                                                    yo - max_spread:yo + max_spread + 1] + reward_discount * decay
            value_map[xo - max_spread:xo + max_spread + 1, ys:ye] = value_map[xo - max_spread:xo + max_spread + 1,
                                                                    ys:ye] + reward_discount * decay

    else:
        # Reward assigned is 0.
        pass

    # remove map padding
    value_map = value_map[world_dim[0] - 1:world_dim[0] + pad_dim[0], world_dim[0] - 1:world_dim[0] + pad_dim[0]]

    return value_map


def get_value_map(world, walls, game_objects, reward_map, pinch_points=None, use_default=True):
    """
    Returns a numpy array map representing the values

    walls must be an array of (x,y) tuples

    game objects must be an array of objects with the following schema:
    {
       loc: (x, y)
       type: string
    }

    reward map must be a dictionary with the following schema
    {
       [ENTITY_TYPE]: number
    }

    pinch points must be an array of (x,y) tuples or is None (articulation points)

    use_default is a boolean to represent whether we should use the default reward map
    """

    # TODO are there numpy helper functions to help with these logic?

    # create 2D matrix filled with zeroes
    world_dim = get_world_dimension(world)
    value_map = np.zeros(world_dim)

    # replace all walls with -10
    for wall in walls:
        x, y = wall
        value_map[y, x] = DEFAULT_REWARDS['wall']

    # sets the reward spread for reward mask application
    max_reward_spread = world_dim[0] - 1

    rec_value_map = value_map
    dia_value_map = value_map

    # get score mask for all non-wall objects
    for item in game_objects:
        if use_default:
            if item['type'] in reward_map:
                reward = reward_map[item['type']]
            else:
                reward = DEFAULT_REWARDS[item['type']]
        else:
            if item['type'] not in reward_map:
                continue
            else:
                reward = reward_map[item['type']]

        # update mask based reward map
        reward_entity = [item['loc'][0], item['loc'][1], reward]
        rec_value_map = update_rec_value_map(reward_entity, rec_value_map, world_dim, max_reward_spread)
        reward_mask = get_reward_mask(item, reward, world)
        dia_value_map = np.add(dia_value_map, reward_mask)

    # re-evaluate for pinch points
    if pinch_points is not None:
        for tile in pinch_points:
            pinch_reward = DEFAULT_REWARDS['pinch']
            if 'pinch' in reward_map:
                pinch_reward = reward_map['pinch']

            # Update mask based reward map
            reward_entity = [tile[0], tile[1], pinch_reward]
            rec_value_map = update_rec_value_map(reward_entity, rec_value_map, world_dim, max_reward_spread)
            reward_mask = get_reward_mask(tile, pinch_reward, world, True)
            dia_value_map = np.add(dia_value_map, reward_mask)

    value_map = np.add(rec_value_map, dia_value_map)

    return value_map


def get_reward_mask(item, reward, world, is_tuple=False):
    """
    Returns reward mask
    """
    world_width, world_height = get_world_dimension(world)
    mask = np.zeros((world_width, world_height))

    abs_reward = abs(reward)

    # modified iterative floodfill algorithm
    to_fill = set()
    if is_tuple:
        to_fill.add(item)
    else:
        to_fill.add(item['loc'])
    while len(to_fill) != 0:
        cur_tile = to_fill.pop()
        neighbours = get_surrounding_tiles(cur_tile, world_width, world_height)
        tile_scores = get_tile_scores_from_mask(neighbours, mask)
        max_reward = np.amax(tile_scores)
        cur_tile_x, cur_tile_y = cur_tile
        if max_reward == 0:  # evaluating starting point
            mask[cur_tile_y, cur_tile_x] = abs_reward
        else:
            mask[cur_tile_y, cur_tile_x] = max_reward - 1
        if max_reward != 1:
            for tile in neighbours:
                x, y = tile
                if mask[y, x] == 0:  # not visited
                    to_fill.add(tile)

    # propagation decreases or increases the value of reward by one until it reaches 0
    # if the reward is a negative number, it will add 1 for each level until reaches 0
    # the opposite is applied to positive numbers
    return mask * -1 if reward < 0 else mask


def get_value_map_objects_from_arr(tiles, item_type=None, has_xy=False, tile_prop=None):
    game_objects = []
    for tile in tiles:
        # variations of getting x, y values
        if has_xy:
            x = tile['x']
            y = tile['y']
        elif tile_prop is not None:
            x, y = tile[tile_prop]
        else:
            x, y = tile
        # if item type not defined, tile has type
        if item_type is None:
            game_objects.append(get_value_map_object(x, y, tile['type']))
        else:
            game_objects.append(get_value_map_object(x, y, item_type))
    return game_objects


def get_value_map_object(x, y, item_type):
    return {
        'loc': (x, y),
        'type': item_type
    }


def get_tile_scores_from_mask(tiles, mask):
    tile_scores = np.zeros(len(tiles))
    for i in range(len(tiles)):
        x, y = tiles[i]
        tile_scores[i] = mask[y, x]
    return tile_scores


def convert_entities_to_coords(entities):
    coords = []
    for entity in entities:
        coords.append(get_entity_coords(entity))
    return coords


def get_move_from_value_map(cur_loc, value_map, world):
    world_width, world_height = get_world_dimension(world)
    neighbours = get_surrounding_tiles(cur_loc, world_width, world_height)
    max_val = -1
    new_loc = cur_loc
    for tile in neighbours:
        x, y = tile
        tile_val = value_map[y, x]
        if tile_val > max_val:
            max_val = tile_val
            new_loc = tile
    return move_to_tile(cur_loc, new_loc)


def player_has_control(player_pos, enemy_pos, world) -> bool:
    """
    Compares the distance of the player and enemy position from the corner of the map.
    If the player is further from the corner of the map, it means that they have map control.
    Returns true if player has control of the map
    """
    world_width, world_height = get_world_dimension(world)
    world_corners = [(0, 0), (world_width - 1, 0), (0, world_height - 1), (world_width - 1, world_height - 1)]

    # check if enemy is closer to world edge than player
    min_player_corner_dist = min(manhattan_distance(player_pos, world_corners[0]),
                                 manhattan_distance(player_pos, world_corners[1]),
                                 manhattan_distance(player_pos, world_corners[2]),
                                 manhattan_distance(player_pos, world_corners[3]))

    min_enemy_corner_dist = min(manhattan_distance(enemy_pos, world_corners[0]),
                                manhattan_distance(enemy_pos, world_corners[1]),
                                manhattan_distance(enemy_pos, world_corners[2]),
                                manhattan_distance(enemy_pos, world_corners[3]))

    # get number of empty tiles in the enemy surrounding that meets the condition for attack engagement
    return min_player_corner_dist > min_enemy_corner_dist


def get_articulation_points(player_loc, world, entities) -> list[tuple[int, int]]:
    """
    Retrieves the articulation points for the walkable tiles in the map
    relative to the player position
    """
    # (x, y) -> set of neighbours
    graph = get_undirected_graph(player_loc, world, entities)
    visited = set()
    art = set()
    parents = {}
    low = {}

    # helper dfs
    def dfs(node_id, node, parent):
        visited.add(node)
        parents[node] = parent
        num_edges = 0
        low[node] = node_id

        for nei in graph[node]:
            if nei == parent:
                continue
            if nei not in visited:
                parents[nei] = node
                num_edges += 1
                dfs(node_id + 1, nei, node)

            low[node] = min(low[node], low[nei])

            if node_id <= low[nei]:
                if parents[node] != -1:  # must not be root
                    art.add(node)

        if parents[node] == -1 and num_edges >= 2:  # if root - different condition applies
            art.add(node)

    # TODO stress test!!
    # if recursive DFS fk's up with stackoverflow, replace with iterative DFS
    # Use custom graph node to propagate lowest up to parent

    dfs(0, player_loc, -1)
    return list(art)


def get_undirected_graph(player_loc, world, entities):
    """
    Iteratively creates an undirected graph relative to player location
    """
    queue = [player_loc]
    graph = defaultdict(set)
    visited = set()

    while len(queue) != 0:
        node = queue.pop(0)
        visited.add(node)
        neighbours = get_surrounding_empty_tiles(node, world, entities)
        for nei in neighbours:
            graph[node].add(nei)
            graph[nei].add(node)
            if nei not in visited:
                queue.append(nei)
    return graph


def death_trap(tile, world, entities) -> bool:
    """
    Checks whether the tile no longer has walkable tiles
    """
    world_width, world_height = get_world_dimension(world)
    neighbours = get_surrounding_tiles(tile, world_width, world_height)
    for nei in neighbours:
        if entity_at(nei, entities) not in BLOCKAGES:
            return False
    return True


def get_detonation_target(target_pos, own_bombs, world, entities) -> tuple[int, int] or None:
    """
    Retrieves the bomb that affects the target.
    Checks if any of our own bomb will have a blast zone at the target position.
    """
    bomb_coords = []
    bomb_dict = {}
    for bomb in own_bombs:
        coord = bomb['coord']
        bomb_coords.append(coord)
        bomb_dict[coord] = bomb
    reachable_bombs = get_reachable_tiles(target_pos, bomb_coords, world, entities, ignore_bomb=True)
    for tile in reachable_bombs:
        bomb = bomb_dict[tile]
        blast_zone = get_blast_zone(tile, bomb['blast_diameter'], entities, world)
        if target_pos in blast_zone:
            return tile
    return None


def get_safe_tiles(hazard_tiles, world, entities):
    """
    Returns every (walkable) tile in the world which isn't in the tiles given
    """
    world_width, world_height = get_world_dimension(world)
    safe_tiles = []
    for y in range(world_height):
        for x in range(world_width):
            tile = (x, y)
            if tile not in hazard_tiles and is_walkable(tile, entities):
                safe_tiles.append(tile)
    return safe_tiles


def dummy_bomb(location, blast_diameter):
    """
    Returns a dummy bomb. Useful for determining traps.
    """
    return {'coord': location, 'blast_diameter': blast_diameter}


def move_results_in_ouchie(location, move, hazards):
    tile = get_tile_from_move(location, move)
    return tile in hazards


def get_num_escape_paths(player_pos, tile, blast_diameter, entities, world):
    """
    Gets the number of reachable escape paths if a bomb was placed on a specific tile.
    """
    # simulate bombing
    blast_zone = get_blast_zone(tile, blast_diameter, entities, world)
    # get safe tiles from blast zone
    safe_tiles = []
    for blast_tile in blast_zone:
        empty_tiles = get_surrounding_empty_tiles(blast_tile, world, entities, ignore_player=False)
        for empty in empty_tiles:
            if empty not in blast_tile:
                safe_tiles.append(empty)
    # are there safe tiles that player can reach?
    reachable_tiles = get_reachable_tiles(player_pos, safe_tiles, world, entities)
    return len(reachable_tiles)


def is_trappable(tile, world, entities):
    return len(get_surrounding_empty_tiles(tile, world, entities, ignore_player=False)) < 2


def is_dangerous(entity, player_pos, enemy_pos, world, entities):
    x, y = get_entity_coords(entity)
    return manhattan_distance(player_pos, enemy_pos) <= 2 and is_trappable((x, y), world, entities)


def get_playzone(tick) -> tuple[int, int, int, int]:
    """
    Retrieves the world dimension at certain tick range. WARNING: HARDCODED
    Returns tuple
    world_width, world_height, x_offset, y_offset
    """
    if tick < 1800:
        return 9, 9, 0, 0
    elif 1800 < tick < 1855:
        return 9, 7, 0, 1  # top and bottom tiles gone
    elif 1855 < tick < 1890:
        return 7, 7, 1, 1  # sides gone
    elif 1890 < tick < 1925:
        return 7, 5, 1, 2  # second layer gone
    elif 1925 < tick < 1950:
        return 5, 5, 2, 2  # etc
    elif 1950 < tick < 1975:
        return 5, 3, 2, 3
    elif 1975 < tick < 1990:
        return 3, 3, 3, 3
    elif 1990 < tick < 2005:
        return 3, 1, 3, 4
    else:
        return 1, 1, 4, 4


def player_in_playzone(player_pos, tick) -> bool:
    """
    Checks if the player is within the area
    """
    world_width, world_height, x_offset, y_offset = get_playzone(tick)

    zone_start_x = 0 + x_offset
    zone_start_y = 0 + y_offset
    zone_end_x = world_width - x_offset
    zone_end_y = world_height - y_offset

    player_x, player_y = player_pos
    return zone_start_x <= player_x < zone_end_x and zone_start_y <= player_y < zone_end_y
