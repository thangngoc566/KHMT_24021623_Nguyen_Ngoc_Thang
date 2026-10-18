import time
from ortools.sat.python import cp_model


def solve_n_queens_cpsat(n, timeout_sec=None):
    start_time = time.perf_counter()

    model = cp_model.CpModel()

    queens = [model.NewIntVar(0, n - 1, f"Q_{i}") for i in range(n)]

    model.AddAllDifferent(queens)

    model.AddAllDifferent([queens[i] + i for i in range(n)])
    model.AddAllDifferent([queens[i] - i for i in range(n)])

    solver = cp_model.CpSolver()
    
    status = solver.Solve(model)
    solve_time = time.perf_counter() - start_time

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        board = [[1 if solver.Value(queens[i]) == j else 0 for j in range(n)] for i in range(n)]
        return board, solve_time
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

    solution, t = solve_n_queens_cpsat(n)

    print(f"\n=> Kết quả N = {n}: {'Thành công' if solution else 'Thất bại'}")
    print(f"=> Thời gian giải: {t:.4f} giây")

    if solution and n <= 16:
        print("\nBàn cờ:")
        print_solution(solution)
