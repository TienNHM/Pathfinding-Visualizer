from .models import Grid, QueueFrontier, NoSolution, Solution
from typing import List


class LocalBeamSearch:
    @staticmethod
    def search(grid: Grid, beam_width: int = 3) -> Solution:
        # Khởi tạo beam với một nút duy nhất (vị trí bắt đầu)
        initial_node = grid.get_node(pos=grid.start)
        beam = [initial_node]

        # Tạo dict để lưu trữ các trạng thái đã được khám phá
        explored_states = {}

        while True:
            next_beam = []  # Tạo beam mới

            for node in beam:
                # Nếu nút hiện tại là nút đích, tạo đường đi và trả về một đối tượng Solution
                if node.state == grid.end:
                    # Tạo danh sách các ô đã đi qua
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

                # Xác định các nút láng giềng của nút hiện tại
                for action, state in grid.get_neighbours(node.state).items():
                    if state in explored_states:
                        continue
                    new_node = grid.get_node(pos=state)
                    new_node.parent = node
                    new_node.action = action
                    next_beam.append(new_node)

                # Thêm trạng thái hiện tại vào explored_states
                explored_states[node.state] = True
            

            # Sắp xếp các nút trong beam tăng dần theo cost (chi phí)
            next_beam.sort(key=lambda n: n.cost)
            # Giữ lại beam_width nút có chi phí thấp nhất
            beam = next_beam[:beam_width]

            # Nếu không còn nút nào trong beam, trả về NoSolution
            if not beam:
                return NoSolution([], list(explored_states))

