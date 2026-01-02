import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup
from loguru import logger
from backend.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential

class JobScraper:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.headless = settings.headless_browser
        self.timeout = settings.browser_timeout

    async def __aenter__(self):
        await self.init_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_browser()

    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        logger.info("Browser initialized")

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def scrape_page(self, url: str) -> str:
        page = await self.browser.new_page()
        try:
            await page.goto(url, timeout=self.timeout)
            await page.wait_for_load_state("networkidle")
            return await page.content()
        finally:
            await page.close()

class LinkedInScraper(JobScraper):
    async def search_jobs(self, keywords: str, location: str = "", max_results: int = 50) -> List[Dict]:
        jobs = []
        url = f"https://www.linkedin.com/jobs/search/?keywords={keywords.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
        try:
            content = await self.scrape_page(url)
            soup = BeautifulSoup(content, 'lxml')
            job_cards = soup.find_all('div', class_='base-card')
            for card in job_cards[:max_results]:
                job = self._parse_linkedin_job(card)
                if job:
                    jobs.append(job)
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {e}")
        return jobs

    def _parse_linkedin_job(self, card) -> Optional[Dict]:
        try:
            title_elem = card.find('h3', class_='base-search-card__title')
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            link_elem = card.find('a', class_='base-card__full-link')
            if not all([title_elem, company_elem, link_elem]): return None
            return {
                "job_id": link_elem.get('href', '').split('/')[-1].split('?')[0],
                "title": title_elem.text.strip(),
                "company": company_elem.text.strip(),
                "location": card.find('span', class_='job-search-card__location').text.strip() if card.find('span', class_='job-search-card__location') else "Remote",
                "url": link_elem.get('href', ''),
                "source": "LinkedIn",
                "scraped_at": datetime.utcnow()
            }
        except Exception as e:
            return None

class JobScraperService:
    async def search_all_platforms(self, keywords: str, location: str = "", platforms: List[str] = None, max_results_per_platform: int = 50) -> List[Dict]:
        all_jobs = []
        if not platforms: platforms = ["linkedin"]
        async with LinkedInScraper() as scraper:
            if "linkedin" in platforms:
                jobs = await scraper.search_jobs(keywords, location, max_results_per_platform)
                all_jobs.extend(jobs)
        return all_jobs
