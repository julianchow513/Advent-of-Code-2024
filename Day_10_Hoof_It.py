from setup import run_methods_in_parallel
from collections import deque
import copy


class HoofIt:
    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = self._read_file()
        self.trail_heads = self._find_trail_heads()
        self.ends = self._find_ends()

    def _read_file(self):
        grid = []
        with open(self.file_path, "r") as file:
            for line in file:
                grid.append(list(map(int, line.strip())))
        return grid

    def _find_trail_heads(self):
        trail_heads = []
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                if self.grid[y][x] == 0:
                    trail_heads.append((x, y))
        return trail_heads

    def _constraint(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def sum_all_trailheads(self):
        total = 0
        for x, y in self.trail_heads:
            total += self.score_trailhead(x, y)
        return total

    def score_trailhead(self, x, y):
        score = 0

        q = deque([(x, y)])
        seen = set([(x, y)])

        while q:
            cur_x, cur_y = q.popleft()
            if self.grid[cur_y][cur_x] == 9:
                score += 1
                continue

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cur_x + dx, cur_y + dy
                if (
                    self._constraint(nx, ny)
                    and (nx, ny) not in seen
                    and self.grid[cur_y][cur_x] + 1 == self.grid[ny][nx]
                ):
                    q.append((nx, ny))
                    seen.add((nx, ny))

        return score

    def sum_all_trailheads_rating(self):
        total = 0
        for x, y in self.trail_heads:
            total += self.score_trailhead_rating(x, y)
        return total

    def _find_ends(self):
        ends = set()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 9:
                    ends.add((x, y))
        return ends

    def score_trailhead_rating(self, x, y):
        grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        q = deque([(x, y)])

        while q:
            cur_x, cur_y = q.popleft()
            grid[cur_y][cur_x] += 1

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cur_x + dx, cur_y + dy
                if (
                    self._constraint(nx, ny)
                    and self.grid[cur_y][cur_x] + 1 == self.grid[ny][nx]
                ):
                    q.append((nx, ny))
        return self.sum_trailhead_rating(grid)
        
    def sum_trailhead_rating(self, grid):
        total = 0
        for x, y in self.ends:
            total += grid[y][x]
        return total


if __name__ == "__main__":
    hi = HoofIt("Inputs/day10_input.txt")

    results = run_methods_in_parallel(
        hi, "sum_all_trailheads", "sum_all_trailheads_rating", num_processes=2
    )

    for method_name, result in results.items():
        print(f"{method_name}: {result}")
