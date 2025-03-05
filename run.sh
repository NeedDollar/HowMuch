#!/bin/bash

# Install Playwright (if not already installed)
# npx playwright install

url="$1"

if [ -z "$url" ]; then
  echo "Usage: $0 <url>"
  exit 1
fi

tempfile=$(mktemp)

cat <<EOF > get_html.js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  try {
    await page.goto('$url');
    const html = await page.content();
    console.log(html);
  } catch (error) {
    console.error(error);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
EOF

node get_html.js > "$tempfile"

if [ $? -eq 0 ]; then
  cat "$tempfile"
  rm "$tempfile"
else
  rm "$tempfile"
  exit 1
fi

rm get_html.js