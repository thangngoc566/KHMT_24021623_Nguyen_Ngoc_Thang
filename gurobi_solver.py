import time
import gurobipy as gp
from gurobipy import GRB


def solve_n_queens_gurobi(n, timeout_sec=None):
    
    start_time = time.perf_counter()
    try:
        env = gp.Env(empty=True)
        env.setParam("OutputFlag", 0)  
        env.start()
        model = gp.Model("NQueens_Gurobi", env=env)
    except gp.GurobiError:
        model = gp.Model("NQueens_Gurobi")
        model.setParam("OutputFlag", 0)

    model.setParam("MIPFocus", 1)  

    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1, name=f"row_{i}")

    for j in range(n):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1, name=f"col_{j}")

    for k in range(-(n - 1), n):
        diag1 = [x[i, i - k] for i in range(max(0, k), min(n, n + k))]
        if len(diag1) > 1:
            model.addConstr(gp.quicksum(diag1) <= 1, name=f"diag1_{k}")

    for k in range(2 * n - 1):
        diag2 = [x[i, k - i] for i in range(max(0, k - n + 1), min(n, k + 1))]
        if len(diag2) > 1:
            model.addConstr(gp.quicksum(diag2) <= 1, name=f"diag2_{k}")

    model.optimize()
    solve_time = time.perf_counter() - start_time

    if model.status == GRB.OPTIMAL:
        board = [[int(x[i, j].X > 0.5) for j in range(n)] for i in range(n)]
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

    solution, t = solve_n_queens_gurobi(n)

    print(f"\n=> Kết quả N = {n}: {'Thành công' if solution else 'Thất bại'}")
    print(f"=> Thời gian giải: {t:.4f} giây")

    if solution and n <= 16:
        print("\nBàn cờ:")
        print_solution(solution)
