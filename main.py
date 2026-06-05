from time import perf_counter

from app.algorithms import breadth_first_search, depth_first_search, ordered_search
from app.problems.regua_puzzle import get_successors, is_goal

ALGORITHMS = (
    ("Breadth-First Search", breadth_first_search),
    ("Depth-First Search", depth_first_search),
    ("Ordered Search", ordered_search),
)


def main():
    initial_state = tuple("AA-BB")
    for name, algorithm in ALGORITHMS:
        start_time = perf_counter()
        resolve = algorithm.search(initial_state, is_goal, get_successors)
        execution_time = perf_counter() - start_time
        print(f"{name} execution time: {execution_time:.6f} seconds")
        if resolve is not None:
            print(f"{name} path:")
            print_path(resolve.get_path())
        else:
            print(f"\n{name} did not find a solution.")
        print()


def print_path(path):
    for state in path:
        print(state)


if __name__ == "__main__":
    main()
