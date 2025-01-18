import os
import sys
import asyncio
import requests
from xml.etree import ElementTree
from rich.logging import RichHandler
import logging 

log_file="crawler_output.log"
logging.basicConfig(
    level= logging.INFO,
    format= "%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True,show_path=False),
        logging.FileHandler(log_file, mode="w")
    ]
)
logger= logging.getLogger("crawler")

__location__ = os.path.dirname(os.path.abspath(__file__))
print(f"Location:{__location__}")
__output__ = os.path.join(__location__, "output")
print(f"Output:{__output__}")

# Append parent directory to system path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Parent directory:{parent_dir}")
sys.path.append(parent_dir)

from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def crawl_parallel(urls: List[str], max_concurrent: int = 3):
    logger.info("\n=== Parallel Crawling ===")

    # Minimal browser config
    browser_config = BrowserConfig(
        headless=True,
        verbose=False, 
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        only_text=True,
        remove_forms=True,
    )

    # Create the crawler instance
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        success_count = 0
        fail_count = 0
        results=None
        for i in range(0, len(urls), max_concurrent):
            batch = urls[i : i + max_concurrent]
            tasks = []

            for j, url in enumerate(batch):
                # Unique session_id per concurrent sub-task
                session_id = f"parallel_session_{i + j}"
                task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
                tasks.append(task)


            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    logger.error(f"Error crawling {url}: {result}")
                    fail_count += 1
                elif result.success:
                    logger.info(f"Successfully crawled {url}")
                    success_count += 1
                else:
                    logger.warning(f"Failed to crawl {url}")
                    fail_count += 1

        logger.info(f"\nSummary:")
        logger.info(f"  - Successfully crawled: {success_count}")
        logger.info(f"  - Failed: {fail_count}")
        logger.info(f"First result: {results[0].markdown_v2.raw_markdown}")


    finally:
        logger.info("\nClosing crawler...")
        await crawler.close()

def get_pydantic_ai_docs_urls():
    """
    Fetches all URLs from the Pydantic AI documentation.
    Uses the sitemap (https://ai.pydantic.dev/sitemap.xml) to get these URLs.
    
    Returns:
        List[str]: List of URLs
    """            
    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    except Exception as e:
        logger.error(f"Error fetching sitemap: {e}")

        return []        

async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        logger.info(f"Found {len(urls)} URLs to crawl")
        await crawl_parallel(urls, max_concurrent=10)
    else:
        logger.warning("No URLs found to crawl")  

if __name__ == "__main__":
    asyncio.run(main())