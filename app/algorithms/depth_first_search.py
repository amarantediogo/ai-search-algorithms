from collections import deque

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree
from app.utils.common import build_child


def search(initial_state, is_goal, get_successors, priority=None, heuristic=None):
    root = SearchNode(initial_state)
    open_stack = deque([root])
    discovered = {initial_state}
    search_tree = SearchTree(root)

    while open_stack:
        current_state = open_stack.pop()

        if is_goal(current_state.state):
            search_tree.set_solution(current_state)
            return search_tree

        for successor in get_successors(current_state.state):
            if successor.state in discovered:
                continue
            discovered.add(successor.state)
            node = build_child(current_state, successor)
            open_stack.append(node)
            search_tree.add_node(node, current_state)

    return None
