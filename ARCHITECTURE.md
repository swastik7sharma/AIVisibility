# AI VISIBILITY TRACKER - TECHNICAL ARCHITECTURE

## 🏗️ SYSTEM OVERVIEW

This document provides a comprehensive technical overview of the AI Visibility Tracker MVP architecture.

---

## 📊 ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  (Django Templates + Forms + JavaScript for status polling)     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                     DJANGO VIEWS LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   Auth     │  │ Dashboard  │  │  Project   │               │
│  │  Views     │  │   Views    │  │   Views    │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                   THREE-MODULE PIPELINE                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MODULE 1: USER INTERFACE PART (LangGraph Workflow)      │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐ │  │
│  │  │  Analyze   │→ │   Discover   │→ │    Generate     │ │  │
│  │  │  Company   │  │ Competitors  │  │    Prompts      │ │  │
│  │  └────────────┘  └──────────────┘  └─────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MODULE 2: VISIBILITY CHECK ENGINE                        │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐ │  │
│  │  │   Query    │→ │   Extract    │→ │    Analyze      │ │  │
│  │  │   Models   │  │   Mentions   │  │   Sentiment     │ │  │
│  │  └────────────┘  └──────────────┘  └─────────────────┘ │  │
│  │                          ↓                               │  │
│  │                  ┌──────────────┐                        │  │
│  │                  │  Calculate   │                        │  │
│  │                  │    Scores    │                        │  │
│  │                  └──────────────┘                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MODULE 3: ANALYSIS & THINK ENGINE                        │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐ │  │
│  │  │ Competitor │→ │   Generate   │→ │    Create       │ │  │
│  │  │  Analysis  │  │   Insights   │  │  Action Plan    │ │  │
│  │  └────────────┘  └──────────────┘  └─────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                   DATA PERSISTENCE LAYER                         │
│                      (SQLite Database)                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Projects │ │ Prompts  │ │ Responses│ │  Scores  │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                    EXTERNAL AI SERVICES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   OpenAI     │  │  Anthropic   │  │   Google     │         │
│  │   (GPT-4)    │  │   (Claude)   │  │  (Gemini)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔧 TECHNOLOGY STACK

### Backend Framework
- **Django 6.0**: Web framework
- **Python 3.12**: Programming language

### Database
- **SQLite3**: Relational database (development)

### AI Orchestration
- **LangChain 1.2.0**: LLM framework
- **LangGraph 1.0.5**: Workflow orchestration

### AI Model Integrations
- **langchain-openai**: OpenAI GPT-4 integration
- **langchain-anthropic**: Claude 3.5 Sonnet integration
- **langchain-google-genai**: Gemini 2.0 Flash integration

### Frontend
- **Django Templates**: Server-side rendering
- **CSS3**: Styling
- **Vanilla JavaScript**: Status polling

---

## 📦 DATABASE SCHEMA

### Core Models

```python
VisibilityProject
├── user (FK → User)
├── company_name
├── company_description
├── area_of_work
├── refined_summary
├── status (setup/validating/checking/analyzing/completed/failed)
└── created_at

Brand
├── project (1-to-1 → VisibilityProject)
└── name

Competitor
├── project (FK → VisibilityProject)
├── name
├── is_ai_suggested
└── is_validated

AIModel
├── name (chatgpt/claude/gemini)
├── display_name
├── weight (1.0/0.9/0.8)
└── is_active

Prompt
├── project (FK → VisibilityProject)
├── text
├── is_ai_generated
└── is_selected

PromptResponse
├── project (FK → VisibilityProject)
├── prompt (FK → Prompt)
├── model (FK → AIModel)
├── raw_response
├── status (pending/success/failed/partial)
├── error_message
└── retry_count

BrandMention
├── response (FK → PromptResponse)
├── brand_name
├── position (1st, 2nd, 3rd...)
├── context
├── is_main_brand
└── competitor (FK → Competitor, nullable)

SentimentScore
├── mention (1-to-1 → BrandMention)
├── sentiment (very_positive/positive/neutral/negative)
├── reasoning
└── confidence

VisibilityScore
├── project (FK → VisibilityProject)
├── brand_name
├── frequency_score
├── prominence_score
├── sentiment_score
├── model_coverage_score
├── raw_score
├── normalized_score (0-100)
├── total_mentions
└── prompts_appeared_in

DetailedReport
├── project (1-to-1 → VisibilityProject)
├── competitor_comparison (JSON)
├── prompt_wise_analysis (JSON)
├── model_wise_analysis (JSON)
├── negative_sentiment_analysis (JSON)
├── why_competitors_win
├── content_gaps
├── messaging_gaps
├── positioning_weaknesses
├── content_ideas (JSON)
├── seo_pr_recommendations (JSON)
└── messaging_improvements (JSON)

ExecutionLog
├── project (FK → VisibilityProject)
├── level (info/warning/error)
├── module (module1/module2/module3)
├── message
└── timestamp
```

---

## 🔄 WORKFLOW EXECUTION

### Module 1: User Interface Part (LangGraph)

**File**: `tracker/workflows.py`

**Purpose**: Collect inputs, analyze company, discover competitors, generate prompts

**Workflow**:
1. **analyze_company(state)**
   - Input: Company name, description, area of work
   - Process: Send to ChatGPT for refinement
   - Output: Refined summary
   - Updates: VisibilityProject.refined_summary

2. **discover_competitors(state)**
   - Input: Refined company summary
   - Process: ChatGPT identifies 5-7 main competitors
   - Output: List of competitors
   - Creates: Competitor records

3. **generate_prompts(state)**
   - Input: Company + competitors
   - Process: ChatGPT generates 8-12 realistic prompts
   - Output: List of prompts
   - Creates: Prompt records

**State Management**: TypedDict with project data passed through nodes

**Error Handling**: 
- Try/except on each node
- Continues on failure with fallbacks
- Logs all activities to ExecutionLog

---

### Module 2: Visibility Check Engine

**File**: `tracker/module2_engine.py`

**Purpose**: Query AI models, extract mentions, analyze sentiment, calculate scores

**Execution Flow**:

1. **query_models()**
   - For each selected prompt:
     - For each selected model:
       - Query model with prompt
       - Store response in PromptResponse
       - Handle API errors with retry logic
   - Creates: PromptResponse records

2. **extract_mentions()**
   - For each successful response:
     - Parse text for brand names (regex matching)
     - Track position of each mention (1st, 2nd, 3rd...)
     - Extract context (50 chars before/after)
     - Identify if main brand or competitor
   - Creates: BrandMention records

3. **analyze_sentiment()**
   - For each brand mention:
     - Send to ChatGPT with context
     - Get sentiment classification
     - Get reasoning
   - Creates: SentimentScore records

4. **calculate_scores()**
   - For each brand (main + competitors):
     - Calculate frequency score (mentions / total prompts)
     - Calculate prominence score (avg of 1/position)
     - Calculate sentiment score (weighted avg)
     - Calculate model coverage score (weighted avg)
     - Aggregate: raw_score = F × P × S × M
     - Normalize to 0-100 scale
   - Creates: VisibilityScore records

**Error Handling**:
- **Retry Logic**: Exponential backoff (2^attempt seconds)
- **Max Retries**: 3 attempts
- **Partial Data**: Mark as 'partial' status if some fail
- **Continue**: Don't crash pipeline on failures

---

### Module 3: Analysis & Think Engine

**File**: `tracker/module3_engine.py`

**Purpose**: Generate insights, comparisons, and actionable recommendations

**Execution Flow**:

1. **generate_competitor_comparison()**
   - Query VisibilityScore records
   - Create leaderboard (sorted by score)
   - Calculate gaps between main brand and top competitor
   - Output: JSON structure

2. **generate_prompt_wise_analysis()**
   - For each prompt:
     - Identify which brand won (lowest avg position)
     - Check if main brand appeared
     - List all brands mentioned
   - Output: JSON structure

3. **generate_model_wise_analysis()**
   - For each model:
     - Identify top brand
     - Get main brand's performance
   - Output: JSON structure

4. **analyze_negative_sentiment()**
   - Find all negative sentiment instances
   - Extract brand, prompt, model, context, reasoning
   - Output: JSON structure

5. **extract_research_sources()**
   - Regex search for URLs in responses
   - Return unique sources
   - Output: List

6. **generate_insights()**
   - Send all data to ChatGPT
   - Request strategic analysis:
     - Why competitors win
     - Content gaps
     - Messaging gaps
     - Positioning weaknesses
   - Output: Text insights

7. **generate_action_plan()**
   - Send insights to ChatGPT
   - Request actionable recommendations:
     - Content ideas (5-7)
     - SEO/PR actions (5-7)
     - Messaging improvements (5-7)
   - Output: JSON lists

**Creates**: DetailedReport record with all sections

---

## 🛡️ ERROR HANDLING STRATEGY

### Retry Logic (Module 2)

```python
def invoke_with_retry(model, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.invoke(prompt)
            return True, response.content, None
        except Exception as e:
            if is_retryable(e):
                delay = 2 ** attempt  # Exponential backoff
                time.sleep(delay)
                continue
            return False, "", str(e)
    return False, "", "All retries exhausted"
```

### Error Types Handled
1. **Rate Limit Exceeded**: Retry with backoff
2. **Quota Exceeded**: Retry, then mark partial
3. **Timeout**: Retry
4. **Invalid API Key**: Fail immediately
5. **Network Error**: Retry
6. **Malformed Response**: Continue with null data

### Graceful Degradation
- If 1 model fails → Continue with other models
- If 1 prompt fails → Continue with other prompts
- If sentiment analysis fails → Default to neutral
- If insights generation fails → Use fallback text

---

## 🧮 SCORING ALGORITHM

### Formula

```
Raw Score = Frequency × Prominence × Sentiment × Model Coverage

Where:
  Frequency = (Prompts where brand mentioned) / (Total prompts)
  Prominence = Average(1 / position) for all mentions
  Sentiment = Average(sentiment_weight) for all mentions
  Model Coverage = Average(model_weight) for all mentions

Sentiment Weights:
  very_positive = 1.2
  positive = 1.0
  neutral = 0.8
  negative = 0.5

Model Weights:
  ChatGPT = 1.0
  Claude = 0.9
  Gemini = 0.8

Normalized Score = min(Raw Score × 100, 100)
```

### Example Calculation

**Brand**: HubSpot  
**Scenario**: 10 prompts, 3 models (30 total queries)

- Mentioned in 7 prompts → Frequency = 0.7
- Positions: [1, 1, 2, 1, 3, 2, 1] → Avg prominence = 0.88
- Sentiments: [positive, positive, very_positive, positive, neutral, positive, positive]
  → Avg sentiment = 1.06
- Models: [ChatGPT×4, Claude×2, Gemini×1]
  → Avg coverage = (1.0×4 + 0.9×2 + 0.8×1) / 7 = 0.96

**Raw Score** = 0.7 × 0.88 × 1.06 × 0.96 = **0.627**

**Normalized Score** = 0.627 × 100 = **62.7%**

---

## 🔐 SECURITY CONSIDERATIONS

### Current Implementation
- Django CSRF protection enabled
- User authentication required for all project views
- API keys stored in environment variables
- SQLite database (local storage only)

### Production Requirements
- Use PostgreSQL instead of SQLite
- Enable HTTPS/SSL
- Set DEBUG=False
- Use strong SECRET_KEY
- Implement rate limiting
- Add API key rotation
- Use proper secrets management
- Enable Django security middleware
- Add input sanitization
- Implement CORS if needed

---

## 📈 SCALABILITY CONSIDERATIONS

### Current Limitations (MVP)
- Threading for background tasks (not Celery)
- SQLite (not suitable for concurrent writes)
- No caching
- No load balancing
- Single server

### Production Scaling Path
1. **Background Tasks**: Replace threading with Celery + Redis
2. **Database**: Migrate to PostgreSQL with connection pooling
3. **Caching**: Add Redis for caching AI responses
4. **Queue**: Use message queue for task distribution
5. **Workers**: Multiple Celery workers for parallel processing
6. **Load Balancer**: Nginx/HAProxy for traffic distribution
7. **CDN**: Static assets on CDN
8. **Monitoring**: Add logging, metrics, alerts

---

## 🚀 DEPLOYMENT ARCHITECTURE (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                    LOAD BALANCER (Nginx)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐      ┌───▼───┐
│Django │        │Django │      │Django │
│Server1│        │Server2│      │Server3│
└───┬───┘        └───┬───┘      └───┬───┘
    │                │                │
    └────────────────┼────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼─────┐    ┌────▼────┐    ┌─────▼────┐
│PostgreSQL│    │  Redis  │    │  Celery  │
│Database  │    │  Cache  │    │  Workers │
└──────────┘    └─────────┘    └──────────┘
                                     │
                          ┌──────────┴──────────┐
                          │                     │
                    ┌─────▼─────┐      ┌───────▼────────┐
                    │  OpenAI   │      │Claude / Gemini │
                    │    API    │      │      APIs      │
                    └───────────┘      └────────────────┘
```

---

## 📊 MONITORING & LOGGING

### Current Logging
- ExecutionLog model: All workflow events
- Django logging: Console output
- Admin panel: View logs

### Production Monitoring Needs
- **Application Monitoring**: Sentry, New Relic
- **API Monitoring**: Track API usage, costs, errors
- **Performance Monitoring**: Response times, query times
- **Error Tracking**: Exceptions, stack traces
- **Business Metrics**: Projects created, completion rate
- **Infrastructure Monitoring**: CPU, memory, disk

---

## 🧪 TESTING STRATEGY

### Current Testing
- Manual testing via UI
- Admin panel inspection
- ExecutionLog review

### Comprehensive Testing Plan
1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test module workflows
3. **API Tests**: Mock external API calls
4. **End-to-End Tests**: Full workflow simulation
5. **Load Tests**: Concurrent users, heavy queries
6. **Security Tests**: Vulnerability scanning
7. **UI Tests**: Selenium/Playwright

---

## 📝 MAINTENANCE & UPDATES

### Regular Maintenance
- Monitor API usage and costs
- Review ExecutionLog for errors
- Clean up old projects
- Update dependencies
- Backup database

### Update Strategy
- Version control with Git
- Feature branches
- Staging environment testing
- Database migration planning
- API version compatibility

---

## 🎯 FUTURE ENHANCEMENTS

### Phase 2 Features
- Historical tracking and trend analysis
- Email notifications on completion
- Export reports to PDF/Excel
- Scheduled periodic checks
- API for programmatic access
- Bulk project creation
- Team collaboration features
- Custom branding

### Phase 3 Features
- Machine learning for prediction
- Real-time monitoring
- Integration with SEO tools
- Social media monitoring
- Content recommendation engine
- A/B testing for strategies
- White-label solution

---

## 📚 REFERENCES

- **Django Documentation**: https://docs.djangoproject.com/
- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **OpenAI API**: https://platform.openai.com/docs/
- **Anthropic API**: https://docs.anthropic.com/
- **Google Gemini**: https://ai.google.dev/docs

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Maintainer**: Development Team
