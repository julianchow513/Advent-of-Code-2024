from collections import deque
from setup import run_methods_in_parallel


class GardenGroups:
    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = self._read_file()

    def _read_file(self):
        grid = []

        with open(self.file_path, "r") as file:
            for line in file:
                grid.append(list(line.strip()))
        return grid

    def _constraint(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def find_groups(self):
        groups = []
        seen = set()

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if (x, y) not in seen:
                    cur_group = self.bfs(x, y)
                    seen.update(cur_group)
                    groups.append(cur_group)

        return groups

    def bfs(self, x, y):
        val = self.grid[y][x]

        q = deque([(x, y)])
        group = set([(x, y)])

        while q:
            cur_x, cur_y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cur_x + dx, cur_y + dy
                if (
                    self._constraint(nx, ny)
                    and self.grid[ny][nx] == val
                    and (nx, ny) not in group
                ):
                    q.append((nx, ny))
                    group.add((nx, ny))
        return group

    def find_fence_price(self):
        groups = self.find_groups()
        total = 0

        for group in groups:
            area = len(group)
            perimeter = self.find_perimeter(group)
            total += area * perimeter
        return total

    def find_perimeter(self, group):
        dirc = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        perimeter = 0

        for x, y in group:
            for dx, dy in dirc:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in group:
                    perimeter += 1
        return perimeter

    def find_discount_fence_price(self):
        groups = self.find_groups()
        total = 0

        for group in groups:
            area = len(group)
            num_sides = self.find_num_sides(group)
            total += area * num_sides
        return total

    def find_num_sides(self, group):
        dirc = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        num_sides = set()

        for x, y in group:
            for dx, dy in dirc:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in group:
                    if (dx, dy) == (0, 1) or (dx, dy) == (0, -1):
                        num_sides.add((x, "h"))
                    else:
                        num_sides.add((nx, "v"))
        return len(num_sides)


if __name__ == "__main__":
    gg = GardenGroups(r"Inputs\day12_input.txt")

    results = run_methods_in_parallel(
        gg, "find_fence_price", "find_discount_fence_price", num_processes=2
    )

    for method_name, result in results.items():
        print(f"{method_name}: {result}")
