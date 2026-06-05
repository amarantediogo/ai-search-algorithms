MOVES = {1, 2}


def is_goal(state: tuple[str]) -> bool:
    size = 1 + len(state) // 2
    seen_a = False
    for i in range(size):
        if state[i] == "A":
            seen_a = True
        if seen_a:
            return False
    return True


def get_successors(state: tuple[str]) -> list[tuple[str]]:
    empty_index = state.index("-")
    successors = []
    for i in range(len(state)):
        distance = abs(i - empty_index)
        if distance in MOVES:
            new_state = list(state)
            new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
            successors.append(tuple(new_state))
    return successors
