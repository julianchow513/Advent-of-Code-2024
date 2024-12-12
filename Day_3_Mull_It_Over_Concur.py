import re
import multiprocessing

class MullItOver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()
        
        self.mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
        self.do_pattern = re.compile(r"do\(\)")
        self.dont_pattern = re.compile(r"don\'t\(\)")

    def _read_file(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def find_mul(self):
        matches = self.mul_pattern.findall(self.input)
        return sum(int(num1) * int(num2) for num1, num2 in matches)

    def find_mul_do_dont(self):
        do_match_idx = self._find_pattern(self.do_pattern)
        dont_match_idx = self._find_pattern(self.dont_pattern)
        
        merged_list = []
        l1, l2 = 0, 0
        while l1 < len(do_match_idx) and l2 < len(dont_match_idx):
            if do_match_idx[l1] < dont_match_idx[l2]:
                merged_list.append((do_match_idx[l1], True))
                l1 += 1
            else:
                merged_list.append((dont_match_idx[l2], False))
                l2 += 1
        
        merged_list.extend((idx, True) for idx in do_match_idx[l1:])
        merged_list.extend((idx, False) for idx in dont_match_idx[l2:])
        
        merged_list.sort()
        
        total = 0
        is_do = True
        current_idx = 0
        
        for match in self.mul_pattern.finditer(self.input):
            while current_idx < len(merged_list) and merged_list[current_idx][0] < match.start():
                _, is_do = merged_list[current_idx]
                current_idx += 1
            
            if is_do:
                num1, num2 = match.groups()
                total += int(num1) * int(num2)
        
        return total

    def _find_pattern(self, pattern):
        return [match.start() for match in pattern.finditer(self.input)]

    def parallel_process(self):
        with multiprocessing.Pool(processes=2) as pool:
            results = pool.map(self._process_method, 
                               ['find_mul', 'find_mul_do_dont'])
        return results

    def _process_method(self, method_name):
        return getattr(self, method_name)()

if __name__ == "__main__":
    file_path = "Inputs/day3_input.txt"
    calc = MullItOver(file_path)
    
    mul_result, mul_do_dont_result = calc.parallel_process()
    print(mul_result)
    print(mul_do_dont_result)