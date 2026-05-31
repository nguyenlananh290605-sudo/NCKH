import numpy as np
from itertools import combinations
from gf2_matrix import gaussian_elimination_gf2


def generate_error_vectors(length, p):
    """Sinh tất cả các tổ hợp vector độ dài 'length' có đúng 'p' bit 1."""
    vectors = []
    for indices in combinations(range(length), p):
        v = np.zeros(length, dtype=int)
        v[list(indices)] = 1
        vectors.append(v)
    return vectors


def stern_algorithm(H, s, w, p, l, max_iter=5000):
    """
    Thuật toán Giải mã Tập thông tin của Jacques Stern (1989).
    """
    r, n = H.shape
    k = n - r

    # Ghép hội chứng s vào cột cuối của H để biến đổi cùng lúc
    H_extended = np.column_stack((H, s))

    for iteration in range(1, max_iter + 1):
        # Bước 1: Hoán vị ngẫu nhiên n cột (không hoán vị cột s)
        permutation = np.random.permutation(n)
        H_perm = H_extended.copy()
        H_perm[:, :n] = H_perm[:, permutation]

        # Bước 2: Khử Gauss trên GF(2)
        H_std, success = gaussian_elimination_gf2(H_perm, k)
        if not success:
            continue  # Thất bại -> Thử hoán vị khác

        H_prime = H_std[:, :k]
        s_prime = H_std[:, -1]

        # Bước 3: Phân chia tập thông tin (Splitting)
        half_k = k // 2
        H_X = H_prime[:, :half_k]
        H_Y = H_prime[:, half_k:]

        X_vectors = generate_error_vectors(half_k, p)
        Y_vectors = generate_error_vectors(k - half_k, p)

        # Bước 4: Tính tổng một phần và đưa vào Hash Table (trên l hàng đầu)
        hash_table = {}
        for e_X in X_vectors:
            v_X = np.dot(H_X[:l, :], e_X) % 2
            key_X = tuple(v_X)  # Chuyển mảng thành tuple để làm key
            if key_X not in hash_table:
                hash_table[key_X] = []
            hash_table[key_X].append(e_X)

        # Bước 5: Tìm kiếm va chạm (Collision Search)
        for e_Y in Y_vectors:
            v_Y = (np.dot(H_Y[:l, :], e_Y) + s_prime[:l]) % 2
            key_Y = tuple(v_Y)

            if key_Y in hash_table:
                # Phát hiện va chạm trên l bit -> Tiến hành xác thực trên toàn bộ r bit
                for e_X in hash_table[key_Y]:
                    S = (np.dot(H_X, e_X) + np.dot(H_Y, e_Y) + s_prime) % 2

                    # Kiểm tra trọng số của phần dư S
                    if np.sum(S) == w - 2 * p:
                        # Ghép nối 3 phần của vector lỗi
                        e_perm = np.concatenate((e_X, e_Y, S))

                        # Khôi phục vị trí gốc bằng cách nghịch đảo hoán vị
                        e_final = np.zeros(n, dtype=int)
                        e_final[permutation] = e_perm

                        return e_final, iteration  # Trả về kết quả và số vòng lặp

    return None, max_iter  # Vượt quá số vòng lặp cho phép