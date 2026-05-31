# Nghiên cứu Thuật toán Xác suất Stern (Jacques Stern's ISD)
> **Đồ án/Tiểu luận Nghiên cứu Khoa học**  
> **Chủ đề:** Phương Pháp Tìm Từ Mã Có Trọng Số Nhỏ (Syndrome Decoding Problem - SDP) trong Mật mã học Hậu lượng tử (Post-Quantum Cryptography).  
> **Tác giả:** Nguyễn Thị Lan Anh (MSV: 23001826)  
> **Đơn vị:** Khoa Toán – Cơ – Tin học, Trường Đại học Khoa học Tự nhiên, ĐHQGHN  
> **Giáo viên hướng dẫn:** GV. Mạc Đăng Trường  

---

## 📌 Giới thiệu dự án

Dự án này tập trung nghiên cứu và hiện thực hóa **Thuật toán Giải mã Tập thông tin của Jacques Stern (1989)** (Information Set Decoding - ISD) bằng ngôn ngữ **Python + NumPy**. Thuật toán Stern là một trong những thuật toán xác suất hiệu quả nhất dùng để giải bài toán **Syndrome Decoding Problem (SDP)** (NP-Khó), vốn là nền tảng an toàn của các hệ mật mã dựa trên mã sửa sai (Code-based Cryptography) tiêu biểu như **McEliece**.

Dự án bao gồm:
1. **Lõi thuật toán Stern (ISD)** tối ưu hóa bằng phương pháp va chạm bảng băm (Meet-in-the-Middle) và phân hoạch tập thông tin.
2. **Ứng dụng Web tương tác (Streamlit)** để trực quan hóa quá trình sinh lỗi, chạy thuật toán và so sánh hiệu năng.
3. **Mã nguồn thực nghiệm (Benchmark)** so sánh hiệu năng giữa thuật toán Prange cổ điển ($p=0$) và Stern ($p > 0$), khảo sát độ phức tạp tính toán khi tăng độ dài mã $n$.
4. **Poster nghiên cứu khoa học chuyên nghiệp (A2)** dạng HTML/CSS kèm công cụ kết xuất tự động ra PDF và PNG bằng Playwright.

---

## 📂 Cấu trúc mã nguồn

Dưới đây là sơ đồ và mô tả các tệp tin chính trong thư mục [d:/NCKH](file:///d:/NCKH):

| Tên Tệp tin | Vai trò / Chức năng |
| :--- | :--- |
| 🛡️ [stern_isd.py](file:///d:/NCKH/stern_isd.py) | **Lõi thuật toán giải mã Stern**. Thực hiện việc hoán vị cột ngẫu nhiên, tìm tập thông tin sạch lỗi thông qua khử Gauss, tạo vector lỗi bán phần, tính toán va chạm bảng băm trên cửa sổ $l$-bit và kiểm tra trọng số lỗi toàn cục. |
| 🧮 [gf2_matrix.py](file:///d:/NCKH/gf2_matrix.py) | Các phép tính toán trên trường hữu hạn $\mathbb{F}_2$. Bao gồm hàm khử Gauss-Jordan để đưa ma trận chẵn lẻ $H$ về dạng chuẩn (systematic form) $[H' \mid I_{n-k}]$. |
| 🎲 [generator.py](file:///d:/NCKH/generator.py) | Trình sinh dữ liệu ngẫu nhiên: sinh ma trận kiểm tra $H$, sinh vector lỗi bí mật $e$ có trọng số Hamming đúng bằng $w$, và tính hội chứng (syndrome) $s = H \cdot e^T \pmod 2$. |
| 📊 [benchmark.py](file:///d:/NCKH/benchmark.py) | Kịch bản chạy thực nghiệm đo hiệu năng: So sánh Stern với Prange, khảo sát sự ảnh hưởng của tham số cửa sổ $l$, và kiểm chứng độ phức tạp hàm mũ khi tăng độ dài từ mã $n$. |
| 💻 [app.py](file:///d:/NCKH/app.py) | **Ứng dụng Streamlit**. Giao diện trực quan hóa tương tác cho phép cấu hình tham số ($n, k, w, p, l$), sinh dữ liệu hệ mật và theo dõi trực quan kết quả giải mã. |
| 🚀 [main.py](file:///d:/NCKH/main.py) | Chương trình mô phỏng chạy nhanh thuật toán Stern trên Terminal. |
| 📰 [poster.html](file:///d:/NCKH/poster.html) / [style.css](file:///d:/NCKH/style.css) | File thiết kế Poster khoa học khổ dọc A2. Hỗ trợ hiển thị công thức toán học chuyên nghiệp bằng **KaTeX** và cấu trúc chia cột hiện đại. |
| 🖨️ [render_poster.py](file:///d:/NCKH/render_poster.py) | Script sử dụng thư viện **Playwright** để chụp màn hình và chuyển đổi file [poster.html](file:///d:/NCKH/poster.html) thành các định dạng chất lượng cao để in ấn: `poster_a2.pdf` và `poster_a2.png`. |
| 🧪 [test.py](file:///d:/NCKH/test.py) | File thử nghiệm chuyển đổi HTML sang PDF dạng A4. |

---

## 🛠️ Hướng dẫn cài đặt và sử dụng

### 1. Chuẩn bị môi trường

Dự án yêu cầu cài đặt **Python 3.10+**. Khuyến khích sử dụng môi trường ảo (`.venv`).

Cài đặt các thư viện cần thiết:
```bash
pip install numpy streamlit playwright
```

Sau khi cài đặt `playwright`, bạn cần cài đặt thêm nhân trình duyệt chromium phục vụ cho việc render ảnh/pdf:
```bash
playwright install chromium
```

### 2. Chạy ứng dụng giao diện trực quan (Streamlit)

Để trải nghiệm giao diện demo trực quan hóa thuật toán, khởi động máy chủ Streamlit bằng lệnh:
```bash
streamlit run app.py
```
Sau khi chạy, trình duyệt sẽ tự động mở trang web demo tại địa chỉ: `http://localhost:8501`. Tại đây bạn có thể:
* Điều chỉnh độ dài mã $n$, số chiều $k$, trọng số lỗi $w$.
* Thay đổi tham số giải mã $p$ (lỗi mỗi nửa tập thông tin) và $l$ (độ dài cửa sổ va chạm).
* Xem biểu đồ phân bố vector lỗi và thống kê thời gian chạy, số vòng lặp thực tế.

### 3. Chạy thực nghiệm đánh giá hiệu năng (Benchmark)

Chương trình benchmark thực hiện 3 kịch bản:
- **Kịch bản 1:** So sánh thuật toán Stern ($p=1, 2$) và thuật toán Prange cổ điển ($p=0$).
- **Kịch bản 2:** Khảo sát giá trị tối ưu của tham số cửa sổ $l$ (Sweet spot).
- **Kịch bản 3:** Kiểm tra tốc độ bùng nổ thời gian tính toán khi tăng quy mô bài toán $n$.

Chạy benchmark qua dòng lệnh:
```bash
python benchmark.py
```



## 📐 Lý thuyết thuật toán giải mã tập thông tin Stern (1989)

### 1. Bài toán Syndrome Decoding (SDP)
Cho trước ma trận $H \in \mathbb{F}_2^{(n-k) \times n}$, vector hội chứng $s \in \mathbb{F}_2^{n-k}$ và một số nguyên dương $w$. Tìm vector lỗi $e \in \mathbb{F}_2^n$ sao cho:
$$H \cdot e^T = s \pmod 2 \quad \text{và} \quad \text{wt}(e) = w$$

### 2. Ý tưởng chính của Stern
1. **Cô lập tập thông tin:** Dùng một hoán vị ngẫu nhiên $\Pi$ trên các cột của $H$, thực hiện phép khử Gauss trên $\mathbb{F}_2$ để đưa $H$ về dạng chuẩn $[H' \mid I_{n-k}]$.
2. **Chia để trị (Splitting):** Chia tập thông tin kích thước $k$ thành hai phần bằng nhau $X$ và $Y$ (mỗi phần độ dài $k/2$). Giả sử vector lỗi $e$ có đúng $p$ bit $1$ trong phần $X$ và $p$ bit $1$ trong phần $Y$ (tổng cộng $2p$ lỗi trong tập thông tin $k$, phần còn lại có $w - 2p$ lỗi nằm trong tập kiểm tra).
3. **Kỹ thuật Cửa sổ l-bit & Va chạm Bảng băm (Meet-in-the-Middle):** 
   - Thay vì kiểm tra trên toàn bộ hội chứng độ dài $r = n-k$, thuật toán chỉ kiểm tra sự trùng khớp trên một cửa sổ nhỏ $l$ bit để lọc bớt ứng viên.
   - Với mọi lỗi bán phần $e_X \in \mathbb{F}_2^{k/2}$ có trọng số $p$, tính hội chứng $l$-bit và đưa vào bảng băm: $\text{Key} = H'_{l, X} \cdot e_X^T$.
   - Với mọi lỗi bán phần $e_Y \in \mathbb{F}_2^{k/2}$ có trọng số $p$, tính $\text{Target} = s'_{l} \oplus H'_{l, Y} \cdot e_Y^T$. Nếu $\text{Target}$ tồn tại trong bảng băm (xảy ra va chạm), tiến hành kiểm tra điều kiện trọng số toàn cục trên phần còn lại.
4. **Lặp lại:** Nếu không có cặp lỗi nào thỏa mãn điều kiện toàn cục $\text{wt}(e) = w$, thuật toán chọn ngẫu nhiên một hoán vị $\Pi$ khác và thực hiện lại từ đầu (Thuật toán dạng Las Vegas).

---

## 🔬 Kết quả thực nghiệm chính

Khảo sát với cấu hình $n=100, k=50, w=10, l=8$:
- **Prange ($p=0$):** Cần trung bình **10.000+ vòng lặp** (trên thực tế thường bị timeout với thời gian chạy trung bình **>47 giây**).
- **Stern ($p=1$):** Cần trung bình **522 vòng lặp** (thời gian chạy trung bình **1.65 giây**).
- **Stern ($p=2$):** Chỉ cần trung bình **33 vòng lặp** (thời gian chạy trung bình **0.18 giây**).
- **Kết luận:** Thiết lập $p=2$ giúp tăng tốc giải mã lên **hơn 260 lần** so với thuật toán Prange cổ điển, cho thấy hiệu quả vượt trội của kỹ thuật va chạm bảng băm.

---

## 📜 Tài liệu tham khảo

1. Stern, J. (1989). *A method for finding codewords of small weight*. Colloquium on Trees in Algebra and Computer Science (STACS).
2. Berlekamp, E., McEliece, R., & van Tilborg, H. (1978). *On the inherent intractability of certain coding problems*. IEEE Transactions on Information Theory.
3. McEliece, R. J. (1978). *A Public-Key Cryptosystem Based on Algebraic Coding Theory*. DSN Progress Report.
