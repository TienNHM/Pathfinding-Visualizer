from enum import Enum

class Solution:
    """Model a solution to a pathfinding problem"""

    def __init__(
        self,
        path: list[tuple[int, int]],
        explored: list[tuple[int, int]],
        time: float = 0,
        path_cost: int = 0
    ) -> None:
        self.path = path
        self.path_cost = path_cost
        self.path_length = len(path)
        self.explored = explored
        self.explored_length = len(explored)
        self.time = time

    def __repr__(self) -> str:
        return (f"Solution([{self.path[0]}, ..., {self.path[-1]}],"
                f" {'{...}'}, {self.time})")


class NoSolution(Solution):
    """Model an empty pathfinding solution"""

    def __repr__(self) -> str:
        explored = list(self.explored)
        return (f"NoSolution([], {'{'}{explored[0]}, {explored[1]},"
                f" ...{'}'}, {self.time})")


class Search(Enum):
    """Enum for search algorithms"""

    BREADTH_FIRST_SEARCH = "BFS"
    LOCAL_BEAM_SEARCH = "LBS"
    GREEDY_BEST_FIRST_SEARCH = "GBFS"