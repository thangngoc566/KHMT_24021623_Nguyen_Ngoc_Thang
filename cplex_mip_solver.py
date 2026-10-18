import time
from docplex.mp.model import Model


def solve_n_queens_cplex_mip(n, timeout_sec=None):
    
    start_time = time.perf_counter()

    mdl = Model("NQueens_CPLEX_MIP")
    mdl.parameters.emphasis.mip = 1  
    mdl.context.solver.log_output = False

    try:
        x = mdl.binary_var_matrix(n, n, name="x")

        constrs = []
        constrs.extend(mdl.sum(x[i, j] for j in range(n)) == 1 for i in range(n))
        constrs.extend(mdl.sum(x[i, j] for i in range(n)) == 1 for j in range(n))

        for k in range(-(n - 1), n):
            diag = [x[i, i - k] for i in range(max(0, k), min(n, n + k))]
            if len(diag) > 1:
                constrs.append(mdl.sum(diag) <= 1)

        for k in range(2 * n - 1):
            diag = [x[i, k - i] for i in range(max(0, k - n + 1), min(n, k + 1))]
            if len(diag) > 1:
                constrs.append(mdl.sum(diag) <= 1)

        mdl.add_constraints(constrs)

        solution = mdl.solve(log_output=False)
        solve_time = time.perf_counter() - start_time

        if solution:
            board = [[int(solution.get_value(x[i, j]) > 0.5) for j in range(n)] for i in range(n)]
            return board, solve_time
        else:
            return None, solve_time
    except Exception as e:
        solve_time = time.perf_counter() - start_time
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

    solution, t = solve_n_queens_cplex_mip(n)

    print(f"\n=> Kết quả N = {n}: {'Thành công' if solution else 'Thất bại'}")
    print(f"=> Thời gian giải: {t:.4f} giây")

    if solution and n <= 16:
        print("\nBàn cờ:")
        print_solution(solution)
