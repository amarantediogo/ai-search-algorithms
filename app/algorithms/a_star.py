from heapq import heappop, heappush
from itertools import count

from app.algorithms.base import Algorithm
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode


class AStar(Algorithm):
    name: str = "A* Search"

    @staticmethod
    def search(problem: Puzzle):
        search_tree = problem.create_search_tree()
        root = search_tree.root
        root_key = problem.generate_state_key(root.value)
        frontier = []
        insertion_order = count()
        best_costs = {root_key: 0}

        heappush(
            frontier,
            (problem.heuristic(root.value), next(insertion_order), 0, root),
        )

        while frontier:
            _, _, current_cost, current_node = heappop(frontier)
            current_key = problem.generate_state_key(current_node.value)

            if current_cost > best_costs[current_key]:
                continue

            if problem.is_goal(current_node.value):
                return current_node

            for move in problem.next_moves(current_node.value):
                new_cost = current_cost + move.cost
                state_key = problem.generate_state_key(move.new_state)

                if state_key in best_costs and best_costs[state_key] <= new_cost:
                    continue

                new_node = SearchNode(
                    move.new_state,
                    parent=current_node,
                    cost=move.cost,
                )
                current_node.add_child(new_node)
                best_costs[state_key] = new_cost
                priority = new_cost + problem.heuristic(new_node.value)
                heappush(
                    frontier,
                    (priority, next(insertion_order), new_cost, new_node),
                )

        return None
