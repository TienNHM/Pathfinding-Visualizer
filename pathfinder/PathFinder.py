import time
from typing import Callable

from .bfs import BreadthFirstSearch
from .localbeam import LocalBeamSearch
from .models import Grid, Solution, Search

SearchFunction = Callable[[Grid, int], Solution]

SEARCH: dict[Search, SearchFunction] = {
    Search.BREADTH_FIRST_SEARCH: BreadthFirstSearch.search,
    Search.LOCAL_BEAM_SEARCH: LocalBeamSearch.search,
}


class PathFinder:
    @staticmethod
    def find_path(
        grid: Grid,
        search: Search,
        beam_width: int = 3,
    ) -> Solution:
        start_time = time.perf_counter()
        solution = SEARCH[search](grid, beam_width)
        time_taken = (time.perf_counter() - start_time) * 1000
        solution.time = time_taken

        return solution
