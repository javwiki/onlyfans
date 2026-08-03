#!/usr/bin/env python3
"""Google search using Playwright to bypass bot detection."""

import asyncio
import sys
from playwright.async_api import async_playwright

async def google_search(query: str, max_results: int = 10) -> list[dict]:
    """Search Google and return results."""
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(f'https://www.google.com/search?q={query}', timeout=30000)
            await page.wait_for_selector('div.g', timeout=10000)
            
            elements = await page.query_selector_all('div.g')
            for i, el in enumerate(elements[:max_results]):
                title_el = await el.query_selector('h3')
                link_el = await el.query_selector('a')
                snippet_el = await el.query_selector('div[data-sncf]')
                
                title = await title_el.inner_text() if title_el else ''
                link = await link_el.get_attribute('href') if link_el else ''
                snippet = await snippet_el.inner_text() if snippet_el else ''
                
                if title and link:
                    results.append({'title': title, 'link': link, 'snippet': snippet})
        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)
        finally:
            await browser.close()
    return results

if __name__ == '__main__':
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'test'
    results = asyncio.run(google_search(query))
    for r in results:
        print(f"Title: {r['title']}")
        print(f"Link: {r['link']}")
        print(f"Snippet: {r['snippet']}")
        print('---')
