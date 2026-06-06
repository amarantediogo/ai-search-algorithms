from app.models.search_node import SearchNode


class SearchTree:
    def __init__(self, root: SearchNode):
        self.root = root
        self.goal = None

    def add_node(self, node: SearchNode, parent: SearchNode):
        parent.add_child(node)

    def set_solution(self, node: SearchNode):
        self.goal = node

    def get_solution_path(self):
        return self.goal.get_path() if self.goal is not None else None

    def get_solution_depth(self):
        if self.goal is None:
            return None
        return len(self.goal.get_path()) - 1

    def get_solution_cost(self):
        if self.goal is None:
            return None
        return self.goal.path_cost

    def get_expanded_nodes(self):
        return sum(1 for node in self._get_nodes() if node.children)

    def get_visited_nodes(self):
        return sum(1 for _ in self._get_nodes())

    def get_average_branching_factor(self):
        expanded_nodes = self.get_expanded_nodes()
        if expanded_nodes == 0:
            return 0

        total_children = sum(len(node.children) for node in self._get_nodes())
        return total_children / expanded_nodes

    def _get_nodes(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(reversed(node.children))
