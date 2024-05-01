from enum import Enum


class Search(Enum):
    """Enum for search algorithms"""

    BREADTH_FIRST_SEARCH = "BFS"
    LOCAL_BEAM_SEARCH = "LBS"
