"""
Setup verification script for AI Visibility Tracker
Run this to check if everything is configured correctly
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set"""
    print("=" * 60)
    print("AI VISIBILITY TRACKER - SETUP VERIFICATION")
    print("=" * 60)
    print()
    
    issues = []
    warnings = []
    
    # Check Python version
    print("✓ Checking Python version...")
    if sys.version_info < (3, 10):
        issues.append("Python 3.10+ required")
    else:
        print(f"  Python {sys.version_info.major}.{sys.version_info.minor} ✓")
    print()
    
    # Check if .env exists
    print("✓ Checking .env file...")
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        issues.append(".env file not found - copy from .env.example")
        print("  ❌ .env file NOT found!")
    else:
        print("  .env file exists ✓")
        
        # Check API keys
        from dotenv import load_dotenv
        load_dotenv()
        
        print("\n✓ Checking API keys...")
        
        openai_key = os.getenv('OPENAI_API_KEY', '')
        if not openai_key or openai_key == 'your_openai_api_key_here':
            issues.append("OPENAI_API_KEY not set or invalid")
            print("  ❌ OPENAI_API_KEY not configured")
        else:
            print(f"  OPENAI_API_KEY configured ✓")
        
        claude_key = os.getenv('CLAUDE_API_KEY', '')
        if not claude_key or claude_key == 'your_claude_api_key_here':
            warnings.append("CLAUDE_API_KEY not set (optional)")
            print("  ⚠️  CLAUDE_API_KEY not configured (optional)")
        else:
            print(f"  CLAUDE_API_KEY configured ✓")
        
        gemini_key = os.getenv('GEMINI_API_KEY', '')
        if not gemini_key or gemini_key == 'your_gemini_api_key_here':
            warnings.append("GEMINI_API_KEY not set (optional)")
            print("  ⚠️  GEMINI_API_KEY not configured (optional)")
        else:
            print(f"  GEMINI_API_KEY configured ✓")
    print()
    
    # Check Django setup
    print("✓ Checking Django installation...")
    try:
        import django
        print(f"  Django {django.get_version()} installed ✓")
    except ImportError:
        issues.append("Django not installed - run: pip install -r requirements.txt")
        print("  ❌ Django not installed")
    print()
    
    # Check LangChain
    print("✓ Checking LangChain installation...")
    try:
        import langchain
        print(f"  LangChain installed ✓")
    except ImportError:
        issues.append("LangChain not installed - run: pip install -r requirements.txt")
        print("  ❌ LangChain not installed")
    print()
    
    # Check database
    print("✓ Checking database...")
    db_file = Path(__file__).parent / 'db.sqlite3'
    if not db_file.exists():
        warnings.append("Database not created - run: python manage.py migrate")
        print("  ⚠️  Database not found (run migrations)")
    else:
        print("  Database exists ✓")
    print()
    
    # Check migrations
    print("✓ Checking migrations...")
    migrations_dir = Path(__file__).parent / 'tracker' / 'migrations'
    if migrations_dir.exists():
        migration_files = list(migrations_dir.glob('*.py'))
        if len(migration_files) > 1:  # More than just __init__.py
            print(f"  Migrations created ✓")
        else:
            warnings.append("Migrations not created - run: python manage.py makemigrations")
            print("  ⚠️  Migrations not created")
    print()
    
    # Check static directory
    print("✓ Checking static directory...")
    static_dir = Path(__file__).parent / 'static'
    if not static_dir.exists():
        warnings.append("Static directory not found")
        print("  ⚠️  Static directory not found")
    else:
        print("  Static directory exists ✓")
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if not issues and not warnings:
        print("✅ All checks passed! You're ready to go!")
        print("\nTo start the server, run:")
        print("  python manage.py runserver")
    else:
        if issues:
            print(f"\n❌ {len(issues)} CRITICAL ISSUE(S) FOUND:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} WARNING(S):")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")
        
        print("\nPlease fix the issues above before running the application.")
        print("\nQuick fix commands:")
        print("  1. Copy .env.example to .env and add API keys")
        print("  2. pip install -r requirements.txt")
        print("  3. python manage.py makemigrations")
        print("  4. python manage.py migrate")
        print("  5. python manage.py init_models")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        check_environment()
    except Exception as e:
        print(f"\n❌ Error during verification: {str(e)}")
        print("\nMake sure you're running this from the project root directory.")
