from setup import run_methods_in_parallel
from collections import defaultdict

class DiskFragmenter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input = self._read_file()
        self.decompressed = self._decompress_input()
    
    def _read_file(self):
        with open(self.file_path, "r") as file:
            return list(file.read().strip())
        
    def _decompress_input(self):
        decompressed = []
        cur_id = 0
        for i in range(len(self.input)):
            if i % 2 == 0:
                decompressed.extend([str(cur_id) for _ in range(int(self.input[i]))])
                cur_id += 1
            else:
                decompressed.extend(['.' for _ in range(int(self.input[i]))])
        return decompressed
    
    def find_checksum(self):
        swapped_decompressed = self._swap_free_space()
        return sum(idx * int(val) for idx, val in enumerate(swapped_decompressed) if val != '.')
    
    def _swap_free_space(self):
        decompressed = self.decompressed.copy()
        r, l = 0, len(decompressed) - 1
        while r < l:
            while r < l and decompressed[r] != '.':
                r += 1
            while r < l and decompressed[l] == '.':
                l -= 1
            if r < l:
                decompressed[r], decompressed[l] = decompressed[l], decompressed[r]
                r += 1
                l -= 1
        return decompressed
    
    def find_group_checksum(self):
        decompressed = self._group_swap_free_space()
        checksum = sum(idx * int(val) for idx, val in enumerate(decompressed) if val != '.')
        return checksum
    
    def _group_swap_free_space(self):
        decompressed = self.decompressed.copy()
        files, free_spaces = self._parse_decompressed(decompressed)
        
        # Sort files by ID descending
        files_sorted = sorted(files, key=lambda x: -x['id'])
        
        # Sort free spaces by start ascending
        free_spaces_sorted = sorted(free_spaces, key=lambda x: x['start'])
        
        for file in files_sorted:
            candidate = None
            for i, fs in enumerate(free_spaces_sorted):
                if fs['size'] >= file['size'] and fs['start'] < file['start']:
                    candidate = i
                    break  # First suitable free space is the leftmost
            if candidate is not None:
                fs = free_spaces_sorted[candidate]
                # Move the file to the free space
                for j in range(fs['start'], fs['start'] + file['size']):
                    decompressed[j] = str(file['id'])
                for j in range(file['start'], file['start'] + file['size']):
                    decompressed[j] = '.'
                
                # Remove the selected free space
                del free_spaces_sorted[candidate]
                
                # Add the new free space (file's original position)
                new_fs = {'start': file['start'], 'size': file['size']}
                # Insert it in the correct position
                inserted = False
                for k in range(len(free_spaces_sorted)):
                    if free_spaces_sorted[k]['start'] > new_fs['start']:
                        free_spaces_sorted.insert(k, new_fs)
                        inserted = True
                        break
                if not inserted:
                    free_spaces_sorted.append(new_fs)
                
                # Merge with previous free space if possible
                if len(free_spaces_sorted) > 1:
                    k = -1
                    for m in range(len(free_spaces_sorted)):
                        if free_spaces_sorted[m]['start'] == new_fs['start']:
                            k = m
                            break
                    if k > 0 and free_spaces_sorted[k-1]['start'] + free_spaces_sorted[k-1]['size'] == free_spaces_sorted[k]['start']:
                        # Merge with previous
                        merged_fs = {'start': free_spaces_sorted[k-1]['start'], 'size': free_spaces_sorted[k-1]['size'] + free_spaces_sorted[k]['size']}
                        del free_spaces_sorted[k]
                        del free_spaces_sorted[k-1]
                        free_spaces_sorted.insert(k-1, merged_fs)
                        k -= 1
                    # Merge with next free space if possible
                    if k < len(free_spaces_sorted)-1 and free_spaces_sorted[k]['start'] + free_spaces_sorted[k]['size'] == free_spaces_sorted[k+1]['start']:
                        # Merge with next
                        merged_fs = {'start': free_spaces_sorted[k]['start'], 'size': free_spaces_sorted[k]['size'] + free_spaces_sorted[k+1]['size']}
                        del free_spaces_sorted[k+1]
                        del free_spaces_sorted[k]
                        free_spaces_sorted.insert(k, merged_fs)
        
        return decompressed
    
    def _parse_decompressed(self, decompressed):
        files = []
        free_spaces = []
        i = 0
        n = len(decompressed)
        while i < n:
            if decompressed[i] != '.':
                # File block
                file_id = int(decompressed[i])
                j = i
                while j < n and decompressed[j] == str(file_id):
                    j += 1
                file_size = j - i
                files.append({'id': file_id, 'start': i, 'size': file_size})
                i = j
            else:
                # Free space
                j = i
                while j < n and decompressed[j] == '.':
                    j += 1
                free_size = j - i
                free_spaces.append({'start': i, 'size': free_size})
                i = j
        return files, free_spaces

if __name__ == "__main__":
    df = DiskFragmenter("Inputs/day9_input.txt")
    
    results = run_methods_in_parallel(df, "find_checksum", "find_group_checksum", num_processes=2)
    
    for method_name, result in results.items():
        print(f"{method_name}: {result}")