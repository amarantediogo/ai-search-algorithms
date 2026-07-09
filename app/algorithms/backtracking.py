from app.algorithms.base import Algorithm
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode


class Backtracking(Algorithm):
    name: str = "Backtracking"

    @staticmethod
    def search(problem: Puzzle):
        search_tree = problem.create_search_tree()
        current_node = search_tree.root
        visited_states = set()

        while current_node:
            if problem.is_goal(current_node.value):
                return current_node.value

            next_moves = problem.next_moves(current_node.value)

            if not next_moves:
                visited_states.add(problem.generate_state_key(current_node.value))
                current_node = current_node.parent
                continue

            valid_next_moves = Backtracking.__filter_valid_moves(
                next_moves, problem, visited_states
            )

            if not valid_next_moves:
                visited_states.add(problem.generate_state_key(current_node.value))
                current_node = current_node.parent
                continue

            priority_move = problem.select_priority_move(valid_next_moves)

            if priority_move:
                new_node = SearchNode(priority_move.new_state, parent=current_node)
                current_node.add_child(new_node)
                visited_states.add(problem.generate_state_key(current_node.value))
                current_node = new_node
            else:
                visited_states.add(problem.generate_state_key(current_node.value))
                current_node = current_node.parent

        return None

    @staticmethod
    def __filter_valid_moves(next_moves, problem, visited_states):
        valid_next_moves = []
        for move in next_moves:
            state_key = problem.generate_state_key(move.new_state)
            if state_key not in visited_states:
                valid_next_moves.append(move)
        return valid_next_moves
