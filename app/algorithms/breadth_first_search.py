from collections import deque


def search(initial_state, is_goal, get_successors):
    queue = deque([initial_state])
    visited = set()

    while queue:
        current_state = queue.popleft()
        if is_goal(current_state):
            return current_state
        if current_state in visited:
            continue
        visited.add(current_state)
        for successor in get_successors(current_state):
            if successor not in visited:
                queue.append(successor)
    return None