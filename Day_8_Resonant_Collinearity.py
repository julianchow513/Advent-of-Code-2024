from setup import run_methods_in_parallel
import math


class Resonant_Collinearity:
    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = self._read_file()
        self.ant_dict = self._find_antennas()

    def _read_file(self):
        grid = []

        with open(self.file_path, "r") as file:
            for line in file:
                grid.append(list(line.strip()))
        return grid

    def _find_antennas(self):
        ant_dict = {}

        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                if val != ".":
                    ant_dict.setdefault(val, []).append((x, y))

        return ant_dict

    def _constraint(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def find_num_antinodes(self):
        antinodes = set()

        for ant_positions in self.ant_dict.values():
            for i, (x, y) in enumerate(ant_positions):
                for ax, ay in ant_positions[i + 1 :]:
                    nx, ny = self._reflect_antennas(x, y, ax, ay)
                    if self._constraint(nx, ny):
                        antinodes.add((nx, ny))

                    nx, ny = self._reflect_antennas(ax, ay, x, y)
                    if self._constraint(nx, ny):
                        antinodes.add((nx, ny))

        return len(antinodes)

    def _reflect_antennas(self, x, y, ax, ay):
        return 2 * x - ax, 2 * y - ay

    def find_num_antinodes_with_t_freq(self):
        antinodes = set()

        for ant_positions in self.ant_dict.values():
            for i, (x, y) in enumerate(ant_positions):
                for ax, ay in ant_positions[i + 1 :]:
                    t_antinodes = self.find_t_freq_antinodes(x, y, ax, ay)
                    antinodes.update(t_antinodes)

        return len(antinodes)

    def _find_distance(self, x, y, ax, ay):
        return x - ax, y - ay

    def find_t_freq_antinodes(self, x, y, ax, ay):
        antinodes = {(x, y)}

        nx, ny = self._find_distance(x, y, ax, ay)
        gcd = math.gcd(nx, ny)
        dx, dy = nx // gcd, ny // gcd

        for direction in (1, -1):
            cur_x, cur_y = x + direction * dx, y + direction * dy
            while self._constraint(cur_x, cur_y):
                antinodes.add((cur_x, cur_y))
                cur_x, cur_y = cur_x + direction * dx, cur_y + direction * dy

        return antinodes


if __name__ == "__main__":
    rc = Resonant_Collinearity("Inputs/day8_input.txt")

    # Run methods in parallel
    results = run_methods_in_parallel(
        rc, "find_num_antinodes", "find_num_antinodes_with_t_freq", num_processes=2
    )

    # Print the results
    for method_name, result in results.items():
        print(f"{method_name}: {result}")
