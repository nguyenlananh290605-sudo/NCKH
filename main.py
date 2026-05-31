import time
import numpy as np
from generator import generate_random_matrix, generate_error_vector
from stern_isd import stern_algorithm


def run_simulation():
    print("=" * 60)
    print("MÔ PHỎNG THUẬT TOÁN STERN (TỐI ƯU THEO BÀI BÁO 1989)")
    print("=" * 60)

    # Cấu hình tham số
    n, k, w = 80, 40, 6
    p, l = 2, 8
    r = n - k

    print(f"[*] Tham số hệ thống: n={n}, k={k}, r={r}, w={w}")
    print(f"[*] Tham số Stern: p={p} (mỗi nửa), l={l} bits")

    # Khởi tạo dữ liệu
    H = generate_random_matrix(r, n)
    e_secret = generate_error_vector(n, w)
    s = (H @ e_secret) % 2

    print(f"[*] Lỗi bí mật cần tìm : {e_secret}")

    # Chạy thuật toán
    print("[*] Đang tiến hành giải mã...")
    start_time = time.time()

    e_found, iterations = stern_algorithm(H, s, w, p, l)

    elapsed_time = time.time() - start_time

    # Báo cáo kết quả
    if e_found is not None:
        print(f"\n[+] TÌM THẤY LỖI SAU {iterations} VÒNG LẶP!")
        print(f"[+] Vector tìm được  : {e_found}")
        if np.array_equal(e_found, e_secret):
            print("[+] Đánh giá         : TRÙNG KHỚP 100% với bí mật ban đầu.")
    else:
        print(f"\n[-] THẤT BẠI. Không tìm thấy sau {iterations} vòng lặp.")

    print(f"[*] Thời gian xử lý  : {elapsed_time:.4f} giây")
    print("=" * 60)


if __name__ == "__main__":
    run_simulation()