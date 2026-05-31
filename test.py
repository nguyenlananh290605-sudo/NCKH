from playwright.sync_api import sync_playwright

def html_to_pdf(html_file, output_pdf):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Mở file HTML (dùng đường dẫn tuyệt đối)
        import os
        path = "file://" + os.path.abspath(html_file)

        page.goto(path)
        page.pdf(path=output_pdf, format="A4")
        browser.close()

html_to_pdf("poster.html", "output_playwright.pdf")