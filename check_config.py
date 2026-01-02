import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def check_dependencies():
    print("=" * 60)
    print("CHECKING DEPENDENCIES")
    print("=" * 60)
    dependencies = {
        'google-generativeai': 'Google Generative AI (Gemini)',
        'anthropic': 'Anthropic (Claude)',
        'openai': 'OpenAI',
        'asyncpg': 'AsyncPG (PostgreSQL driver)',
        'sqlalchemy': 'SQLAlchemy',
        'fastapi': 'FastAPI'
    }
    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name}: Installed")
        except ImportError:
            print(f"❌ {name}: NOT INSTALLED")
            missing.append(module)
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False
    print("\n✅ All dependencies installed!")
    return True
def check_config():
    print("\n" + "=" * 60)
    print("CHECKING CONFIGURATION")
    print("=" * 60)
    try:
        from backend.config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"\n📋 Current Settings:")
        print(f"  - LLM Provider: {settings.llm_provider}")
        print(f"  - Database URL: {settings.database_url[:50]}...")
        print(f"  - App Environment: {settings.app_env}")
        print(f"  - Debug Mode: {settings.debug}")
        print(f"\n🔑 API Keys:")
        if settings.gemini_api_key:
            print(f"  - Gemini API Key: {settings.gemini_api_key[:20]}... ✅")
        else:
            print(f"  - Gemini API Key: NOT SET ❌")
        if settings.anthropic_api_key:
            print(f"  - Anthropic API Key: {settings.anthropic_api_key[:20]}... ✅")
        else:
            print(f"  - Anthropic API Key: NOT SET")
        if settings.openai_api_key:
            print(f"  - OpenAI API Key: {settings.openai_api_key[:20]}... ✅")
        else:
            print(f"  - OpenAI API Key: NOT SET")
        print(f"\n🗄️  Database:")
        if 'postgresql' in settings.database_url:
            print(f"  - Type: PostgreSQL (Neon) ✅")
            print(f"  - Connection: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'N/A'}")
        elif 'sqlite' in settings.database_url:
            print(f"  - Type: SQLite (Local) ✅")
        else:
            print(f"  - Type: Unknown ⚠️")
        return True
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False
def check_llm_engine():
    print("\n" + "=" * 60)
    print("CHECKING LLM ENGINE")
    print("=" * 60)
    try:
        from backend.modules.llm_engine import LLMEngine
        engine = LLMEngine()
        print(f"✅ LLM Engine initialized successfully!")
        print(f"  - Provider: {engine.provider}")
        print(f"  - Model: {engine.model}")
        return True
    except Exception as e:
        print(f"❌ Error initializing LLM Engine: {e}")
        print(f"\nMake sure you have:")
        print(f"  1. Installed required dependencies")
        print(f"  2. Set the API key in .env file")
        print(f"  3. Set LLM_PROVIDER in .env file")
        return False
def check_database():
    print("\n" + "=" * 60)
    print("CHECKING DATABASE")
    print("=" * 60)
    try:
        import asyncio
        from backend.models.database import init_db, engine
        async def test_db():
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(lambda _: None)
                print(f"✅ Database connection successful!")
                await init_db()
                print(f"✅ Database tables initialized!")
                return True
            except Exception as e:
                print(f"❌ Database error: {e}")
                return False
        result = asyncio.run(test_db())
        return result
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
def main():
    print("\n" + "=" * 60)
    print("JOB APPLICATION ASSISTANT - CONFIGURATION CHECK")
    print("=" * 60 + "\n")
    results = []
    results.append(("Dependencies", check_dependencies()))
    results.append(("Configuration", check_config()))
    results.append(("LLM Engine", check_llm_engine()))
    results.append(("Database", check_database()))
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, status in results:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}: {'PASS' if status else 'FAIL'}")
    all_passed = all(status for _, status in results)
    if all_passed:
        print("\n🎉 All checks passed! Your setup is ready to use.")
        print("\nNext steps:")
        print("  1. Run: start_backend.bat (or ./start_backend.sh)")
        print("  2. Run: start_frontend.bat (or ./start_frontend.sh)")
        print("  3. Open: http://localhost:8501")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Set API keys in .env file")
        print("  3. Check database connection string")
    return 0 if all_passed else 1
if __name__ == "__main__":
    sys.exit(main())
