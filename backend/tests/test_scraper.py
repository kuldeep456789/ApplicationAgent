import pytest
from backend.modules.scraper import LinkedInScraper, IndeedScraper, JobScraperService
@pytest.mark.asyncio
async def test_linkedin_scraper_init():
    async with LinkedInScraper() as scraper:
        assert scraper.browser is not None
@pytest.mark.asyncio
async def test_indeed_scraper_init():
    async with IndeedScraper() as scraper:
        assert scraper.browser is not None
@pytest.mark.asyncio
async def test_job_scraper_service():
    service = JobScraperService()
    assert 'linkedin' in service.scrapers
    assert 'indeed' in service.scrapers
@pytest.mark.asyncio
async def test_search_all_platforms():
    service = JobScraperService()
    assert callable(service.search_all_platforms)
