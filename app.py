import streamlit as st
import numpy as np
import time
from generator import generate_random_matrix, generate_error_vector
from stern_isd import stern_algorithm  # Dùng hàm tối ưu

st.set_page_config(page_title="Stern Algorithm Demo", layout="wide")

st.title("🛡️ Mô phỏng thuật toán Jacques Stern (ISD)")
st.markdown("Đồ án tìm kiếm từ mã trọng số nhỏ dựa trên Nghịch lý ngày sinh.")

# --- KHỞI TẠO SESSION STATE ---
if "problem_generated" not in st.session_state:
    st.session_state.problem_generated = False

# --- BẢNG ĐIỀU KHIỂN ---
st.sidebar.header("1. Tạo Bài Toán (Hệ Mật)")
n = st.sidebar.number_input("Độ dài mã (n)", min_value=10, max_value=200, value=60, step=10)
k = st.sidebar.number_input("Kích thước thông tin (k)", min_value=5, max_value=100, value=30, step=5)
w = st.sidebar.number_input("Trọng số lỗi (w)", min_value=1, max_value=20, value=4, step=1)

if st.sidebar.button("🎲 Sinh Bài Toán Mới"):
    if k >= n:
        st.sidebar.error("Lỗi: k phải nhỏ hơn n")
    else:
        st.session_state.r = n - k
        st.session_state.H = generate_random_matrix(st.session_state.r, n)
        st.session_state.e_secret = generate_error_vector(n, w)
        st.session_state.s = (np.dot(st.session_state.H, st.session_state.e_secret) % 2).astype(np.uint8)
        st.session_state.problem_generated = True
        st.sidebar.success("Đã tạo bài toán mới!")

st.sidebar.markdown("---")
st.sidebar.header("2. Tham số Giải mã Stern")
p = st.sidebar.slider("Lỗi mỗi nửa tập thông tin (p)", min_value=0, max_value=w, value=1)
l = st.sidebar.slider("Kích thước cửa sổ va chạm (l)", min_value=1, max_value=20, value=6)

# Cảnh báo Logic
if 2 * p > w:
    st.sidebar.warning(f"Cảnh báo: 2*p ({2 * p}) lớn hơn w ({w}). Thuật toán khó tìm ra nghiệm.")

# --- KHU VỰC CHÍNH ---
if st.session_state.problem_generated:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dữ liệu Bài toán")
        st.write(f"**Ma trận kiểm tra H** ({st.session_state.r}x{n}):")
        st.dataframe(st.session_state.H, height=200)

    with col2:
        st.subheader("Bí mật (Vector lỗi e)")
        st.write(f"Trọng số w={w}")
        st.code(str(st.session_state.e_secret))
        # Vẽ biểu đồ hiển thị vị trí lỗi
        st.bar_chart(st.session_state.e_secret, height=150)

    st.divider()

    if st.button("🚀 Bắt đầu Giải mã Stern", type="primary"):
        with st.spinner("Đang chạy thuật toán giải mã..."):
            start_time = time.time()
            # Gọi hàm giải mã
            e_found, iterations = stern_algorithm(
                st.session_state.H,
                st.session_state.s,
                w, p, l, max_iter=5000
            )
            elapsed_time = time.time() - start_time

        st.subheader("Báo cáo Kết quả")
        if e_found is not None:
            st.success("✅ THÀNH CÔNG! Thuật toán đã tìm ra vector lỗi.")

            m1, m2, m3 = st.columns(3)
            m1.metric("Thời gian tính toán", f"{elapsed_time:.4f} giây")
            m2.metric("Số vòng lặp", f"{iterations} vòng")

            if np.array_equal(e_found, st.session_state.e_secret):
                m3.metric("Độ chính xác", "100% (Khớp bí mật)")
            else:
                m3.metric("Độ chính xác", "Nghiệm tương đương")

            st.write("**Vị trí lỗi tìm được:**")
            st.bar_chart(e_found, height=150)
            st.balloons()
        else:
            st.error(f"❌ THẤT BẠI: Vượt quá {iterations} vòng lặp.")
else:
    st.info("👈 Hãy nhấn 'Sinh Bài Toán Mới' ở thanh điều khiển bên trái để bắt đầu.")