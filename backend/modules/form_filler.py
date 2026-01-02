from typing import Dict, List, Optional
from playwright.async_api import Page, Browser
from loguru import logger
import asyncio

class FormFiller:
    def __init__(self, browser: Browser):
        self.browser = browser

    async def fill_application_form(self, url: str, user_data: Dict, resume_path: Optional[str] = None) -> bool:
        page = await self.browser.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state("networkidle")
            fields = await self._detect_form_fields(page)
            for field in fields:
                await self._fill_field(page, field, user_data)
            if resume_path:
                await self._upload_resume(page, resume_path)
            return True
        except Exception as e:
            logger.error(f"Error filling form: {e}")
            return False
        finally:
            await page.close()

    async def _detect_form_fields(self, page: Page) -> List[Dict]:
        fields = []
        patterns = {
            "name": ["name", "full-name", "fullname"],
            "email": ["email", "e-mail"],
            "phone": ["phone", "mobile"]
        }
        for field_type, p_list in patterns.items():
            for p in p_list:
                selector = f"input[name*='{p}'], input[id*='{p}']"
                try:
                    el = await page.query_selector(selector)
                    if el:
                        fields.append({"type": field_type, "selector": selector})
                        break
                except: continue
        return fields

    async def _fill_field(self, page: Page, field: Dict, user_data: Dict):
        val = user_data.get(field['type'], "")
        if val:
            try: await page.fill(field['selector'], str(val))
            except: pass

    async def _upload_resume(self, page: Page, resume_path: str):
        selectors = ["input[type='file']", "input[name*='resume']", "input[id*='resume']"]
        for s in selectors:
            try:
                el = await page.query_selector(s)
                if el:
                    await el.set_input_files(resume_path)
                    return
            except: continue

class ApplicationAutomator:
    def __init__(self, browser: Browser):
        self.filler = FormFiller(browser)

    async def automate_application(self, job_url: str, user_profile: Dict) -> bool:
        return await self.filler.fill_application_form(job_url, user_profile, user_profile.get('resume_path'))
