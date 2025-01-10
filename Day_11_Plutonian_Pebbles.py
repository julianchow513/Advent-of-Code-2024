from setup import run_methods_in_parallel
import copy
import math
import cupy as cp


class PlutonianPebbles:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()
        self.gpu_input = cp.array(self.input, dtype=cp.int64)

    def _read_file(self):
        with open(self.file_path, "r") as file:
            return list(map(int, file.read().split(" ")))

    def blink_25(self):
        stones = copy.deepcopy(self.input)
        for _ in range(25):
            stones = self.blink(stones)
        return len(stones)

    def blink(self, stones):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            else:
                num_digits = math.floor(math.log10(stone)) + 1
                if num_digits % 2 == 0:
                    mid = num_digits // 2
                    l = stone // 10**mid
                    r = stone % 10**mid
                    new_stones.append(l)
                    new_stones.append(r)
                else:
                    new_stones.append(stone * 2024)
        return new_stones

    def blink_gpu(self, stones, counts):
        mask_zero = stones == 0
        new_stones_zero = cp.ones_like(stones[mask_zero])
        new_counts_zero = counts[mask_zero]

        mask_non_zero = stones != 0
        non_zero_stones = stones[mask_non_zero]
        non_zero_counts = counts[mask_non_zero]

        num_digits = cp.floor(cp.log10(non_zero_stones)) + 1
        num_digits = cp.maximum(num_digits, 1)

        mask_even = num_digits % 2 == 0
        even_stones = non_zero_stones[mask_even]
        even_counts = non_zero_counts[mask_even]
        mid = (num_digits[mask_even].astype(cp.int64)) // 2
        ten_pow_mid = 10**mid
        l = even_stones // ten_pow_mid
        r = even_stones % ten_pow_mid
        new_stones_even = cp.concatenate((l, r))
        new_counts_even = cp.concatenate((even_counts, even_counts))

        mask_odd = num_digits % 2 != 0
        odd_stones = non_zero_stones[mask_odd]
        odd_counts = non_zero_counts[mask_odd]
        new_stones_odd = odd_stones * 2024
        new_counts_odd = odd_counts

        new_stones = cp.concatenate((new_stones_zero, new_stones_even, new_stones_odd))
        new_counts = cp.concatenate((new_counts_zero, new_counts_even, new_counts_odd))

        sorted_indices = cp.argsort(new_stones)
        sorted_new_stones = new_stones[sorted_indices]
        sorted_new_counts = new_counts[sorted_indices]

        diff_new = cp.diff(sorted_new_stones)
        unique_new = cp.concatenate((sorted_new_stones[:1], sorted_new_stones[1:][diff_new != 0]))
        indices = cp.searchsorted(unique_new, sorted_new_stones)
        counts_sum = cp.bincount(indices, weights=sorted_new_counts, minlength=len(unique_new))

        return unique_new, counts_sum

    def blink_75(self):
        unique_stones, counts = cp.unique(self.input, return_counts=True)
        for _ in range(75):
            unique_stones, counts = self.blink_gpu(unique_stones, counts)
        total_stones = cp.sum(counts)
        return int(total_stones.item())


if __name__ == "__main__":
    pp = PlutonianPebbles(r"Inputs\day11_input.txt")

    results = run_methods_in_parallel(pp, "blink_25", "blink_75", num_processes=2)

    for method_name, result in results.items():
        print(f"{method_name}: {result}")
