import asyncio
from playwright.async_api import async_playwright
import sys
import tempfile
import os

#pip install playwright && playwright install

async def get_page_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url)
            html = await page.content()
            return html
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        html_content = asyncio.run(get_page_html(url))

        if html_content:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(html_content)
                temp_filename = temp_file.name

            try:
                with open(temp_filename, 'r', encoding='utf-8') as f:
                    print(f.read())
            finally:
                os.unlink(temp_filename)

        else:
            sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
