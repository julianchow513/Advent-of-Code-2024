class CeresSearch:
    x_mas1 = [["M", '_', "M"], ['_', 'A', '_'], ["S", '_', "S"]]
    x_mas2 = [["S", '_', "S"], ['_', 'A', '_'], ["M", '_', "M"]]
    x_mas3 = [['M', '_', 'S'], ['_', 'A', '_'], ['M', '_', 'S']]
    x_mas4 = [['S', '_', 'M'], ['_', 'A', '_'], ['S', '_', 'M']]

    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()

    def _read_file(self):
        grid = []

        with open(self.file_path, "r") as file:
            for line in file:
                grid.append(list(line.strip()))
        return grid

    def find_all_xmas(self):
        return sum([self.find_horizontal(), self.find_vertical(), self.find_major_diagonal(), self.find_anti_diagonal()])

    def find_horizontal(self):
        counter = 0

        for line in self.input:
            for i in range(len(line) - 3):
                if "".join(line[i : i + 4]) in {"XMAS", "SAMX"}:
                    counter += 1

        return counter

    def find_vertical(self):
        counter = 0

        for i in range(len(self.input[0])):
            for j in range(len(self.input) - 3):
                if self.input[j][i] + self.input[j + 1][i] + self.input[j + 2][
                    i
                ] + self.input[j + 3][i] in {"XMAS", "SAMX"}:
                    counter += 1

        return counter

    def find_major_diagonal(self):
        counter = 0
        diag = {}
        for i in range(len(self.input)):
            for j in range(len(self.input[0])):
                summ = i - j
                if summ not in diag:
                    diag[summ] = []
                diag[summ].append(self.input[i][j])
        
        for _,v in diag.items():
            if len(v) > 3:
                for i in range(len(v) - 3):
                    if v[i] + v[i+1] + v[i+2] + v[i+3] in {"XMAS", "SAMX"}:
                        counter += 1

        return counter
    
    def find_anti_diagonal(self):
        counter = 0
        diag = {}
        for i in range(len(self.input)):
            for j in range(len(self.input[0])):
                summ = i + j
                if summ not in diag:
                    diag[summ] = []
                diag[summ].append(self.input[i][j])
        
        for _,v in diag.items():
            if len(v) > 3:
                for i in range(len(v) - 3):
                    if v[i] + v[i+1] + v[i+2] + v[i+3] in {"XMAS", "SAMX"}:
                        counter += 1

        return counter
    
    def find_x_mas(self):
        counter = 0

        for i in range(1, len(self.input)-1):
            for j in range(1, len(self.input[0])-1):
                if self.input[i][j] == "A":
                    tl, bl, m, tr, br = self.input[i-1][j-1], self.input[i+1][j-1], self.input[i][j], self.input[i-1][j+1], self.input[i+1][j+1]
                    
                    cur_matrix = [[tl, '_', tr], ['_', m, '_'], [bl, '_', br]]
                    if cur_matrix in [self.x_mas1, self.x_mas2, self.x_mas3, self.x_mas4]:
                        counter += 1
        return counter

if __name__ == "__main__":
    file_path = "Inputs/day4_input.txt"
    calc = CeresSearch(file_path)
    print(calc.find_all_xmas())
    print(calc.find_x_mas())