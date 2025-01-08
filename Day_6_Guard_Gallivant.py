import copy
from multiprocessing import Pool, cpu_count
class GuardGallivant:

    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = self._read_file()
        self.starting_guard_pos = self._find_guard()

    def _read_file(self):
        grid = []
        with open(self.file_path, "r") as file:
            for line in file:
                grid.append(list(line.strip()))
        return grid

    def _find_guard(self):
        for i in range(len(self.grid[0])):
            for j in range(len(self.grid)):
                if self.grid[j][i] == "^":
                    return (i, j)

    def find_distinct_guard_pos(self):
        dirc = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dirc_idx = 0

        visited = set()
        cur_x, cur_y = self.starting_guard_pos

        while self._constraint(cur_x, cur_y):
            cur_dirc_idx = dirc_idx % 4
            dx, dy = dirc[cur_dirc_idx]

            nx, ny = cur_x + dx, cur_y + dy

            if self._constraint(nx, ny) and self.grid[ny][nx] == "#":
                dirc_idx += 1

            else:
                visited.add((cur_x, cur_y))
                cur_x, cur_y = nx, ny
        return len(visited)

    def _constraint(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def get_dir_dict(self):
        dirc = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dirc_idx = 0

        cur_x, cur_y = self.starting_guard_pos
        visited = set()
        visited_dirc_dict = {}

        while self._constraint(cur_x, cur_y):
            cur_dirc_idx = dirc_idx % 4
            dx, dy = dirc[cur_dirc_idx]

            nx, ny = cur_x + dx, cur_y + dy

            if self._constraint(nx, ny) and self.grid[ny][nx] == "#":
                dirc_idx += 1

            else:
                visited.add((cur_x, cur_y))
                visited_dirc_dict.setdefault((cur_x, cur_y), set()).add(cur_dirc_idx)
                cur_x, cur_y = nx, ny

        return visited, visited_dirc_dict

    def find_num_blocks_create_loop(self):
        visited, visited_dirc_dict = self.get_dir_dict()
        
        num_processes = cpu_count()
        visited_list = list(visited)
        chunk_size = len(visited) // num_processes
        
        chunks = [
            visited_list[i:i + chunk_size]
            for i in range(0, len(visited_list), chunk_size)
        ]
        
        with Pool(processes=num_processes) as pool:
            results = pool.map(self.process_chunk, chunks)
            
        total = sum(results)
        return total
        
        total = 0
    def process_chunk(self, chunk):
        partial_total = 0
        for x, y in chunk:
            if (x, y) == self.starting_guard_pos:
                continue

            cur_grid = copy.deepcopy(self.grid)
            cur_grid[y][x] = "#"
            partial_total += self.traverse_grid_for_loop(cur_grid)
        return partial_total

    def traverse_grid_for_loop(self, grid):
        dirc = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dirc_idx = 0

        cur_x, cur_y = self.starting_guard_pos
        visited = set()
        visited_dirc_dict = {} 

        while self._constraint(cur_x, cur_y):
            cur_dirc_idx = dirc_idx % 4 
            dx, dy = dirc[cur_dirc_idx]
            nx, ny = cur_x + dx, cur_y + dy

            if self._constraint(nx, ny) and grid[ny][nx] == "#":
                dirc_idx += 1
                continue

            if (cur_x, cur_y) in visited_dirc_dict and cur_dirc_idx in visited_dirc_dict[(cur_x, cur_y)]:
                return 1

            visited.add((cur_x, cur_y))
            visited_dirc_dict.setdefault((cur_x, cur_y), set()).add(cur_dirc_idx)
            cur_x, cur_y = nx, ny

        return 0


if __name__ == "__main__":
    gg = GuardGallivant(r"Inputs\day6_input.txt")
    total_distinct_pos = gg.find_distinct_guard_pos()
    print(total_distinct_pos)
    total_blocks_create_loop = gg.find_num_blocks_create_loop()
    print(total_blocks_create_loop)
