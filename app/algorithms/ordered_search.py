from collections import deque

from app.models.search_node import SearchNode


def search(initial_state, is_goal, get_successors):
    open_queue = deque([SearchNode(initial_state)])
    visited = set()

    while open_queue:
        current_state = open_queue.popleft()

        if is_goal(current_state.state):
            return current_state

        visited.add(current_state.state)

        for successor in get_successors(current_state.state):
            if successor[0] not in visited:
                open_queue.append(
                    SearchNode(successor[0], current_state, cost=successor[1])
                )

        open_queue = deque(sorted(open_queue, key=lambda node: node.cost))

    return None
