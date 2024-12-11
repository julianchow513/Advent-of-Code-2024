class HistorianHysteria:
    def __init__(self, file_path):
        self.file_path = file_path
        self.list1, self.list2 = self._read_file()
    
    def _read_file(self):
        list1 = []
        list2 = []

        with open(self.file_path, 'r') as file:
            for line in file:
                num1, num2 = (int(x) for x in line.split())
                list1.append(num1)
                list2.append(num2)

        return list1, list2
    
    def calculate_total(self):
        sorted_list1 = sorted(self.list1)
        sorted_list2 = sorted(self.list2)
        
        return sum(abs(a - b) for a, b in zip(sorted_list1, sorted_list2))

    def calculate_similarity(self):
        counter_2 = {}

        for num in self.list2:
            counter_2[num] = counter_2.get(num, 0) + 1

        similarity = 0
        for num in self.list1:
            similarity += num * counter_2.get(num, 0)

        return similarity

if __name__ == "__main__":
    file_path = 'Inputs/day1_input.txt'
    calc = HistorianHysteria(file_path)
    total = calc.calculate_total()
    similarity = calc.calculate_similarity()
    print('Total:', total)
    print("Similarity:", similarity)