# 📁 PROJECT FILE STRUCTURE

Complete listing of all files in the AI Visibility Tracker project.

---

## 📂 Root Directory

```
AIEO/
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── .env                           # API keys (YOU MUST CREATE THIS)
├── .env.example                   # Template for .env
├── .gitignore                     # Git ignore rules
├── db.sqlite3                     # SQLite database
├── verify_setup.py                # Setup verification script
├── start_server.bat               # Quick start script (Windows)
│
├── README.md                      # Main documentation
├── QUICKSTART.md                  # 5-minute setup guide
├── GETTING_STARTED.md             # Detailed getting started guide
├── ARCHITECTURE.md                # Technical architecture
├── TESTING_CHECKLIST.md           # Testing procedures
├── PROJECT_COMPLETE.md            # Project completion summary
└── FILE_STRUCTURE.md              # This file
```

---

## 📂 Django Project (ai_visibility_tracker/)

```
ai_visibility_tracker/
├── __init__.py                    # Package marker
├── settings.py                    # Django settings ⭐
├── urls.py                        # Root URL configuration ⭐
├── wsgi.py                        # WSGI configuration
└── asgi.py                        # ASGI configuration
```

**Key Files:**
- `settings.py`: Database, apps, middleware, API keys
- `urls.py`: URL routing (includes tracker.urls)

---

## 📂 Tracker App (tracker/)

```
tracker/
├── __init__.py                    # Package marker
├── models.py                      # Database models (11 models) ⭐
├── views.py                       # View controllers ⭐
├── urls.py                        # App URL configuration ⭐
├── admin.py                       # Django admin configuration ⭐
├── apps.py                        # App configuration
├── tests.py                       # Test cases (empty)
│
├── ai_config.py                   # LangChain/AI model setup ⭐
├── workflows.py                   # Module 1 (LangGraph) ⭐
├── module2_engine.py              # Module 2 (Scoring) ⭐
├── module3_engine.py              # Module 3 (Analysis) ⭐
│
├── management/                    # Custom Django commands
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── init_models.py         # Initialize AI models ⭐
│
├── migrations/                    # Database migrations
│   ├── __init__.py
│   └── 0001_initial.py            # Initial migration ⭐
│
└── templates/tracker/             # HTML templates
    ├── base.html                  # Base template ⭐
    ├── index.html                 # Landing page
    ├── signup.html                # Sign up page
    ├── login.html                 # Login page
    ├── dashboard.html             # Dashboard ⭐
    ├── create_project.html        # Step 1: Create project ⭐
    ├── validate_project.html      # Step 2: Validate ⭐
    ├── select_models.html         # Step 3: Select models ⭐
    ├── execute_check.html         # Step 4: Execute ⭐
    ├── check_status.html          # Step 5: Status ⭐
    └── view_report.html           # Step 6: View report ⭐
```

**Key Files (⭐ = Critical):**

### Core Application Files
- `models.py`: 11 database models (VisibilityProject, Brand, Competitor, etc.)
- `views.py`: 10+ view functions handling all user interactions
- `urls.py`: URL routing for the app
- `admin.py`: Admin panel configuration for all models

### AI & Workflow Files
- `ai_config.py`: LangChain setup, model configuration, retry logic
- `workflows.py`: Module 1 - LangGraph workflow (analyze, discover, generate)
- `module2_engine.py`: Module 2 - Visibility scoring engine
- `module3_engine.py`: Module 3 - Analysis and insights generation

### Templates (User Interface)
- `base.html`: Base template with navigation and styling
- `dashboard.html`: Main dashboard showing all projects
- `create_project.html`: Project creation form
- `validate_project.html`: Competitor/prompt validation
- `view_report.html`: Comprehensive report display

---

## 📂 Static Files (static/)

```
static/
└── (empty - CSS is inline in base.html)
```

**Note**: For production, extract CSS to separate files here.

---

## 📊 DATABASE MODELS (11 Total)

Defined in `tracker/models.py`:

1. **VisibilityProject** - Main project tracker
2. **Brand** - Company being tracked
3. **Competitor** - Competitor brands
4. **AIModel** - AI models (ChatGPT, Claude, Gemini)
5. **Prompt** - Test prompts/queries
6. **ModelSelection** - Selected models per project
7. **PromptResponse** - Raw AI responses
8. **BrandMention** - Extracted mentions
9. **SentimentScore** - Sentiment analysis
10. **VisibilityScore** - Aggregated visibility scores
11. **DetailedReport** - Final analysis report
12. **ExecutionLog** - Workflow execution logs

---

## 🎯 CORE WORKFLOWS (3 Modules)

### Module 1: User Interface Part
**File**: `tracker/workflows.py`
- `analyze_company()` - Analyze company with ChatGPT
- `discover_competitors()` - Find competitors
- `generate_prompts()` - Generate test prompts
- `create_module1_graph()` - LangGraph workflow
- `run_module1()` - Execute Module 1

### Module 2: Visibility Check Engine
**File**: `tracker/module2_engine.py`
- `VisibilityCheckEngine` class
- `query_models()` - Query AI models
- `extract_mentions()` - Extract brand mentions
- `analyze_sentiment()` - Analyze sentiment
- `calculate_scores()` - Calculate visibility scores
- `run_module2()` - Execute Module 2

### Module 3: Analysis & Think Engine
**File**: `tracker/module3_engine.py`
- `AnalysisEngine` class
- `generate_competitor_comparison()` - Leaderboard
- `generate_prompt_wise_analysis()` - Per-prompt analysis
- `generate_model_wise_analysis()` - Per-model analysis
- `analyze_negative_sentiment()` - Negative sentiment detection
- `generate_insights()` - Strategic insights
- `generate_action_plan()` - Recommendations
- `run_module3()` - Execute Module 3

---

## 🔧 UTILITY FILES

### Setup & Verification
- `verify_setup.py` - Check configuration
- `start_server.bat` - Quick start script (Windows)
- `manage.py` - Django management

### Management Commands
- `tracker/management/commands/init_models.py` - Initialize AI models

---

## 📚 DOCUMENTATION FILES (7 Files)

1. **README.md** (Main)
   - Project overview
   - Features
   - Installation
   - Usage
   - Architecture overview

2. **QUICKSTART.md**
   - 5-minute setup
   - Quick commands
   - Common issues

3. **GETTING_STARTED.md**
   - Detailed guide
   - First visibility check
   - Understanding reports
   - Tips and tricks

4. **ARCHITECTURE.md**
   - Technical architecture
   - System design
   - Database schema
   - Workflow details
   - Scaling considerations

5. **TESTING_CHECKLIST.md**
   - Complete testing procedures
   - Module-by-module tests
   - Edge cases
   - Sign-off checklist

6. **PROJECT_COMPLETE.md**
   - Implementation status
   - Deliverables
   - Success criteria
   - Next steps

7. **FILE_STRUCTURE.md** (This file)
   - File listing
   - Directory structure
   - Key files reference

---

## 📏 CODE STATISTICS

- **Total Python Files**: 15+
- **Total Templates**: 10
- **Total Models**: 11
- **Total Views**: 10+
- **Total Management Commands**: 1
- **Total Documentation Files**: 7
- **Lines of Code**: ~3,500+

---

## 🎨 FILE NAMING CONVENTIONS

### Python Files
- `snake_case.py` - Standard Python convention
- `models.py` - Database models
- `views.py` - View controllers
- `urls.py` - URL configuration
- `*_engine.py` - Processing engines (Module 2, 3)
- `workflows.py` - LangGraph workflows (Module 1)

### Templates
- `lowercase.html` - All lowercase
- `base.html` - Base template
- `*_project.html` - Project workflow templates
- `view_report.html` - Report display

### Documentation
- `UPPERCASE.md` - Major documentation
- `README.md` - Main documentation
- `*_CHECKLIST.md` - Checklists

---

## 🔍 WHERE TO FIND SPECIFIC CODE

### Authentication & User Management
- Views: `tracker/views.py` → `signup()`, `login_view()`
- Templates: `tracker/templates/tracker/signup.html`, `login.html`

### Project Creation & Workflow
- Views: `tracker/views.py` → `create_project()`, `validate_project()`, etc.
- Module 1: `tracker/workflows.py`
- Templates: `create_project.html`, `validate_project.html`, etc.

### AI Model Integration
- Configuration: `tracker/ai_config.py`
- Usage: `tracker/workflows.py`, `module2_engine.py`, `module3_engine.py`

### Scoring Algorithm
- Implementation: `tracker/module2_engine.py` → `calculate_scores()`
- Formula: See ARCHITECTURE.md

### Report Generation
- Implementation: `tracker/module3_engine.py`
- Display: `tracker/templates/tracker/view_report.html`

### Admin Panel
- Configuration: `tracker/admin.py`
- Access: http://localhost:8000/admin/

### Database Schema
- Models: `tracker/models.py`
- Migrations: `tracker/migrations/0001_initial.py`

---

## 🚀 QUICK FILE REFERENCE

| What You Want | Where To Look |
|---------------|---------------|
| Add new database model | `tracker/models.py` |
| Add new page/view | `tracker/views.py` + `tracker/urls.py` + template |
| Modify Module 1 workflow | `tracker/workflows.py` |
| Modify scoring algorithm | `tracker/module2_engine.py` |
| Modify insights generation | `tracker/module3_engine.py` |
| Change AI model configuration | `tracker/ai_config.py` |
| Modify admin panel | `tracker/admin.py` |
| Add new Django command | `tracker/management/commands/` |
| Update styling | `tracker/templates/tracker/base.html` |
| Configure settings | `ai_visibility_tracker/settings.py` |
| Add API keys | `.env` |

---

## 💾 DATABASE FILES

- `db.sqlite3` - SQLite database (created after migrations)
- `tracker/migrations/0001_initial.py` - Database schema migration

---

## 🔐 SENSITIVE FILES (Never Commit!)

- `.env` - Contains API keys and secrets
- `db.sqlite3` - Contains user data (in .gitignore)
- `*.pyc` - Python bytecode (in .gitignore)
- `__pycache__/` - Python cache (in .gitignore)

---

## 📦 DEPENDENCIES (requirements.txt)

Main dependencies:
- Django >= 5.0.0
- langchain >= 0.1.0
- langchain-openai >= 0.0.5
- langchain-anthropic >= 0.1.0
- langchain-google-genai >= 0.0.6
- langgraph >= 0.0.20
- python-dotenv >= 1.0.0
- openai >= 1.10.0
- anthropic >= 0.8.0
- google-generativeai >= 0.3.0

---

## 🎯 ENTRY POINTS

| Purpose | Command | File |
|---------|---------|------|
| Start server | `python manage.py runserver` | `manage.py` |
| Verify setup | `python verify_setup.py` | `verify_setup.py` |
| Run migrations | `python manage.py migrate` | `manage.py` |
| Create superuser | `python manage.py createsuperuser` | `manage.py` |
| Init AI models | `python manage.py init_models` | `tracker/management/commands/init_models.py` |

---

## 📌 KEY FILES SUMMARY

**Must Configure:**
- `.env` - Add your API keys

**Core Application:**
- `tracker/models.py` - Database structure
- `tracker/views.py` - Application logic
- `tracker/workflows.py` - Module 1 (AI analysis)
- `tracker/module2_engine.py` - Module 2 (Scoring)
- `tracker/module3_engine.py` - Module 3 (Insights)

**User Interface:**
- `tracker/templates/tracker/*.html` - All pages

**Documentation:**
- `README.md` - Start here
- `QUICKSTART.md` - Quick setup
- `GETTING_STARTED.md` - Detailed guide

---

## ✅ FILES CHECKLIST

Use this to verify all files are present:

- [ ] manage.py
- [ ] requirements.txt
- [ ] .env (create from .env.example)
- [ ] verify_setup.py
- [ ] start_server.bat
- [ ] ai_visibility_tracker/settings.py
- [ ] tracker/models.py
- [ ] tracker/views.py
- [ ] tracker/ai_config.py
- [ ] tracker/workflows.py
- [ ] tracker/module2_engine.py
- [ ] tracker/module3_engine.py
- [ ] tracker/templates/tracker/ (10 HTML files)
- [ ] README.md
- [ ] QUICKSTART.md
- [ ] GETTING_STARTED.md
- [ ] ARCHITECTURE.md
- [ ] TESTING_CHECKLIST.md
- [ ] PROJECT_COMPLETE.md

---

**Last Updated**: January 2026  
**Project**: AI Visibility Tracker MVP  
**Version**: 1.0
