from collections import deque

class PrintQueue:
    def __init__(self, file_path):
        self.file_path = file_path
        self.page_order, self.print_order = self._read_file()
        self.page_order_dict = self._get_page_order_map()
        valid_order_line_idxs = self.get_print_order_valid()
        total = self.calculate_valid_middle_sum(valid_order_line_idxs)
        print(total)
        
    def _read_file(self):
        with open(self.file_path, "r") as file:
            content = file.read()

        page_order, print_order = content.strip().split("\n\n")
        page_order = [tuple(map(int, line.split('|'))) for line in page_order.split('\n')]
        print_order = [tuple(map(int, line.split(','))) for line in print_order.split('\n')]
        
        return page_order, print_order
    
    def _get_page_order_map(self):
        page_order_dict = {}

        for pre, post in self.page_order:
            page_order_dict.setdefault(pre, set()).add(post)

        return page_order_dict
    
    def get_print_order_valid(self):
        valid_order_line_idxs = []

        for idx, order in enumerate(self.print_order):
            if self.is_order_valid(order):
                valid_order_line_idxs.append(idx)

        return valid_order_line_idxs

    def is_order_valid(self, order):
        order_set = set(order)  # Convert order to a set for faster lookups

        for j in range(len(order)):
            for k in range(j + 1, len(order)):
                pre, post = order[j], order[k]
                # Only enforce rules if both pages are in the order
                if post in self.page_order_dict.get(pre, set()):
                    if not self.is_valid(pre, post, order_set):
                        return False
        return True
    
    def is_valid(self, pre, post, order_set):
        q = deque([pre])
        seen = set([pre])

        while q:
            cur = q.popleft()
            if cur == post:
                return True

            for page in self.page_order_dict.get(cur, set()):
                if page in order_set and page not in seen:  # Only consider pages in the order
                    q.append(page)
                    seen.add(page)

        return False
    
    def calculate_valid_middle_sum(self, valid_order_line_idxs):
        total = 0
        
        for idx in valid_order_line_idxs:
            middle_index = (len(self.print_order[idx]) - 1) // 2
            total += self.print_order[idx][middle_index]
        
        return total
        

if __name__ == "__main__":
    file_path = "Inputs/day5_input.txt"
    calc = PrintQueue(file_path)