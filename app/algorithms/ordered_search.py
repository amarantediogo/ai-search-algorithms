from collections import deque

from app.models.search_node import SearchNode
from app.models.search_tree import SearchTree


def search(initial_state, is_goal, get_successors, priority=None):
    open_queue = deque([SearchNode(initial_state)])
    visited = set()
    search_tree = SearchTree(open_queue[0])

    while open_queue:
        current_state = open_queue.popleft()

        if is_goal(current_state.state):
            search_tree.set_solution(current_state)
            return search_tree

        visited.add(current_state.state)

        for successor in get_successors(current_state.state):
            if successor.state not in visited:
                node = SearchNode(successor.state, current_state, successor.cost)
                open_queue.append(node)
                search_tree.add_node(node, current_state)

        open_queue = deque(sorted(open_queue, key=lambda node: node.cost))

    return None
