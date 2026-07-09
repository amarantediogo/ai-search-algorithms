from heapq import heappop, heappush
from itertools import count

from app.algorithms.base import Algorithm
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode


class Ordered(Algorithm):
    name: str = "Ordered Search"

    @staticmethod
    def search(problem: Puzzle):
        search_tree = problem.create_search_tree()
        root = search_tree.root
        visited_states = {problem.generate_state_key(root.value)}
        frontier = []
        insertion_order = count()

        heappush(frontier, (problem.heuristic(root.value), next(insertion_order), root))

        while frontier:
            _, _, current_node = heappop(frontier)

            if problem.is_goal(current_node.value):
                return current_node.value

            next_moves = problem.next_moves(current_node.value)

            for move in next_moves:
                state_key = problem.generate_state_key(move.new_state)
                if state_key in visited_states:
                    continue

                new_node = SearchNode(move.new_state, parent=current_node)
                current_node.add_child(new_node)
                visited_states.add(state_key)
                heappush(
                    frontier,
                    (
                        problem.heuristic(new_node.value),
                        next(insertion_order),
                        new_node,
                    ),
                )

        return None
