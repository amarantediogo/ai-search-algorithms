from dataclasses import dataclass

from app.models.search_tree.search_node import SearchNode


@dataclass
class SearchTree:
    root: SearchNode

    def get_visited_nodes(self) -> list[SearchNode]:
        nodes = []
        stack = [self.root]

        while stack:
            current_node = stack.pop()
            nodes.append(current_node)
            stack.extend(current_node.children or [])

        return nodes

    def count_visited_nodes(self) -> int:
        return len(self.get_visited_nodes())

    def get_expanded_nodes(self) -> list[SearchNode]:
        return [
            node
            for node in self.get_visited_nodes()
            if node.children
        ]

    def count_expanded_nodes(self) -> int:
        return len(self.get_expanded_nodes())

    def average_branching_factor(self) -> float:
        expanded_nodes = self.get_expanded_nodes()

        if not expanded_nodes:
            return 0.0

        total_children = sum(len(node.children or []) for node in expanded_nodes)
        return total_children / len(expanded_nodes)
