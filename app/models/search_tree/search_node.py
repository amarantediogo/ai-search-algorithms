from dataclasses import dataclass


@dataclass
class SearchNode:
    value: any
    parent: "SearchNode" = None
    children: list["SearchNode"] = None

    @property
    def depth(self) -> int:
        depth = 0
        current_node = self
        while current_node.parent is not None:
            depth += 1
            current_node = current_node.parent
        return depth

    def add_child(self, child: "SearchNode") -> None:
        child.parent = self
        if self.children is None:
            self.children = []
        self.children.append(child)
