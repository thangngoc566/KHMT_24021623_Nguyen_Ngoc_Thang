# BTL1 - Các vấn đề hiện đại của Khoa học máy tính

## Giới thiệu

Đây là toàn bộ mã nguồn và dữ liệu thực nghiệm phục vụ **Bài tập lớn số 1** của học phần **Các vấn đề hiện đại của Khoa học máy tính (INT3011E)**.

Đề tài tập trung vào việc mô hình hóa và giải bài toán **N-Queens** bằng phương pháp **SAT (Boolean Satisfiability Problem)**, đồng thời đặt lên bàn cân so sánh với các phương pháp Quy hoạch nguyên (ILP/MIP) và Lập trình ràng buộc (CP). Mục tiêu của chương trình là xây dựng các mô hình toán học khác nhau cho bài toán, chuyển đổi các ràng buộc thành công thức logic chuẩn hội (CNF), sau đó sử dụng bộ giải SAT và các bộ giải tối ưu hóa để tìm nghiệm.

Trong dự án, bài toán được cài đặt và thực nghiệm với ba phương pháp mã hóa ràng buộc *At-Most-One (AMO)* chính cho SAT:
* **Binomial (Pairwise) Encoding**
* **Binary Encoding**
* **Commander Encoding**

Bên cạnh bộ giải SAT (**Glucose3** thông qua thư viện `PySAT`), kết quả còn được đối chiếu thực nghiệm với các bộ giải công nghiệp hàng đầu:
* **CPLEX CP** & **OR-Tools (CP-SAT)** (nhóm Lập trình ràng buộc)
* **CPLEX MIP** & **Gurobi** (nhóm Quy hoạch nguyên hỗn hợp)

Các phương pháp encoding và mô hình hóa được sử dụng để biểu diễn các ràng buộc hàng, cột và đường chéo của bài toán N-Queens, từ đó đánh giá sự đánh đổi giữa không gian biểu diễn và hiệu năng giải thực tế.