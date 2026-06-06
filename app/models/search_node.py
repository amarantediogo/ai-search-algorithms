from typing import Any


class SearchNode:
    def __init__(self, state: Any, parent: "SearchNode" = None, cost: int = 0):
        self.state = state
        self.parent = parent
        self.children: list["SearchNode"] = []
        self.cost = cost
        self.path_cost = cost if parent is None else parent.path_cost + cost

    def add_child(self, child_node: "SearchNode"):
        child_node.parent = self
        child_node.path_cost = self.path_cost + child_node.cost
        self.children.append(child_node)

    def get_path(self):
        path = []
        current_node = self
        while current_node is not None:
            path.append(current_node.state)
            current_node = current_node.parent
        return list(reversed(path))
