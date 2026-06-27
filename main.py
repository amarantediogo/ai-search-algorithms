import csv
from pathlib import Path
import sys
from time import perf_counter

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.algorithms import (
    a_star_search,
    backtracking_search,
    breadth_first_search,
    depth_first_search,
    ida_star_search,
    ordered_search,
    greedy_search,
)
from app.problems.regua_puzzle import (
    get_successors,
    heuristic,
    is_goal,
    load_instances,
)

RESULTS_PATH = ROOT_DIR / "results" / "regua_puzzle_results.csv"

ALGORITHMS = (
    ("Backtracking Search", backtracking_search),
    ("Breadth-First Search", breadth_first_search),
    ("Depth-First Search", depth_first_search),
    ("Ordered Search", ordered_search),
    ("Greedy Search", greedy_search),
    ("A* Search", a_star_search),
    ("IDA* Search", ida_star_search),
)

TIMEOUT_SECONDS = 600


def main():
    instances_path = Path(__file__).resolve().parent / "instances" / "regua_puzzle.json"
    instances = load_instances(str(instances_path))
    results = []

    for instance in instances:
        print(f"Instance: {instance.name}")
        print(f"Initial state: {format_state(instance.initial_state)}")
        priority = instance.get_priority()

        for name, algorithm in ALGORITHMS:
            start_time = perf_counter()
            resolve = algorithm.search(
                instance.initial_state,
                is_goal,
                get_successors,
                priority,
                heuristic,
                TIMEOUT_SECONDS,
            )
            execution_time = perf_counter() - start_time
            print(f"{name} execution time: {execution_time:.6f} seconds")

            if resolve is not None:
                solution_path = resolve.get_solution_path()
                print_path(solution_path)
                print_metrics(resolve)
                results.append(
                    build_result_row(
                        instance.name,
                        instance.initial_state,
                        name,
                        "found",
                        execution_time,
                        resolve,
                        solution_path,
                    )
                )
            else:
                print(f"\n{name} did not find a solution.")
                results.append(
                    build_result_row(
                        instance.name,
                        instance.initial_state,
                        name,
                        "not_found",
                        execution_time,
                    )
                )
            print()

        print("-" * 40)
        print()

    save_results_csv(results, RESULTS_PATH)
    print(f"Results saved to: {RESULTS_PATH}")


def build_result_row(
    instance_name,
    initial_state,
    algorithm_name,
    status,
    execution_time,
    search_tree=None,
    solution_path=None,
):
    return {
        "instance": instance_name,
        "initial_state": format_state(initial_state),
        "algorithm": algorithm_name,
        "status": status,
        "execution_time_seconds": f"{execution_time:.6f}",
        "solution_depth": (
            search_tree.get_solution_depth() if search_tree is not None else ""
        ),
        "solution_cost": (
            search_tree.get_solution_cost() if search_tree is not None else ""
        ),
        "expanded_nodes": (
            search_tree.get_expanded_nodes() if search_tree is not None else ""
        ),
        "visited_nodes": (
            search_tree.get_visited_nodes() if search_tree is not None else ""
        ),
        "average_branching_factor": (
            f"{search_tree.get_average_branching_factor():.2f}"
            if search_tree is not None
            else ""
        ),
        "solution_path": format_path(solution_path) if solution_path else "",
    }


def save_results_csv(results, path):
    if not results:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


def print_path(path):
    print("Solution path:")
    for state in path:
        print(format_state(state))


def print_metrics(search_tree):
    print("Solution metrics:")
    print(f"Solution depth: {search_tree.get_solution_depth()}")
    print(f"Solution cost: {search_tree.get_solution_cost()}")
    print(f"Expanded nodes: {search_tree.get_expanded_nodes()}")
    print(f"Visited nodes: {search_tree.get_visited_nodes()}")
    print(
        "Average branching factor: " f"{search_tree.get_average_branching_factor():.2f}"
    )


def format_state(state):
    return "".join(state)


def format_path(path):
    return " -> ".join(format_state(state) for state in path)


if __name__ == "__main__":
    main()
