#!/usr/bin/env python3
"""Search using Playwright - Yahoo Japan."""

import asyncio
import sys
from playwright.async_api import async_playwright

async def search_yahoo_japan(query: str, max_results: int = 10) -> list[dict]:
    """Search Yahoo Japan and return results."""
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(f'https://search.yahoo.co.jp/search?p={query}', timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            
            # Extract search results
            links = await page.evaluate('''() => {
                const results = [];
                document.querySelectorAll('a').forEach(a => {
                    const text = a.innerText.trim();
                    const href = a.href;
                    if (text && href && href.includes('http') && !href.includes('yahoo')) {
                        results.push({title: text.substring(0, 100), link: href});
                    }
                });
                return results.slice(0, ''' + str(max_results) + ''');
            }''')
            
            results = links
        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)
        finally:
            await browser.close()
    return results

if __name__ == '__main__':
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'test'
    results = asyncio.run(search_yahoo_japan(query))
    for r in results:
        print(f"Title: {r['title']}")
        print(f"Link: {r['link']}")
        print('---')
