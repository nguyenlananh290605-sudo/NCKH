import time
import numpy as np
from generator import generate_random_matrix, generate_error_vector
from stern_isd import stern_algorithm


def run_experiment(n, k, w, p, l, num_trials=3):
    """Hàm chạy thử nghiệm nhiều lần và lấy trung bình"""
    total_time = 0
    total_iters = 0
    success_count = 0

    for _ in range(num_trials):
        # Sinh dữ liệu mới cho mỗi lần thử
        H = generate_random_matrix(n - k, n)
        e_secret = generate_error_vector(n, w)
        s = (np.dot(H, e_secret) % 2).astype(np.uint8)

        start_time = time.time()
        # Chạy tối đa 10000 vòng lặp để tránh treo máy quá lâu
        e_found, iters = stern_algorithm(H, s, w, p, l, max_iter=10000)
        elapsed = time.time() - start_time

        total_time += elapsed
        total_iters += iters
        if e_found is not None:
            success_count += 1

    avg_time = total_time / num_trials
    avg_iters = total_iters / num_trials
    return avg_time, avg_iters, success_count


def main():
    print("=" * 60)
    print("CHẠY THỰC NGHIỆM ĐÁNH GIÁ HIỆU NĂNG THUẬT TOÁN STERN")
    print("=" * 60)

    # ---------------------------------------------------------
    print("\n[KỊCH BẢN 1]: Đánh giá ảnh hưởng của tham số p (So sánh với Prange)")
    print("Cố định: n=100, k=50, w=10, l=8")
    print("{:<10} | {:<15} | {:<15}".format("Tham số p", "T.Gian TB (s)", "Số vòng lặp TB"))
    print("-" * 45)
    for p in [0, 1, 2]:  # p=0 chính là thuật toán Prange cổ điển
        avg_t, avg_i, succ = run_experiment(100, 50, 10, p, 8, num_trials=3)
        print("{:<10} | {:<15.4f} | {:<15.1f}".format(f"p = {p}", avg_t, avg_i))

    # ---------------------------------------------------------
    print("\n[KỊCH BẢN 2]: Sự đánh đổi của Cửa sổ va chạm l")
    print("Cố định: n=120, k=60, w=12, p=2")
    print("{:<10} | {:<15} | {:<15}".format("Tham số l", "T.Gian TB (s)", "Số vòng lặp TB"))
    print("-" * 45)
    for l in [4, 8, 12, 16]:
        avg_t, avg_i, succ = run_experiment(120, 60, 12, 2, l, num_trials=3)
        print("{:<10} | {:<15.4f} | {:<15.1f}".format(f"l = {l}", avg_t, avg_i))

    # ---------------------------------------------------------
    print("\n[KỊCH BẢN 3]: Sự bùng nổ độ phức tạp khi tăng n (Scalability)")
    print("Cố định: R=1/2 (k=n/2), tỷ lệ lỗi 10% (w=n/10), p=2, l=8")
    print("{:<25} | {:<15} | {:<15}".format("Cấu hình (n, k, w)", "T.Gian TB (s)", "Số vòng lặp TB"))
    print("-" * 60)
    configs = [
        (60, 30, 6),
        (80, 40, 8),
        (100, 50, 10),
        (120, 60, 12)
    ]
    for (n, k, w) in configs:
        avg_t, avg_i, succ = run_experiment(n, k, w, 2, 8, num_trials=3)
        print("{:<25} | {:<15.4f} | {:<15.1f}".format(f"n={n}, k={k}, w={w}", avg_t, avg_i))

    print("\nHOÀN THÀNH!")


if __name__ == "__main__":
    main()