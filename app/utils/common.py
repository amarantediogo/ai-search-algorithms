from app.models.search_node import SearchNode
from app.models.move import Move


def build_child(parent: SearchNode, move: Move) -> SearchNode:
    return SearchNode(move.state, cost=move.cost)
