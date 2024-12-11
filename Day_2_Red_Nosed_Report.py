class RedNosedReport:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()
    
    def _read_file(self):
        lol = []

        with open(self.file_path, 'r') as file:
            for line in file:
                lol.append(list(map(int, line.strip().split())))
        return lol
    
    def calculate_safe(self):
        counter = 0

        for line in self.input:
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
            new_line = line[:i] + line[i+1:]
            if self.is_increasing_safe(new_line) or self.is_decreasing_safe(new_line):
                return True
        return False
    
    def calc_safe_with_dampener(self):
        counter = 0

        for line in self.input:
            if self.is_safe_with_removal(line):
                counter += 1
            
        return counter

if __name__ == "__main__":
    report = RedNosedReport('Inputs/day2_input.txt')
    print(report.calculate_safe())
    print(report.calc_safe_with_dampener())