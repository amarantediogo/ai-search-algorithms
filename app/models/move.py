class Move:
    state: any
    movement: any
    cost: int

    def __init__(self, state, movement, cost):
        self.state = state
        self.movement = movement
        self.cost = cost
