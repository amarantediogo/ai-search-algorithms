from app.models.search_node import SearchNode


class SearchTree:
    def __init__(self, root: SearchNode):
        self.root = root

    def add_node(self, node: SearchNode, parent: SearchNode):
        node.parent = parent
        parent.children.append(node)

    def set_solution(self, node: SearchNode):
        self.goal = node

    def get_solution_path(self):
        return self.goal.get_path() if hasattr(self, "goal") else None

    def get_solution_depth(self):
        if not hasattr(self, "goal"):
            return None

        depth = 0
        current_node = self.goal
        while current_node.parent is not None:
            depth += 1
            current_node = current_node.parent
        return depth

    def get_solution_cost(self):
        if not hasattr(self, "goal"):
            return None

        cost = 0
        current_node = self.goal
        while current_node.parent is not None:
            cost += current_node.cost
            current_node = current_node.parent
        return cost

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

    def get_profundidade_solucao(self):
        return self.get_solution_depth()

    def get_custo_solucao(self):
        return self.get_solution_cost()

    def get_nos_expandidos(self):
        return self.get_expanded_nodes()

    def get_nos_visitados(self):
        return self.get_visited_nodes()

    def get_fator_ramificacao_medio(self):
        return self.get_average_branching_factor()

    def _get_nodes(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(reversed(node.children))
