from multiprocessing import Pool, cpu_count


class RedNosedReport:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()
        self.num_processes = cpu_count()

    def _read_file(self):
        lol = []

        with open(self.file_path, "r") as file:
            for line in file:
                lol.append(list(map(int, line.strip().split())))
        return lol

    def split_chunk(self, data):
        chunk_size = len(data) // self.num_processes
        remainder = len(data) % self.num_processes

        chunks = []
        start_idx = 0

        for i in range(self.num_processes):
            end_idx = start_idx + chunk_size + (1 if i < remainder else 0)
            chunks.append(data[start_idx:end_idx])
            start_idx = end_idx

        return chunks

    def calculate_safe(self):
        chunks = self.split_chunk(self.input)
        with Pool(self.num_processes) as pool:
            results = pool.map(self.calculate_safe_chunk, chunks)

        return sum(results)

    def calculate_safe_chunk(self, chunk):
        counter = 0

        for line in chunk:
            if self.is_increasing_safe(line) or self.is_decreasing_safe(line):
                counter += 1

        return counter

    def is_increasing_safe(self, line):
        for i in range(1, len(line)):
            diff = line[i] - line[i - 1]
            if not (1 <= diff <= 3):
                return False
        return True

    def is_decreasing_safe(self, line):
        for i in range(1, len(line)):
            diff = line[i] - line[i - 1]
            if not (-3 <= diff <= -1):
                return False
        return True

    def is_safe_with_removal(self, line):
        for i in range(len(line)):
            new_line = line[:i] + line[i + 1 :]
            if self.is_increasing_safe(new_line) or self.is_decreasing_safe(new_line):
                return True
        return False

    def calc_safe_with_dampener(self):
        chunks = self.split_chunk(self.input)
        with Pool(self.num_processes) as pool:
            results = pool.map(self.calc_safe_with_dampener_chunk, chunks)

        return sum(results)

    def calc_safe_with_dampener_chunk(self, chunk):
        counter = 0

        for line in chunk:
            if self.is_safe_with_removal(line):
                counter += 1

        return counter


if __name__ == "__main__":
    report = RedNosedReport("Inputs/day2_input.txt")
    print(report.calculate_safe())
    print(report.calc_safe_with_dampener())
