from setup import run_methods_in_parallel
from collections import deque


class ClawContraption:
    def __init__(self, file_path):
        self.file_path = file_path
        self.machines = self._read_file()

    def _read_file(self):
        machines = []
        with open(self.file_path) as f:
            machine_blocks = f.read().strip().split("\n\n")

        for block in machine_blocks:
            machine = self._parse_machine_txt(block)
            machines.append(machine)

        return machines

    def _parse_machine_txt(self, block):
        lines = block.splitlines()
        button_a = (
            lines[0].split(": ")[1].replace("X+", "").replace("Y+", "").split(", ")
        )
        button_b = (
            lines[1].split(": ")[1].replace("X+", "").replace("Y+", "").split(", ")
        )
        prize = lines[2].split(": ")[1].replace("X=", "").replace("Y=", "").split(", ")

        machine = {
            "a": {"x": int(button_a[0]), "y": int(button_a[1])},
            "b": {"x": int(button_b[0]), "y": int(button_b[1])},
            "prize": {"x": int(prize[0]), "y": int(prize[1])},
        }
        return machine

    def find_total_tokens(self):
        total_tokens = 0
        for machine in self.machines:
            total_tokens += self.find_machine_tokens(machine)
        return total_tokens

    def find_machine_tokens(self, machine):
        A = machine["a"]
        B = machine["b"]
        P = machine["prize"]

        det = A["x"] * B["y"] - A["y"] * B["x"]

        if det != 0:
            return self.solve_non_zero_determinant(A, B, P, det)
        else:
            return self.solve_zero_determinant(A, B, P)

    def solve_non_zero_determinant(self, A, B, P, det):
        a_num = P["x"] * B["y"] - P["y"] * B["x"]
        b_num = P["y"] * A["x"] - P["x"] * A["y"]

        if a_num % det == 0 and b_num % det == 0:
            a, b = a_num // det, b_num // det
            if 0 <= a <= 100 and 0 <= b <= 100:
                return 3 * a + b
        return 0

    def solve_zero_determinant(self, A, B, P):
        if A["x"] == A["y"] == 0:
            return self.solve_zero_A(B, P)
        else:
            return self.solve_non_zero_A(A, B, P)

    def solve_zero_A(self, B, P):
        if B["x"] == B["y"] == 0:
            return 0 if P["x"] == P["y"] == 0 else 0

        for coord in ["x", "y"]:
            if B[coord] != 0:
                b = P[coord] / B[coord]
                if (
                    b.is_integer()
                    and 0 <= b <= 100
                    and P["x"] == B["x"] * b
                    and P["y"] == B["y"] * b
                ):
                    return int(b)
        return 0

    def solve_non_zero_A(self, A, B, P):
        for coord in ["x", "y"]:
            if A[coord] != 0:
                for a in range(101):
                    if B[coord] != 0:
                        if (P[coord] - A[coord] * a) % B[coord] == 0:
                            b = (P[coord] - A[coord] * a) // B[coord]
                            if (
                                0 <= b <= 100
                                and A["x"] * a + B["x"] * b == P["x"]
                                and A["y"] * a + B["y"] * b == P["y"]
                            ):
                                return 3 * a + b
                    elif (
                        P[coord] - A[coord] * a == 0
                        and P["y" if coord == "x" else "x"]
                        - A["y" if coord == "x" else "x"] * a
                        == 0
                    ):
                        return 3 * a
        return 0

    def find_large_total_tokens(self):
        total_tokens = 0
        for machine in self.machines:
            total_tokens += self.find_large_machine_tokens(machine)
        return total_tokens

    def find_large_machine_tokens(self, machine):
        A_x = machine["a"]["x"]
        A_y = machine["a"]["y"]
        B_x = machine["b"]["x"]
        B_y = machine["b"]["y"]
        XP = machine["prize"]["x"] + 10000000000000
        YP = machine["prize"]["y"] + 10000000000000

        det = A_x * B_y - A_y * B_x

        if det != 0:
            a_num = XP * B_y - YP * B_x
            b_num = YP * A_x - XP * A_y
            if a_num % det == 0 and b_num % det == 0:
                a = a_num // det
                b = b_num // det
                if a >= 0 and b >= 0:
                    return 3 * a + b
            return 0
        else:
            if A_x * YP - A_y * XP != 0 or B_x * YP - B_y * XP != 0:
                return 0

            if B_x != 0 and B_y != 0:
                b_part = XP // B_x
                a_part = (YP - B_y * b_part) // A_y
                if (
                    A_x * a_part + B_x * b_part == XP
                    and A_y * a_part + B_y * b_part == YP
                ):
                    return 3 * a_part + b_part
            return 0


if __name__ == "__main__":
    file_path = "Inputs/day13_input.txt"
    cc = ClawContraption(file_path)

    results = run_methods_in_parallel(
        cc, "find_large_total_tokens", "find_total_tokens", num_processes=1
    )

    for method_name, result in results.items():
        print(f"{method_name}: {result}")
