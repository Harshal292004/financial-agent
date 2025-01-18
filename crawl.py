import os
import re
import asyncio
import requests
from xml.etree import ElementTree
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from RichLogger import RichLogger


class CrawlWebpages:
    """
    Crawls web pages and saves clean output to a directory.
    """

    def __init__(
        self,
        output_dir: str = "output",
        output_file_name: str = "cleaned_document.txt",
        sitemap_url: str = "https://ai.pydantic.dev/sitemap.xml",
        max_concurrent: int = 3,
        browser_config: BrowserConfig = None,
        crawl_config: CrawlerRunConfig = None,
    ):
        # Set default paths
        self.__location__ = os.path.dirname(os.path.abspath(__file__))
        self.__output_file__ = os.path.join(self.__location__, output_dir, output_file_name)

        # Ensure the output directory exists
        os.makedirs(os.path.join(self.__location__, output_dir), exist_ok=True)

        # Logger instance
        self.logger = RichLogger()

        # Parameters
        self.sitemap_url = sitemap_url
        self.max_concurrent = max_concurrent

        # Browser configuration
        self.browser_config = browser_config or BrowserConfig(
            headless=True,
            verbose=False,
            extra_args=["--disable-dev-shm-usage", "--no-sandbox"],
        )

        # Crawler run configuration
        self.crawl_config = crawl_config or CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            only_text=True,
            remove_forms=True,
        )

    def clean_and_save_content(self, raw_content: str):
        """
        Cleans the extracted page and saves it to a file.
        """
        # Remove HTML tags
        cleaned_content = re.sub(r"<[^>]+>", "", raw_content)

        # Remove inline scripts or styles
        cleaned_content = re.sub(r"(?:<script.*?>.*?</script>|<style.*?>.*?</style>)", "", cleaned_content, flags=re.DOTALL)

        # Remove unwanted special characters but keep TypeScript-related punctuation
        cleaned_content = re.sub(r"[^\w\s.,:;/@#?&%=()\[\]{}'\"+-]+", " ", cleaned_content)

        # Collapse multiple spaces or newlines into a single space
        cleaned_content = re.sub(r"\s+", " ", cleaned_content).strip()

        # Write cleaned content to a file
        with open(self.__output_file__, "a") as f:
            f.write(cleaned_content)

        self.logger.success(f"Cleaned content saved to {self.__output_file__}")

    async def crawl_parallel(self, urls: List[str]):
        """
        Crawl sites in parallel to save time.
        """
        self.logger.info("\nStart Crawling in parallel")
        # Create the crawler instance
        crawler = AsyncWebCrawler(config=self.browser_config)
        await crawler.start()

        try:
            success_count = 0
            fail_count = 0

            for i in range(0, len(urls), self.max_concurrent):
                batch = urls[i : i + self.max_concurrent]
                tasks = []

                for j, url in enumerate(batch):
                    # Unique session_id per concurrent sub-task
                    session_id = f"parallel_session_{i + j}"
                    task = crawler.arun(url=url, config=self.crawl_config, session_id=session_id)
                    tasks.append(task)

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for url, result in zip(batch, results):
                    if isinstance(result, Exception):
                        self.logger.error(f"Error crawling {url}: {result}")
                        fail_count += 1
                    elif result.success:
                        
                        self.clean_and_save_content(result.markdown_v2.raw_markdown)
                        self.logger.success(f"Successfully crawled {url}")
                        success_count += 1
                    else:
                        self.logger.warn(f"Failed to crawl {url}")
                        fail_count += 1

            self.logger.info("\nSummary:")
            self.logger.info(f"  - Successfully crawled: {success_count}")
            self.logger.info(f"  - Failed: {fail_count}")

        finally:
            self.logger.info("\nClosing crawler...")
            await crawler.close()

    def get_pydantic_ai_docs_urls(self) -> List[str]:
        """
        Fetches all URLs from the Pydantic AI documentation.
        Uses the sitemap to get these URLs.

        Returns:
            List[str]: List of URLs
        """
        try:
            response = requests.get(self.sitemap_url)
            response.raise_for_status()

            # Parse the XML
            root = ElementTree.fromstring(response.content)

            # Extract all URLs from the sitemap
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]

            return urls
        except Exception as e:
            self.logger.error(f"Error fetching sitemap: {e}")
            return []

    async def extract_page(self):
        """
        Run the full process: fetch URLs and crawl them.
        """
        urls = self.get_pydantic_ai_docs_urls()
        if urls:
            self.logger.info(f"Found {len(urls)} URLs to crawl")
            await self.crawl_parallel(urls)
        else:
            self.logger.warn("No URLs found to crawl")


if __name__ == "__main__":
    crawler = CrawlWebpages()
    asyncio.run(crawler.extract_page())
