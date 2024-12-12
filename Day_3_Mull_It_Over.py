import re
import heapq
from collections import deque


class MullItOver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()

        self.mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
        self.do_pattern = re.compile(r"do\(\)")
        self.dont_pattern = re.compile(r"don\'t\(\)")

    def _read_file(self):
        with open(self.file_path, "r") as file:
            txt = file.read()
        return txt

    def find_mul(self):
        return sum(
            int(num1) * int(num2) for num1, num2 in self.mul_pattern.findall(self.input)
        )

    def find_mul_do_dont(self):
        do_match_idx = self._find_pattern(self.do_pattern)
        dont_match_idx = self._find_pattern(self.dont_pattern)

        heap = self._merge_lists(do_match_idx, dont_match_idx)

        total = 0
        is_do = True

        for match in self.mul_pattern.finditer(self.input):
            num1, num2 = match.groups()
            while heap and heap[0][0] < match.start():
                _, is_do = heap.popleft()

            if is_do:
                total += int(num1) * int(num2)
        return total

    def _find_pattern(self, pattern):
        return [match.start() for match in pattern.finditer(self.input)]

    def _merge_lists(self, list1, list2):
        merged_list = deque()

        l1, l2 = 0, 0

        while l1 < len(list1) and l2 < len(list2):
            if list1[l1] < list2[l2]:
                merged_list.append((list1[l1], True))
                l1 += 1
            else:
                merged_list.append((list2[l2], False))
                l2 += 1

        while l1 < len(list1):
            merged_list.append((list1[l1], True))
            l1 += 1

        while l2 < len(list2):
            merged_list.append((list2[l2], False))
            l2 += 1

        return merged_list


if __name__ == "__main__":
    file_path = "Inputs/day3_input.txt"
    calc = MullItOver(file_path)
    print(calc.find_mul())
    print(calc.find_mul_do_dont())
