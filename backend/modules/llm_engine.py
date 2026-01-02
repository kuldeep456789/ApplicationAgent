from typing import List, Dict, Optional
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
import google.generativeai as genai
from loguru import logger
from backend.config import settings
import json
import asyncio

class LLMEngine:
    def __init__(self, provider: str = None):
        self.provider = provider or settings.llm_provider
        
        if self.provider == "anthropic":
            self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
            self.model = "claude-3-5-sonnet-20241022"
        elif self.provider == "openai":
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            self.model = "gpt-4-turbo-preview"
        elif self.provider == "gemini":
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.client = None
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def analyze_job(self, job: Dict, user_profile: Dict) -> Dict:
        prompt = self._build_analysis_prompt(job, user_profile)
        try:
            if self.provider == "anthropic":
                response = await self._call_claude(prompt)
            elif self.provider == "openai":
                response = await self._call_openai(prompt)
            elif self.provider == "gemini":
                response = await self._call_gemini(prompt)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            return self._parse_analysis(response)
        except Exception as e:
            logger.error(f"Error analyzing job: {e}")
            return {
                "match_score": 0.0,
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "error": str(e)
            }

    async def generate_cover_letter(self, job: Dict, user_profile: Dict, tone: str = "professional") -> str:
        prompt = self._build_cover_letter_prompt(job, user_profile, tone)
        try:
            if self.provider == "anthropic":
                return await self._call_claude(prompt)
            elif self.provider == "openai":
                return await self._call_openai(prompt)
            elif self.provider == "gemini":
                return await self._call_gemini(prompt)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            return ""

    async def extract_job_requirements(self, job_description: str) -> Dict:
        prompt = f"Analyze the following job description and extract structured information:\n\nJob Description:\n{job_description}\n\nExtract and return a JSON object with: required_skills, preferred_skills, experience_years, education, responsibilities, qualifications. Return only valid JSON."
        try:
            if self.provider == "anthropic":
                response = await self._call_claude(prompt)
            elif self.provider == "openai":
                response = await self._call_openai(prompt)
            elif self.provider == "gemini":
                response = await self._call_gemini(prompt)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error extracting requirements: {e}")
            return {}

    def _build_analysis_prompt(self, job: Dict, user_profile: Dict) -> str:
        return f"Analyze how well this candidate matches the job posting.\n\nJob Title: {job.get('title')}\nCompany: {job.get('company')}\nDescription: {job.get('description')}\n\nCandidate Profile: {user_profile}\n\nReturn a JSON object with match_score (0-100), strengths, weaknesses, and recommendations."

    def _build_cover_letter_prompt(self, job: Dict, user_profile: Dict, tone: str) -> str:
        return f"Generate a {tone} cover letter for the following job and candidate profile.\n\nJob: {job}\nCandidate: {user_profile}"

    async def _call_claude(self, prompt: str) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def _call_openai(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def _call_gemini(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: self.model.generate_content(prompt))
        return response.text

    def _parse_analysis(self, response: str) -> Dict:
        try:
            # Simple extractor for markdown-wrapped JSON
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error parsing analysis response: {e}")
            return {"match_score": 0.0, "error": "Parsing failed"}

class JobMatcher:
    def __init__(self):
        self.llm = LLMEngine()

    async def score_jobs(self, jobs: List[Dict], user_profile: Dict) -> List[Dict]:
        scored_jobs = []
        for job in jobs:
            analysis = await self.llm.analyze_job(job, user_profile)
            job['match_score'] = analysis.get('match_score', 0.0)
            scored_jobs.append(job)
        return scored_jobs
