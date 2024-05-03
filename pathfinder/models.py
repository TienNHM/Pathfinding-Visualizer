from __future__ import annotations
from heapq import heappush, heappop
from enum import Enum


class Node:
    def __init__(
        self,
        value: str,
        state: tuple[int, int],
        cost: int,
        parent: Node | None = None,
        action: str | None = None
    ) -> None:
        self.value = str(cost) if value == "" else value
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        self.estimated_distance = float("inf")

    def __lt__(self, other: Node) -> bool:
        if self.estimated_distance == float("inf"):
            return self.state < other.state
        
        return self.estimated_distance < other.estimated_distance

    def __repr__(self) -> str:
        return f"Node({self.state!r}, Node(...), {self.action!r})"


class Frontier:
    def __init__(self) -> None:
        self.frontier: list[Node] = []

    def add(self, node: Node) -> None:
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]) -> bool:
        return any(node.state == state for node in self.frontier)

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} => {self.frontier}"


class StackFrontier(Frontier):
    def remove(self) -> Node:
        if self.is_empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop()


class QueueFrontier(Frontier):
    def remove(self) -> Node:
        if self.is_empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop(0)


class PriorityQueueFrontier(Frontier):
    def __init__(self):
        self.frontier: list[tuple[int, Node]] = []

    def add(self, node: Node, priority: int = 0) -> None:
        heappush(self.frontier, (priority, node))

    def get(self, state: tuple[int, int]) -> Node | None:
        for _, node in self.frontier:
            if node.state == state:
                return node

        return None

    def pop(self) -> Node:
        _, node = heappop(self.frontier)
        return node


class Grid:
    def __init__(
        self,
        grid: list[list[Node]],
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> None:
        self.grid: list[list[Node]] = grid
        self.start = start
        self.end = end
        self.width = max(len(row) for row in grid)
        self.height = len(grid)

    def get_node(self, pos: tuple[int, int]) -> Node:
        return self.grid[pos[0]][pos[1]]

    def get_cost(self, pos: tuple[int, int]) -> int:
        try:
            return self.grid[pos[0]][pos[1]].cost
        except IndexError:
            print(f"IndexError: {pos}")
            return 999999

    def get_neighbours(
        self,
        pos: tuple[int, int]
    ) -> dict[str, tuple[int, int]]:

        row, col = pos

        action_pos_mapper = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1),
            # "upleft": (row - 1, col - 1),
            # "upright": (row - 1, col + 1),
            # "downleft": (row + 1, col - 1),
            # "downright": (row + 1, col + 1),
        }

        possible_actions = {}
        for action, (r, c) in action_pos_mapper.items():
            print('---------------------------')
            print(action, (r, c), self.get_cost((r, c)))
            if not (0 <= r < self.height and 0 <= c < self.width):
                continue

            if self.grid[r][c].value == "#":
                continue

            possible_actions[action] = (r, c)

        return possible_actions

    def __repr__(self) -> str:
        return f"Grid([[...], ...], {self.start}, {self.end})"


class Solution:
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
    def __repr__(self) -> str:
        explored = list(self.explored)
        return (f"NoSolution([], {'{'}{explored[0]}, {explored[1]},"
                f" ...{'}'}, {self.time})")


class Search(Enum):
    BREADTH_FIRST_SEARCH = "BFS"
    LOCAL_BEAM_SEARCH = "LBS"
    GREEDY_BEST_FIRST_SEARCH = "GBFS"