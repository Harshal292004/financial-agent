import os
import sys
import asyncio
import requests
from xml.etree import ElementTree
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# Define paths
__location__ = os.path.dirname(os.path.abspath(__file__))
__output__ = os.path.join(__location__, "output")
parent_dir = os.path.join(__location__, "output")
sys.path.append(parent_dir)


# Function to crawl URLs in parallel
async def crawl_parallel(urls: List[str], max_concurrent: int = 3):
    
    browser_config = BrowserConfig(
        headless=False,
        verbose=False,
        extra_args=["--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    crawler = AsyncWebCrawler(config=browser_config)
    
    # Manually manage crawler context (alternatively use `async with`)
    await crawler.start()
    try:
        success_count = 0
        fail_count = 0
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i:i + max_concurrent]
            tasks = []

            for j, url in enumerate(batch):
                session_id = f"parallel_session_{i + j}"
                task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    print(f"Error crawling {url}: {result}")
                    fail_count += 1
                elif result.success:
                    success_count += 1
                else:
                    fail_count += 1
        print(f"Successfully crawled {success_count} URLs. Failed: {fail_count}.")
    finally:
        await crawler.close()


# Function to fetch URLs from the Pydantic AI sitemap
def get_pydantic_ai_docs_urls(url:str="https://ai.pydantic.dev/sitemap.xml"):
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)
        namespace = {'ns': 'https://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        return urls

    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


# Main async entry point
async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        await crawl_parallel(urls, max_concurrent=3)
    else:
        print("No URLs found to crawl.")


# Script entry point
if __name__ == "__main__":
    asyncio.run(main())
