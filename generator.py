import numpy as np
import random

def generate_random_matrix(r, n):
    """Sinh ma trận nhị phân H ngẫu nhiên kích thước r x n."""
    return np.random.randint(0, 2, size=(r, n), dtype=int)

def generate_error_vector(n, w):
    """Sinh vector lỗi e độ dài n, có trọng số Hamming đúng bằng w."""
    e = np.zeros(n, dtype=int)
    # Chọn ngẫu nhiên w vị trí để bật bit 1
    error_positions = random.sample(range(n), w)
    for pos in error_positions:
        e[pos] = 1
    return e

def compute_syndrome(H, e):
    """Tính vector hội chứng s = H * e^T (modulo 2)."""
    return np.dot(H, e) % 2