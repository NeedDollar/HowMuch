import re
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import sys

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto("https://www.tesco.com/groceries/en-GB/products/263204408")
        page.wait_for_function("document.body.textContent.includes('Lowicz')", timeout=10000)

        html_content = page.content()

        # Write HTML content to file with UTF-8 encoding
        with open("tesco_product.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("HTML content saved to tesco_product.html") #confirmation that the script ran correctly.

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Page or context closed unexpectedly.", file=sys.stderr)
        sys.exit(1) #exit with error code.
    finally:
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run(playwright)