from math import prod
from setup import run_methods_in_parallel
class BridgeRepair:
    def __init__(self, file_path):
        self.file_path = file_path
        self.totals, self.values = self._read_file()

    def _read_file(self):
        values = []
        totals = []
        with open(self.file_path) as f:
            for line in f:
                tot, val = line.split(':')
                totals.append(int(tot))
                values.append([int(x) for x in val.split()])

        return totals, values
    
    def find_valid_sum(self):
        valid_idx = self.find_valid_idx()
        return sum(self.totals[i] for i in valid_idx)
    
    def find_valid_idx(self):
        valid_idx = []
        
        for i in range(len(self.totals)):
            tot, vals = self.totals[i], self.values[i]
            if sum(vals) == tot:
                valid_idx.append(i)
            elif prod(vals) == tot:
                valid_idx.append(i)
            elif self.is_valid(tot, vals):
                valid_idx.append(i)
        
        return valid_idx
                
    def is_valid(self, tot, vals):
        def backtrack(idx, cur_val):
            if idx == len(vals):
                if cur_val == tot:
                    return True
                return False
            
            num = vals[idx]
            if cur_val > tot:
                return False
            
            if backtrack(idx + 1, cur_val + num):
                return True
            if idx > 0 and backtrack(idx + 1, cur_val * num):
                return True
            
            return False
    
        return backtrack(0, 0)
    
    def find_valid_sum_three_op(self):
        valid_idx = self.find_valid_idx_to()
        return sum(self.totals[i] for i in valid_idx)
    
    def find_valid_idx_to(self):
        valid_idx = []
        
        for i in range(len(self.totals)):
            tot, vals = self.totals[i], self.values[i]
            if sum(vals) == tot:
                valid_idx.append(i)
            elif prod(vals) == tot:
                valid_idx.append(i)
            elif self.concatenate(vals) == tot:
                valid_idx.append(i)
            elif self.is_valid_to(tot, vals):
                valid_idx.append(i)
        
        return valid_idx
    
    def concatenate(self, vals):
        res = str(vals[0])
        
        for i in range(1, len(vals)):
            res = res + str(vals[i])
        
        return int(res)

    def is_valid_to(self, tot, vals):
        def backtrack(idx, cur_val):
            if idx == len(vals):
                if cur_val == tot:
                    return True
                return False
            
            num = vals[idx]
            if cur_val > tot:
                return False
            
            if backtrack(idx + 1, cur_val + num):
                return True
            if idx > 0 and backtrack(idx + 1, cur_val * num):
                return True
            if idx > 0 and backtrack(idx + 1, int(str(cur_val) + str(num))):
                return True
            
            return False
    
        return backtrack(0, 0)
        
if __name__ == "__main__":
    # Create an instance of the BridgeRepair class
    br = BridgeRepair("Inputs/day7_input.txt")

    # Run methods in parallel
    results = run_methods_in_parallel(
        br,
        "find_valid_sum",
        "find_valid_sum_three_op",
        num_processes=2  # Use 2 processes
    )

    # Print the results
    for method_name, result in results.items():
        print(f"{method_name}: {result}")