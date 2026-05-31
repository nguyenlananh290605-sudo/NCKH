from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath('poster.html')
pdf_path = os.path.abspath('poster_a2.pdf')
img_path = os.path.abspath('poster_a2.png')

with sync_playwright() as p:
    # 1. Khởi tạo trình duyệt
    browser = p.chromium.launch()

    # Kích thước pixel cho A2 ở mật độ hiển thị cao (tương đương ~3508x4961 cho 300DPI)
    # Ở đây dùng scale factor để tăng độ sắc nét cho ảnh
    context = browser.new_context(
        viewport={'width': 1587, 'height': 2245},  # Tỷ lệ A2 dọc (mm * 3.78)
        device_scale_factor=2  # Tăng gấp đôi mật độ điểm ảnh để in ấn sắc nét
    )
    page = context.new_page()

    page.goto('file://' + html_path, wait_until='networkidle')
    # Đợi MathJax hoặc các font chữ load xong
    page.wait_for_timeout(2000)

    # --- XUẤT FILE PDF (Khuyên dùng để đi in vì giữ được vector) ---
    page.pdf(
        path=pdf_path,
        format="A2",
        print_background=True,
        margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
    )


    page.screenshot(
        path=img_path,
        full_page=True,
        type='png'
    )

    browser.close()

print(f'Đã lưu PDF: {pdf_path}')
print(f'Đã lưu Ảnh: {img_path}')