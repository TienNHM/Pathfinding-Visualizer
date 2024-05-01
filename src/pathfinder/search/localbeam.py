from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from typing import List


class LocalBeamSearch:
    @staticmethod
    def search(grid: Grid, beam_width: int = 10) -> Solution:
        """Find path between two points in a grid using Local Beam Search

        Args:
            grid (Grid): Grid of points
            beam_width (int): Number of states to maintain in the beam

        Returns:
            Solution: Solution found
        """
        print(f"Local Beam Search: Beam Width = {beam_width}")
        
        # Initialize the beam with a single node (source cell)
        initial_node = grid.get_node(pos=grid.start)
        beam = [initial_node]

        # Keep track of explored positions
        explored_states = {}

        while True:
            next_beam = []  # Next iteration's beam

            for node in beam:
                # If reached destination point
                if node.state == grid.end:
                    # Generate path and return a Solution object
                    cells = []
                    path_cost = 0
                    temp = node
                    while temp.parent is not None:
                        cells.append(temp.state)
                        path_cost += temp.cost
                        temp = temp.parent
                    cells.append(grid.start)
                    cells.reverse()
                    return Solution(cells, list(explored_states), path_cost=path_cost)

                # Determine possible actions
                for action, state in grid.get_neighbours(node.state).items():
                    if state in explored_states:
                        continue
                    new_node = grid.get_node(pos=state)
                    new_node.parent = node
                    new_node.action = action
                    next_beam.append(new_node)

                # Add current node position into the explored set
                explored_states[node.state] = True
            

            # Sort next_beam by some heuristic (e.g., path cost, distance to goal)
            next_beam.sort(key=lambda n: n.cost)

            # Keep only the top beam_width nodes
            beam = next_beam[:beam_width]

            # Return empty Solution object if beam is empty
            if not beam:
                print("No solution found")
                return NoSolution([], list(explored_states))

# Example usage:
# local_beam_search = LocalBeamSearch()
# solution = local_beam_search.search(grid=my_grid, beam_width=5)
# print(solution)
