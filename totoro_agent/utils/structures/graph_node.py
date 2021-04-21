from typing import Tuple


class Node:
    def __init__(self, position: Tuple, parent: Tuple):
        self.position = position
        self.parent = parent
        self.dist_to_start = 0
        self.dist_to_goal = 0
        self.total_cost = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __gt__(self, other):
        return self.total_cost > other.total_cost

    def __repr__(self):
        return "({0},{1})".format(self.position, self.total_cost)
