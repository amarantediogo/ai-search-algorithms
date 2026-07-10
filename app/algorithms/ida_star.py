from math import inf

from app.algorithms.base import Algorithm
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode


class IDAStar(Algorithm):
    name: str = "IDA* Search"

    @staticmethod
    def search(problem: Puzzle):
        initial_state = problem.get_initial_state()
        threshold = problem.heuristic(initial_state)

        while True:
            search_tree = problem.create_search_tree()
            root = search_tree.root
            path_states = {problem.generate_state_key(root.value)}
            solution, next_threshold = IDAStar.__search(
                problem,
                root,
                current_cost=0,
                threshold=threshold,
                path_states=path_states,
            )

            if solution is not None:
                return solution

            if next_threshold == inf:
                return None

            threshold = next_threshold

    @staticmethod
    def __search(problem, current_node, current_cost, threshold, path_states):
        estimated_cost = current_cost + problem.heuristic(current_node.value)

        if estimated_cost > threshold:
            return None, estimated_cost

        if problem.is_goal(current_node.value):
            return current_node, threshold

        next_threshold = inf

        for move in problem.next_moves(current_node.value):
            state_key = problem.generate_state_key(move.new_state)
            if state_key in path_states:
                continue

            child_node = SearchNode(
                move.new_state,
                parent=current_node,
                cost=move.cost,
            )
            current_node.add_child(child_node)
            path_states.add(state_key)

            solution, candidate_threshold = IDAStar.__search(
                problem,
                child_node,
                current_cost + move.cost,
                threshold,
                path_states,
            )

            if solution is not None:
                return solution, candidate_threshold

            next_threshold = min(next_threshold, candidate_threshold)
            path_states.remove(state_key)

        return None, next_threshold
