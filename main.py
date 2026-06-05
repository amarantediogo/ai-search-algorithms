from app.algorithms import breadth_first_search
from app.problems.regua_puzzle import get_successors, is_goal


def main():
    initial_state = tuple("AAA-BBB")
    resolve = breadth_first_search.search(initial_state, is_goal, get_successors)
    print(resolve)


if __name__ == "__main__":
    main()
