from app.models.instances.regua_puzzle_instance import ReguaPuzzleInstance
from app.models.puzzles.regua_puzzle import ReguaPuzzle


def main():
    regua_puzzle()


def regua_puzzle():
    instances_path = "data/instances/regua_puzzle.json"
    puzzle = ReguaPuzzle()
    instances = ReguaPuzzleInstance.load_instances(instances_path)

    for instance in instances:
        print(f"Solving instance: {instance}")
        try:
            puzzle.solve(instance)
        except Exception as e:
            print(f"An error occurred while solving the instance: {e}")
        break


if __name__ == "__main__":
    main()
