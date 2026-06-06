from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(initial_state, is_goal, get_successors, priority=None, heuristic=None):
    limit = heuristic(initial_state)

    while True:
        root = SearchNode(initial_state)
        search_tree = SearchTree(root)
        result = _search_limited(
            root,
            limit,
            is_goal,
            get_successors,
            heuristic,
            search_tree,
            {initial_state},
        )

        if isinstance(result, SearchNode):
            search_tree.set_solution(result)
            return search_tree

        if result == float("inf"):
            return None

        limit = result


def _search_limited(
    node,
    limit,
    is_goal,
    get_successors,
    heuristic,
    search_tree,
    path_states,
):
    estimate = node.path_cost + heuristic(node.state)
    if estimate > limit:
        return estimate

    if is_goal(node.state):
        return node

    next_limit = float("inf")

    for successor in get_successors(node.state):
        if successor.state in path_states:
            continue

        child = build_child(node, successor)
        search_tree.add_node(child, node)
        path_states.add(child.state)

        result = _search_limited(
            child,
            limit,
            is_goal,
            get_successors,
            heuristic,
            search_tree,
            path_states,
        )
        if isinstance(result, SearchNode):
            return result

        next_limit = min(next_limit, result)
        path_states.remove(child.state)

    return next_limit
