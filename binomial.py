import time
from pysat.solvers import Glucose3



def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def at_most_one(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses


def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)


def generate_clauses(n, variables):
    clauses = []

    # Exactly one queen in each row
    for i in range(n):
        exactly_one(clauses, variables[i])

    # Exactly one queen in each column
    for j in range(n):
        exactly_one(clauses, [variables[i][j] for i in range(n)])


    # At most one queen in each diagonal
    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j + k < n:
                    at_most_one(clauses, [variables[i][j], variables[i + k][j + k]])
                if i + k < n and j - k >= 0:
                    at_most_one(clauses, [variables[i][j], variables[i + k][j - k]])

    return clauses


def solve_n_queens(n):
    start_time = time.perf_counter()

    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    is_solved = solver.solve()
    solve_time = time.perf_counter() - start_time

    if is_solved:
        model = solver.get_model()
        board = [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
        solver.delete()
        return board, solve_time
    else:
        solver.delete()
        return None, solve_time


def print_solution(solution):
    if solution is None:
        print("Không tìm thấy nghiệm (UNSAT).")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


if __name__ == "__main__":
    n = int(input("Nhập kích thước N (ví dụ: 8, 16, 32, 64, 100, 128, 256): "))
    print(f"Đang giải N = {n}...")

    solution, t = solve_n_queens(n)

    print(f"\n=> Kết quả N = {n}: {'Thành công' if solution else 'Thất bại'}")
    print(f"=> Thời gian giải: {t:.4f} giây")

    if solution and n <= 16:
        print("\nBàn cờ:")
        print_solution(solution)
