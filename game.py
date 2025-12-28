import copy

class Game:
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    def __init__(self, grid, turn: int , me, opponent):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        # turn 0 = my turn ,  turn 1 = opponent turn
        self.turn = turn

        self.player = me
        self.opponent = opponent

    def get_available_moves(self) -> list:
        moves = [1,2,3,4,5,6]
        moves.remove(self.player.color)
        try:
            moves.remove(self.opponent.color)
        except:
            pass
        return moves

    def check_total_score(self) -> int:
        return self.player.score + self.opponent.score


    def is_frontier(self, pos, player) -> bool:
        x, y = pos
        for dx, dy in Game.directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_pos(nx, ny) and (nx, ny) not in player.captured:
                return True
        return False

    def make_move(self, color) -> bool:
        if color not in self.get_available_moves():
            print("Invalid move")
            return False

        if self.turn == 0:
            player = self.player
            opponent = self.opponent
        else:
            player = self.opponent
            opponent = self.player

        queue = list(player.frontier)
        new_captured = set()

        while queue:
            x, y = queue.pop(0)

            for dx, dy in Game.directions:
                nx, ny = x + dx, y + dy

                if not self.is_valid_pos(nx, ny):
                    continue
                if (nx, ny) in opponent.captured or (nx, ny) in player.captured:
                    continue
                if self.grid[nx][ny] != color:
                    continue

                player.captured.add((nx,ny))
                new_captured.add((nx,ny))
                queue.append((nx,ny))

        new_frontier = set()
        for pos in player.captured:
            if self.is_frontier(pos, player):
                new_frontier.add(pos)

        player.frontier = new_frontier
        player.color = color
        player.score = len(player.captured)

        self.turn = 1 - self.turn

        return True

    def get_grid(self):
        return self.grid

    def draw(self):
        for row in self.grid:
            print(row)
        print('-----' * 3)

    def is_valid_pos(self, i, j) -> bool:
        return 0 <= i < self.rows and 0 <= j < self.cols

    def clone(self):
        return Game(copy.deepcopy(self.grid), self.turn, self.player.clone(), self.opponent.clone())
