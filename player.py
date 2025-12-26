class Player:
    def __init__(self, color, captured):
        self.color = color
        self.score = len(captured)
        self.captured = set(captured)
        self.frontier = set(captured)

    def get_captured(self):
        return self.captured

    def capture(self, pos):
        self.captured.add(pos)
        self.score = len(self.captured)

    def get_frontier(self):
        return self.frontier

    def clone(self):
        p = Player(self.color, set(self.captured))
        p.frontier = set(self.frontier)
        return p

