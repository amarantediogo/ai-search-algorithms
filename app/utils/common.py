from app.models.search_node import SearchNode


def build_child(parent: SearchNode, move) -> SearchNode:
    return SearchNode(move.state, parent, move.cost)
