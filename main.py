from time import perf_counter

from app.algorithms import (
    a_star_search,
    backtracking_search,
    breadth_first_search,
    depth_first_search,
    ida_star_search,
    ordered_search,
    greedy_search,
)
from app.problems.regua_puzzle import get_successors, heuristic, is_goal

ALGORITHMS = (
    ("Backtracking Search", backtracking_search),
    ("Breadth-First Search", breadth_first_search),
    ("Depth-First Search", depth_first_search),
    ("Ordered Search", ordered_search),
    ("Greedy Search", greedy_search),
    ("A* Search", a_star_search),
    ("IDA* Search", ida_star_search),
)

PRIORITY = {
    "piece_priority": "A",
    "move_priority": "shortest",
}


def main():
    initial_state = tuple("AA-BB")
    for name, algorithm in ALGORITHMS:
        start_time = perf_counter()
        resolve = algorithm.search(
            initial_state, is_goal, get_successors, PRIORITY, heuristic
        )
        execution_time = perf_counter() - start_time
        print(f"{name} execution time: {execution_time:.6f} seconds")
        if resolve is not None:
            print_path(resolve.get_solution_path())
            print_metrics(resolve)
        else:
            print(f"\n{name} did not find a solution.")
        print()


def print_path(path):
    print("Solution path:")
    for state in path:
        print(state)


def print_metrics(search_tree):
    print("Solution metrics:")
    print(f"Solution depth: {search_tree.get_solution_depth()}")
    print(f"Solution cost: {search_tree.get_solution_cost()}")
    print(f"Expanded nodes: {search_tree.get_expanded_nodes()}")
    print(f"Visited nodes: {search_tree.get_visited_nodes()}")
    print(
        "Average branching factor: " f"{search_tree.get_average_branching_factor():.2f}"
    )


if __name__ == "__main__":
    main()
