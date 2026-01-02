from typing import List, Dict
import re
from datetime import datetime

def clean_text(text: str) -> str:
    if not text: return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\-.,!?]', '', text)
    return text.strip()

def extract_email(text: str) -> str:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else ""

def calculate_match_score(user_skills: List[str], required_skills: List[str], preferred_skills: List[str] = None) -> float:
    if not required_skills: return 0.0
    user_skills_lower = [s.lower() for s in user_skills]
    required_skills_lower = [s.lower() for s in required_skills]
    required_matches = sum(1 for skill in required_skills_lower if skill in user_skills_lower)
    required_score = (required_matches / len(required_skills_lower)) * 70
    preferred_score = 0
    if preferred_skills:
        preferred_skills_lower = [s.lower() for s in preferred_skills]
        preferred_matches = sum(1 for skill in preferred_skills_lower if skill in user_skills_lower)
        preferred_score = (preferred_matches / len(preferred_skills_lower)) * 30
    return min(required_score + preferred_score, 100.0)

def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date: return ""
    return date.strftime(format_str)

def parse_salary(salary_text: str) -> Dict[str, float]:
    cleaned = re.sub(r'[$,]', '', salary_text)
    numbers = re.findall(r'\d+(?:\.\d+)?', cleaned)
    if len(numbers) >= 2:
        return {"min": float(numbers[0]), "max": float(numbers[1])}
    elif len(numbers) == 1:
        return {"min": float(numbers[0]), "max": float(numbers[0])}
    return {"min": 0.0, "max": 0.0}

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    if not text or len(text) <= max_length: return text
    return text[:max_length - len(suffix)] + suffix
