from .models import Grid, QueueFrontier, NoSolution, Solution


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid, _: int = 3) -> Solution:
        # Khởi tạo nút bắt đầu và thêm vào Frontier
        node = grid.get_node(pos=grid.start)
        frontier = QueueFrontier()
        frontier.add(node)
        # Tạo dict để lưu trữ các trạng thái đã được khám phá
        explored_states = {}

        while True:
            # Trả về NoSolution nếu Frontier rỗng
            if frontier.is_empty():
                return NoSolution([], list(explored_states))

            # Lấy nút đầu tiên từ Frontier
            node = frontier.remove()
            # Thêm trạng thái hiện tại vào explored_states
            explored_states[node.state] = True
            # Nếu nút hiện tại là nút đích, tạo đường đi và trả về một đối tượng Solution
            if node.state == grid.end:
                # Tạo danh sách các ô đã đi qua
                cells = []
                path_cost = 0
                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    path_cost += temp.cost
                    temp = temp.parent

                cells.append(grid.start)
                cells.reverse()

                return Solution(
                    cells, list(explored_states), path_cost=path_cost)

            # Xác định các nút láng giềng của nút hiện tại
            for action, state in grid.get_neighbours(node.state).items():
                if state in explored_states or frontier.contains_state(state):
                    continue

                new = grid.get_node(pos=state)
                new.parent = node
                new.action = action
                frontier.add(node=new)
