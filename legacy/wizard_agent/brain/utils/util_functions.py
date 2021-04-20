from typing import List

from . import constants
from . import structures

ACTIONS = constants.ACTIONS
Node = structures.Node

def manhattan_distance(start, end):
    """
    returns the manhattan distance between two tiles, calculated as:
    |x1 - x2| + |y1 - y2|
    """
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return distance


def get_surrounding_tiles(location, game_state):
    """Given a tile location as an (x,y) tuple, this function will return the surrounding tiles up, down, left and to
    the right as a list (i.e. [(x1,y1), (x2,y2),...]) as long as they do not cross the edge of the map """
    x = location[0]
    y = location[1]

    # find all the surrounding tiles relative to us
    # location[0] = col index; location[1] = row index
    tile_up = (x, y - 1)
    tile_down = (x, y + 1)
    tile_left = (x - 1, y)
    tile_right = (x + 1, y)

    # combine these int a list
    all_surrounding_tiles = [tile_up, tile_down, tile_right, tile_left]

    # get ones that are within bounds
    valid_surrounding_tiles = []

    for tile in all_surrounding_tiles:
        if game_state.is_in_bounds(tile):
            valid_surrounding_tiles.append(tile)

    return valid_surrounding_tiles


def get_empty_tiles(tiles, game_state):
    """
    Given a list of tiles, return ones that are actually empty
    """
    empty_tiles = []

    for tile in tiles:
        if is_walkable(tile, game_state):
            empty_tiles.append(tile)

    return empty_tiles


def get_safest_tile(location, tiles, bombs):
    """
    Given a list of tiles and bombs, find the tile that's safest to move to
    """

    bomb_distance = 1000
    closest_bomb = bombs[0]

    for bomb in bombs:
        new_bomb_distance = manhattan_distance(bomb, location)
        if new_bomb_distance < bomb_distance:
            bomb_distance = new_bomb_distance
            closest_bomb = bomb

    safe_dict = {}
    for tile in tiles:
        distance = manhattan_distance(closest_bomb, tile)
        safe_dict[tile] = distance

    # return the tile with the furthest distance from any bomb
    safest_tile = max(safe_dict, key=safe_dict.get)

    return safest_tile


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


def get_shortest_path(start, end, game_state, blast_tiles = []):
    """
    Finds the shortest path from the start node to the end node.
    Returns an array of (x,y) tuples. Uses A* search algorithm
    """
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
        neighbours = get_surrounding_tiles(current_node.position, game_state)

        for tile in neighbours:
            if tile in blast_tiles:
                continue  # skip if blast tile

            if not is_walkable(tile, game_state):
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


def is_walkable(tile, game_state):
    """
    Returns true if the tile is walkable
    """
    collectible = ["a", "t"]
    return not game_state.is_occupied(tile) or game_state.entity_at(tile) in collectible


def can_enqueue(queue, neighbour):
    """
    Helper function for the A* search algorithm. Checks if neighbour is in
    the queue and if it has lower total value
    """
    for node in queue:
        if neighbour == node and neighbour.total_cost >= node.total_cost:
            return False
    return True


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


def get_bombs_in_range(location, bombs):
    """
    Retrieves the bombs within the range of the AI
    """
    bombs_in_range = []
    for bomb in bombs:
        distance = manhattan_distance(location, bomb)
        # only freak out when bomb is in immediate position
        if distance <= 6:
            bombs_in_range.append(bomb)
    return bombs_in_range


def get_blast_zone(bomb, game_state):
    """
    Retrieves the tiles affected by the bomb blast
    """
    block_tile = ["ib", "sb", "ob"]
    blast_tiles = [bomb]
    neighbours = get_surrounding_tiles(bomb, game_state)
    for tile in neighbours:
        blast_tiles.append(tile)
        entity = game_state.entity_at(tile)
        if entity not in block_tile:
            x = tile[0]
            y = tile[1]
            blast_dir = move_to_tile(bomb, tile)
            if blast_dir == ACTIONS["left"]:
                blast_tiles.append((x - 1, y))
            elif blast_dir == ACTIONS["right"]:
                blast_tiles.append((x + 1, y))
            elif blast_dir == ACTIONS["up"]:
                blast_tiles.append((x, y + 1))
            elif blast_dir == ACTIONS["down"]:
                blast_tiles.append((x, y - 1))
    return blast_tiles


def get_nearest_tile(location, tiles):
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


def get_reachable_tiles(location, tiles, game_state):
    reachable_tiles = []
    for tile in tiles:
        path = get_shortest_path(location, tile, game_state)
        if path:
            reachable_tiles.append(tile)
    return reachable_tiles


def get_surrounding_empty_tiles(location, game_state):
    """
    Retrieves surrounding walkable tile around the location
    """
    surrounding_tiles = get_surrounding_tiles(location, game_state)
    empty_tiles = get_empty_tiles(surrounding_tiles, game_state)
    return empty_tiles


def get_empty_locations(tiles, game_state):
    empty_locations = []
    for tile in tiles:
        empty_tiles = get_surrounding_empty_tiles(tile, game_state)
        empty_locations = empty_locations + empty_tiles
    return empty_locations


def is_opponent_closer(location, opponent_location, block):
    """
    Gets the opponent's distance from the treasure and compare's it to our own distance from the treasure
    """
    if block is None:
        return False

    opponent_dist = manhattan_distance(opponent_location, block)
    our_dist = manhattan_distance(location, block)
    if our_dist > opponent_dist:
        return True
    return False


def get_opponent(location, opponents):
    for opponent in opponents:
        if opponent != location:
            return opponent
    return opponents[0]


def is_safe_path(location, target_location, bombs, game_state):
    path = get_shortest_path(location, target_location, game_state)
    all_blast = []
    for bomb in bombs:
        blast_tiles = get_blast_zone(bomb, game_state)
        all_blast.append(blast_tiles)
    if path:
        for coord in path:
            if coord in all_blast:
                return False
    return True


def get_safe_tiles(danger_tiles, game_state):
    """
    Retrieves all the safe walkable tiles outside of danger zone
    """
    safe_tiles = []
    for tile in danger_tiles:
        empty_tiles = get_surrounding_empty_tiles(tile, game_state)
        for empty in empty_tiles:
            if empty not in danger_tiles:
                safe_tiles.append(empty)
    return safe_tiles


def safe_escape(location, game_state):
    all_safe_walkable_tiles = []
    bombs = game_state.bombs
    blast_area = []
    for bomb in bombs:
        blast_zone = get_blast_zone(bomb, game_state)
        blast_area = blast_area + blast_zone
    blast_area = blast_area + get_blast_zone(location, game_state)  # putting the bomb on the bot's current location
    for row in range(0, 12):
        for col in range(0, 10):
            tile = tuple([row, col])
            if tile not in blast_area:
                if is_walkable(tile, game_state):
                    path = get_shortest_path(location, tile, game_state)
                    if path:
                        all_safe_walkable_tiles.append(tile)

    nearest_tile = get_nearest_tile(location, all_safe_walkable_tiles)
    return nearest_tile


def get_escape_matrix(game_state):
    size = game_state.size
    width = size[0]
    height = size[1]
    escape_paths = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            tile = (x, y)
            idx = width * y + x
            if is_walkable(tile, game_state):
                empty_tiles = get_surrounding_empty_tiles(tile, game_state)
                escape_paths[idx] = len(empty_tiles)
            else:
                escape_paths[idx] = -1
    return escape_paths


def get_matrix_val_for_tile(tile, matrix, map_width):
    x = tile[0]
    y = tile[1]
    idx = map_width * y + x
    return matrix[idx]


def get_tile_from_move(location, move):
    x = location[0]
    y = location[1]

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
