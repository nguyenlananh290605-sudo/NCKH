import numpy as np


def gaussian_elimination_gf2(H, k):
    """
    Thực hiện phép khử Gauss-Jordan trên GF(2) để đưa ma trận H
    về dạng hệ thống H_std = [H' | I_{n-k}].

    Tham số:
        H (numpy.ndarray): Ma trận kiểm tra chẵn lẻ.
        k (int): Số chiều không gian thông tin.

    Trả về:
        H_std (numpy.ndarray): Ma trận đã khử (nếu thành công).
        success (bool): Trạng thái thành công/thất bại.
    """
    r, n = H.shape  # r = n - k
    H_std = H.copy() % 2

    # Ép r cột cuối cùng thành ma trận đơn vị I_{n-k}
    for i in range(r):
        target_col = k + i

        # Bước 1: Tìm phần tử chốt (Pivot) = 1
        pivot_row = -1
        for j in range(i, r):
            if H_std[j, target_col] == 1:
                pivot_row = j
                break

        # Nếu không tìm thấy chốt, cột này phụ thuộc tuyến tính -> Thất bại
        if pivot_row == -1:
            return None, False

        # Bước 2: Hoán vị hàng để đưa chốt lên đường chéo chính
        if pivot_row != i:
            H_std[[i, pivot_row]] = H_std[[pivot_row, i]]

        # Bước 3: Khử các phần tử khác trong cùng cột (dùng phép XOR)
        for j in range(r):
            if j != i and H_std[j, target_col] == 1:
                H_std[j] = (H_std[j] + H_std[i]) % 2

    return H_std, True