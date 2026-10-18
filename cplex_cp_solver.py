import time
from docplex.cp.model import CpoModel

def solve_n_queens_cplex_cp(n, timeout_sec=None):
    
    start_time = time.perf_counter()

    mdl = CpoModel(name="NQueens_CPLEX_CP")

    queens = [mdl.integer_var(0, n - 1, name=f"Q_{i}") for i in range(n)]

    mdl.add(mdl.all_diff(queens))

    mdl.add(mdl.all_diff([queens[i] + i for i in range(n)]))
    mdl.add(mdl.all_diff([queens[i] - i for i in range(n)]))

    try:
        res = mdl.solve(Workers=1, LogVerbosity="Quiet")
    except Exception as e:
        solve_time = time.perf_counter() - start_time
        if "limit" in str(e).lower():
            return None, solve_time, "LIMIT"
        return None, solve_time, f"ERROR: {type(e).__name__}"

    solve_time = time.perf_counter() - start_time

    if res and res.is_solution():
        board = [[1 if res.get_value(queens[i]) == j else 0 for j in range(n)] for i in range(n)]
        return board, solve_time
    else:
        return None, solve_time


def print_solution(solution):
    if solution is None:
        print("Không tìm thấy nghiệm.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


if __name__ == "__main__":
    n = int(input("Nhập kích thước N (ví dụ: 8, 16, 32, 64, 100, 128, 256): "))
    print(f"Đang giải N = {n}...")

    solution, t = solve_n_queens_cplex_cp(n)

    print(f"\n=> Kết quả N = {n}: {'Thành công' if solution else 'Thất bại'}")
    print(f"=> Thời gian giải: {t:.4f} giây")

    if solution and n <= 16:
        print("\nBàn cờ:")
        print_solution(solution)
