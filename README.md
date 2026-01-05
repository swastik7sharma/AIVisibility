# AI VISIBILITY TRACKER

A comprehensive Django application that tracks brand visibility in AI-generated answers across ChatGPT, Claude, and Gemini.

## 📊 System Workflow

![AI Visibility Tracker Workflow](workflow_diagram.png)

The system consists of three sequential modules that work together to analyze your brand's visibility in AI-generated responses.

## 🎯 What This Does

When users ask AI assistants like ChatGPT "What's the best CRM for startups?", which brands get mentioned? This tool:

- **Discovers** which competitors dominate AI recommendations
- **Measures** visibility across multiple AI models
- **Analyzes** sentiment, positioning, and prominence
- **Generates** actionable recommendations to improve visibility

---

## 🏗️ System Architecture

The system is built with **THREE MANDATORY MODULES** that execute sequentially:

### Module 1: User Interface Part
- User authentication & project creation
- Company details input
- AI-powered competitor discovery (using ChatGPT)
- Realistic prompt generation
- User validation & customization

### Module 2: Online Visibility Check Engine
- Queries all selected AI models with all selected prompts
- Extracts brand mentions with position tracking
- Calculates 4 key metrics:
  1. **Frequency**: How many prompts mention the brand
  2. **Prominence**: Position of mentions (1/position scoring)
  3. **Sentiment**: AI-analyzed tone (very positive/positive/neutral/negative)
  4. **Model Coverage**: Weighted by model importance
- Computes aggregate visibility score (0-100%)
- **Error Handling**: Exponential backoff retry for API failures

### Module 3: Analysis and Think Engine
- Competitive analysis & leaderboard
- Prompt-wise performance breakdown
- Model-wise performance analysis
- Negative sentiment detection
- Strategic insights generation
- Actionable recommendations (content, SEO/PR, messaging)

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.12+ (Anaconda environment)
- API Keys for:
  - OpenAI (ChatGPT)
  - Anthropic (Claude)
  - Google (Gemini)

### Installation

1. **Activate Anaconda Environment** (Windows)
```powershell
C:/Users/swast/anaconda3/Scripts/activate
```

2. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

3. **Create .env File**
Copy `.env.example` to `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
```

4. **Run Migrations**
```powershell
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser** (Optional, for admin access)
```powershell
python manage.py createsuperuser
```

6. **Run Server**
```powershell
python manage.py runserver
```

7. **Access Application**
- Main App: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/

---

## 📊 How to Use

### Step 1: Sign Up / Login
Create an account or log in to access the dashboard.

### Step 2: Create New Visibility Check
1. Enter your company details:
   - Company name
   - Description
   - Area of work / category

2. Wait for AI analysis (ChatGPT will):
   - Refine your company summary
   - Discover 5-7 main competitors
   - Generate 8-12 realistic prompts

### Step 3: Validate & Customize
- Edit the AI-generated company summary
- Select/deselect competitors or add custom ones
- Choose which prompts to test or add your own
- Click "Continue to Model Selection"

### Step 4: Select AI Models
- Choose which AI models to query:
  - ✅ ChatGPT (weight: 1.0)
  - ✅ Claude (weight: 0.9)
  - ✅ Gemini (weight: 0.8)

### Step 5: Execute Check
- Review summary (prompts × models = total API calls)
- Start visibility check
- Process runs in background (5-15 minutes)

### Step 6: View Report
Access comprehensive report with:
- 🏆 Visibility leaderboard
- 📊 Competitor comparison
- 🎯 Prompt-wise analysis
- 🤖 Model-wise breakdown
- ⚠️ Negative sentiment alerts
- 💡 Strategic insights
- ✅ Action plan

---

## 🔧 Technical Stack

- **Backend**: Django 6.0
- **Database**: SQLite3
- **AI Orchestration**: LangChain + LangGraph
- **AI Models**:
  - OpenAI GPT-4 (ChatGPT)
  - Anthropic Claude 3.5 Sonnet
  - Google Gemini 2.0 Flash
- **Frontend**: Django Templates + CSS

---

## 📁 Project Structure

```
AIEO/
├── ai_visibility_tracker/     # Django project settings
│   ├── settings.py            # Configuration
│   └── urls.py                # URL routing
├── tracker/                   # Main app
│   ├── models.py              # Database models
│   ├── views.py               # View controllers
│   ├── urls.py                # App URLs
│   ├── ai_config.py           # LangChain config
│   ├── workflows.py           # Module 1 (LangGraph)
│   ├── module2_engine.py      # Module 2 (Scoring)
│   ├── module3_engine.py      # Module 3 (Analysis)
│   ├── admin.py               # Admin interface
│   └── templates/             # HTML templates
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
├── .env                       # API keys (create this)
└── README.md                  # This file
```

---

## 🎨 Key Features

### ✅ Module Separation
Strict execution order: Module 1 → Module 2 → Module 3

### ✅ Error Handling
- Exponential backoff retry (max 3 attempts)
- Graceful degradation for API failures
- Partial data handling
- Detailed execution logging

### ✅ Scoring Algorithm
```
Visibility Score = Frequency × Prominence × Sentiment × Model Coverage

Where:
- Frequency: (Mentions in prompts) / (Total prompts)
- Prominence: Average of (1 / position)
- Sentiment: 1.2 (very positive) to 0.5 (negative)
- Model Coverage: Weighted average by model importance

Normalized to 0-100 scale
```

### ✅ Competitor Impersonation
Run entire analysis from any competitor's perspective with one click.

---

## 🔐 Security Notes

- **Never commit .env file** (contains API keys)
- **Change Django SECRET_KEY** in production
- **Set DEBUG=False** in production
- SQLite is for development only - use PostgreSQL for production

---

## 📝 Database Models

- **VisibilityProject**: Main project tracker
- **Brand**: Main company being tracked
- **Competitor**: Competitor brands
- **AIModel**: Available AI models
- **Prompt**: Test prompts/queries
- **PromptResponse**: Raw AI responses
- **BrandMention**: Extracted mentions
- **SentimentScore**: Sentiment analysis
- **VisibilityScore**: Aggregated scores
- **DetailedReport**: Final analysis
- **ExecutionLog**: Workflow logging

---

## 🐛 Troubleshooting

### API Key Errors
- Ensure `.env` file exists with valid keys
- Check key permissions and quotas

### Import Errors
- Activate Anaconda environment
- Reinstall packages: `pip install -r requirements.txt`

### Slow Execution
- Reduce number of prompts or models
- Check API rate limits
- Monitor ExecutionLog in admin

### Module Not Running
- Check project status in admin
- Review ExecutionLog for errors
- Ensure background threads are running

---

## 🚧 Known Limitations

- **No Docker**: Runs locally only
- **No Deployment**: Development setup
- **SQLite**: Not suitable for production
- **Background Tasks**: Uses threading (not Celery)
- **Rate Limits**: Subject to API provider limits

---

## 📈 Future Enhancements

- Historical tracking (trend analysis)
- Email notifications on completion
- Export reports to PDF
- Scheduled periodic checks
- Celery for background tasks
- PostgreSQL migration
- Docker containerization
- Cloud deployment ready

---

## 📞 Support

For issues or questions:
1. Check ExecutionLog in Django admin
2. Review error messages in terminal
3. Verify API keys in .env
4. Ensure all dependencies installed

---

## ⚖️ License

This is a proprietary MVP. All rights reserved.

---

## 🙏 Credits

Built with:
- Django
- LangChain & LangGraph
- OpenAI, Anthropic, Google AI APIs
