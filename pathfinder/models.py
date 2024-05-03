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
    """Model a frontier for managing nodes"""

    def __init__(self) -> None:
        self.frontier: list[Node] = []

    def add(self, node: Node) -> None:
        """Add a new node to the frontier

        Args:
            node (Node): Maze node
        """
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]) -> bool:
        """Check if a state exists in the frontier

        Args:
            state (tuple[int, int]): Postion of a node

        Returns:
            bool: Whether the provided state exists
        """
        return any(node.state == state for node in self.frontier)

    def is_empty(self) -> bool:
        """Check if the frontier is empty

        Returns:
            bool: Whether the frontier is empty
        """
        return len(self.frontier) == 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} => {self.frontier}"


class StackFrontier(Frontier):
    def remove(self) -> Node:
        """Remove element from the stack

        Raises:
            Exception: Empty Frontier

        Returns:
            Node: Cell (Node) in a matrix
        """
        if self.is_empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop()


class QueueFrontier(Frontier):
    def remove(self) -> Node:
        """Remove element from the queue

        Raises:
            Exception: Empty Frontier

        Returns:
            Node: Cell (Node) in a matrix
        """
        if self.is_empty():
            raise Exception("Empty Frontier")
        else:
            return self.frontier.pop(0)


class PriorityQueueFrontier(Frontier):
    def __init__(self):
        self.frontier: list[tuple[int, Node]] = []

    def add(self, node: Node, priority: int = 0) -> None:
        """Add a new node into the frontier

        Args:
            node (AStarNode): Maze node
            priority (int, optional): Node priority. Defaults to 0.
        """
        heappush(self.frontier, (priority, node))

    def get(self, state: tuple[int, int]) -> Node | None:
        """Get node by state. Create new if not found

        Args:
            state (tuple[int, int]): State

        Returns:
            Node: Required node
        """
        for _, node in self.frontier:
            if node.state == state:
                return node

        return None

    def pop(self) -> Node:
        """Remove a node from the frontier

        Returns:
            AStarNode: Node to be removed
        """
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

        # Calculate grid dimensions
        self.width = max(len(row) for row in grid)
        self.height = len(grid)

    def get_node(self, pos: tuple[int, int]) -> Node:
        """Get node by position

        Args:
            pos (tuple[int, int]): Cell position

        Returns:
            int: Weight
        """
        return self.grid[pos[0]][pos[1]]

    def get_cost(self, pos: tuple[int, int]) -> int:
        """Get weight of a node

        Args:
            pos (tuple[int, int]): Cell position

        Returns:
            int: Weight
        """
        try:
            return self.grid[pos[0]][pos[1]].cost
        except IndexError:
            print(f"IndexError: {pos}")
            # return infinte cost
            return 999999

    def get_neighbours(
        self,
        pos: tuple[int, int]
    ) -> dict[str, tuple[int, int]]:
        """Determine the neighbours of a cell

        Args:
            pos (tuple[int, int]): Cell position

        Returns:
            dict[str, tuple[int, int]]: Action - Position Mapper
        """

        row, col = pos

        # Map actions with resulting cell positions
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

        # Determine possilbe actions
        possible_actions = {}

        # TODO: choose best actions based on the value of the cell
        #      and the distance to the goal
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