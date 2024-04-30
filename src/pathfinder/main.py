import time
from typing import Callable

from .search.astar import AStarSearch
from .search.gbfs import GreedyBestFirstSearch
from .search.bfs import BreadthFirstSearch
from .search.dfs import DepthFirstSearch
from .search.dijkstras import DijkstrasSearch
from .search.localbeam import LocalBeamSearch
from .models.grid import Grid
from .models.solution import Solution
from .models.search_types import Search
from .models.search_types import Search

SearchFunction = Callable[[Grid, int], Solution]

SEARCH: dict[Search, SearchFunction] = {
    Search.ASTAR_SEARCH: AStarSearch.search,
    Search.DIJKSTRAS_SEARCH: DijkstrasSearch.search,
    Search.BREADTH_FIRST_SEARCH: BreadthFirstSearch.search,
    Search.GREEDY_BEST_FIRST_SEARCH: GreedyBestFirstSearch.search,
    Search.DEPTH_FIRST_SEARCH: DepthFirstSearch.search,
    Search.LOCAL_BEAM_SEARCH: LocalBeamSearch.search,
}


class PathFinder:
    @staticmethod
    def find_path(
        grid: Grid,
        search: Search,
        beam_width: int = 10,
    ) -> Solution:
        start_time = time.perf_counter()
        solution = SEARCH[search](grid, beam_width)
        time_taken = (time.perf_counter() - start_time) * 1000
        solution.time = time_taken

        return solution
