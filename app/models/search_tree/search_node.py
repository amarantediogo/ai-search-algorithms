from dataclasses import dataclass


@dataclass
class SearchNode:
    value: any
    parent: "SearchNode" = None
    children: list["SearchNode"] = None
    cost: float = 0.0

    @property
    def depth(self) -> int:
        depth = 0
        current_node = self
        while current_node.parent is not None:
            depth += 1
            current_node = current_node.parent
        return depth

    @property
    def path_cost(self) -> float:
        total_cost = 0.0
        current_node = self
        while current_node is not None:
            total_cost += current_node.cost
            current_node = current_node.parent
        return total_cost

    @property
    def path(self) -> list["SearchNode"]:
        path = []
        current_node = self
        while current_node is not None:
            path.append(current_node)
            current_node = current_node.parent
        return list(reversed(path))

    def add_child(self, child: "SearchNode") -> None:
        child.parent = self
        if self.children is None:
            self.children = []
        self.children.append(child)
