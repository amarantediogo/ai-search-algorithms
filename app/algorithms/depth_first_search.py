from collections import deque

from app.models.search_node import SearchNode


def search(initial_state, is_goal, get_successors, priority=None):
    open_stack = deque([SearchNode(initial_state)])
    visited = set()

    while open_stack:
        current_state = open_stack.pop()

        if is_goal(current_state.state):
            return current_state

        visited.add(current_state.state)

        for successor in get_successors(current_state.state):
            if successor.state not in visited:
                open_stack.append(
                    SearchNode(successor.state, current_state, successor.cost)
                )

    return None
