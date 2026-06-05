from app.models.search_node import SearchNode


class SearchTree:
    def __init__(self, root: SearchNode):
        self.root = root

    def add_node(self, node: SearchNode, parent: SearchNode):
        parent.children.append(node)

    def set_solution(self, node: SearchNode):
        self.goal = node

    def get_solution_path(self):
        return self.goal.get_path() if hasattr(self, "goal") else None
