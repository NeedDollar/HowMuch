const { chromium } = require('playwright');

(async () => {
  const url = process.argv[2];

  if (!url) {
    console.error("Please provide a URL as a command-line argument.");
    process.exit(1);
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();

  page.on('pageerror', (err) => {
    console.error('PAGE ERROR:', err);
  });

  page.on('requestfailed', (request) => {
    console.error('REQUEST FAILED:', request.url(), request.failure());
  });

  try {
    const response = await page.goto(url, {
      waitUntil: 'domcontentloaded',
      headers: {
        accept:
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        priority: 'u=0, i',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
      },
    });

    if (response) {
      console.log('Response object:', response); // Log the response object
      if (!response.ok()) {
        console.error(`HTTP error! status: ${response.status()}`);
      }
    }

    const html = await page.content();
    console.log(html);

  } catch (error) {
    console.error("Error:", error); // Log the full error object
  } finally {
    await browser.close();
  }
})();