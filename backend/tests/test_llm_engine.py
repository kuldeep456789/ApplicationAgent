import pytest
from backend.modules.llm_engine import LLMEngine, JobMatcher
def test_llm_engine_init_anthropic():
    engine = LLMEngine(provider="anthropic")
    assert engine.provider == "anthropic"
    assert engine.model == "claude-3-5-sonnet-20241022"
def test_llm_engine_init_openai():
    engine = LLMEngine(provider="openai")
    assert engine.provider == "openai"
    assert engine.model == "gpt-4-turbo-preview"
def test_llm_engine_invalid_provider():
    with pytest.raises(ValueError):
        LLMEngine(provider="invalid")
def test_job_matcher_init():
    matcher = JobMatcher()
    assert matcher.llm is not None
@pytest.mark.asyncio
async def test_build_analysis_prompt():
    engine = LLMEngine()
    job = {
        : 'Software Engineer',
        : 'Tech Corp',
        : 'Build amazing software',
        : 'Python, FastAPI'
    }
    user_profile = {
        : ['Python', 'FastAPI', 'React'],
        : 5,
        : {'degree': 'BS Computer Science'}
    }
    prompt = engine._build_analysis_prompt(job, user_profile)
    assert 'Software Engineer' in prompt
    assert 'Python' in prompt
