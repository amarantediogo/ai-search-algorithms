from collections import deque

from app.algorithms.base import Algorithm
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode


class BFS(Algorithm):
    name: str = "Breadth-First Search"

    @staticmethod
    def search(problem: Puzzle):
        search_tree = problem.create_search_tree()
        root = search_tree.root
        queue = deque([root])
        visited_states = {problem.generate_state_key(root.value)}

        while queue:
            current_node = queue.popleft()

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
                queue.append(new_node)

        return None
