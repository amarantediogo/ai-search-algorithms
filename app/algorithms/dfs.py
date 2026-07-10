from app.algorithms.base import Algorithm
from app.models.puzzles.base import Puzzle
from app.models.search_tree.search_node import SearchNode


class DFS(Algorithm):
    name: str = "Depth-First Search"

    @staticmethod
    def search(problem: Puzzle):
        search_tree = problem.create_search_tree()
        limit = len(problem.get_initial_state()) ** 2
        root = search_tree.root
        stack = [root]
        visited_depths = {problem.generate_state_key(root.value): 0}

        while stack:
            current_node = stack.pop()
            current_depth = current_node.depth

            if problem.is_goal(current_node.value):
                return current_node

            if current_depth >= limit:
                continue

            next_moves = problem.next_moves(current_node.value)

            for move in next_moves:
                child_depth = current_depth + 1
                state_key = problem.generate_state_key(move.new_state)
                best_known_depth = visited_depths.get(state_key)
                if best_known_depth is not None and best_known_depth <= child_depth:
                    continue

                child_node = SearchNode(
                    move.new_state,
                    parent=current_node,
                    cost=move.cost,
                )
                current_node.add_child(child_node)
                visited_depths[state_key] = child_depth
                stack.append(child_node)

        return None
