class SearchNode:
    state: any
    parent: "SearchNode"
    children: list["SearchNode"]
    cost: int

    def __init__(self, state, parent=None, cost=1):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = cost

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def get_path(self):
        path = []
        current_node = self
        while current_node is not None:
            path.append(current_node.state)
            current_node = current_node.parent
        return list(reversed(path))
