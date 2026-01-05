# 🚀 QUICK START GUIDE
# AI Visibility Tracker MVP

## ⚡ ONE-TIME SETUP (5 minutes)

### 1. Add Your API Keys to .env

Open the `.env` file (create it if it doesn't exist) and add:

```
OPENAI_API_KEY=sk-...your-key-here
CLAUDE_API_KEY=sk-ant-...your-key-here  
GEMINI_API_KEY=...your-key-here
DJANGO_SECRET_KEY=change-this-to-something-random
DEBUG=True
```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Claude: https://console.anthropic.com/
- Gemini: https://makersuite.google.com/app/apikey

### 2. Run the Server

```powershell
C:/Users/swast/anaconda3/python.exe manage.py runserver
```

### 3. Open Browser

Navigate to: http://localhost:8000/

---

## 📋 FIRST RUN CHECKLIST

✅ Anaconda environment active  
✅ All packages installed (`pip install -r requirements.txt`)  
✅ Migrations applied (`python manage.py migrate`)  
✅ AI models initialized (`python manage.py init_models`)  
✅ .env file created with API keys  
✅ Server running (`python manage.py runserver`)  

---

## 🎯 USAGE WORKFLOW

### 1. Create Account
- Click "Get Started" or "Sign Up"
- Fill in username, password
- Login

### 2. Create New Visibility Check
- Click "New Check"
- Enter your company details:
  - **Company Name**: e.g., "HubSpot"
  - **Description**: What your product/service does
  - **Category**: e.g., "CRM software", "Project Management"
- Click "Analyze Company"

### 3. Wait for AI Analysis (30-60 seconds)
- ChatGPT will analyze your company
- Discover competitors automatically
- Generate realistic prompts

### 4. Validate & Customize
- Review the refined company summary (edit if needed)
- Select which competitors to track
- Add custom competitors
- Choose which prompts to test
- Add custom prompts
- Click "Continue to Model Selection"

### 5. Select AI Models
- Choose models to query:
  - ✅ ChatGPT (recommended)
  - ✅ Claude
  - ✅ Gemini
- Click "Proceed to Execution"

### 6. Execute Check
- Review summary
- Click "Start Visibility Check"
- Wait 5-15 minutes (depends on # of prompts × models)

### 7. View Report
- Once complete, click "View Report"
- Explore:
  - 🏆 Visibility leaderboard
  - 📊 Competitor comparison
  - 🎯 Prompt-wise analysis
  - 🤖 Model-wise breakdown
  - 💡 Strategic insights
  - ✅ Action plan

---

## 🔧 COMMON COMMANDS

### Start Server
```powershell
C:/Users/swast/anaconda3/python.exe manage.py runserver
```

### Create Superuser (Admin Access)
```powershell
C:/Users/swast/anaconda3/python.exe manage.py createsuperuser
```

### Access Admin Panel
http://localhost:8000/admin/

### Reset Database (if needed)
```powershell
del db.sqlite3
C:/Users/swast/anaconda3/python.exe manage.py migrate
C:/Users/swast/anaconda3/python.exe manage.py init_models
```

---

## ⚠️ TROUBLESHOOTING

### "Module not found" errors
```powershell
C:/Users/swast/anaconda3/Scripts/activate
pip install -r requirements.txt
```

### "API key invalid" errors
- Check .env file exists in project root
- Verify API keys are correct
- Ensure no extra spaces in .env

### Server won't start
- Check if port 8000 is already in use
- Use different port: `python manage.py runserver 8080`

### Slow execution
- Reduce number of prompts (select 3-5 instead of all)
- Reduce number of models (use only ChatGPT for testing)
- Check your API rate limits

### Background task not running
- Check ExecutionLog in admin panel
- Look for error messages in terminal
- Verify API keys have sufficient quota

---

## 📊 UNDERSTANDING THE SCORES

### Visibility Score (0-100%)
Combined metric of:
1. **Frequency** (0-1): % of prompts mentioning brand
2. **Prominence** (0-1): Average position (1st = 1.0, 2nd = 0.5, etc.)
3. **Sentiment** (0.5-1.2): 
   - Very Positive = 1.2
   - Positive = 1.0
   - Neutral = 0.8
   - Negative = 0.5
4. **Model Coverage** (0.8-1.0): Weighted by model importance

**Formula:**  
`Score = Frequency × Prominence × Sentiment × Model Coverage`  
Normalized to 0-100 scale

### What's a Good Score?
- **80-100%**: Dominant visibility
- **60-80%**: Strong presence
- **40-60%**: Moderate visibility
- **20-40%**: Weak presence
- **0-20%**: Rarely mentioned

---

## 🎓 TIPS FOR BEST RESULTS

### 1. Company Description
- Be specific about what you do
- Mention key features/benefits
- Include target audience

### 2. Competitor Selection
- Focus on direct competitors
- Include market leaders
- Mix established and emerging brands

### 3. Prompt Creation
- Use natural language
- Ask questions users would really ask
- Cover different angles:
  - "Best [category] for [use case]"
  - "Compare X vs Y"
  - "Alternatives to [competitor]"
  - "Top [category] tools"

### 4. Model Selection
- Always include ChatGPT (most important)
- Add Claude for comparison
- Add Gemini for broader coverage

---

## 📈 EXAMPLE TEST RUN

**Company:** DocuSign  
**Description:** Electronic signature and document management platform  
**Category:** Document management software

**Expected Competitors:** Adobe Sign, HelloSign, PandaDoc, SignNow

**Sample Prompts:**
- "What's the best e-signature tool for businesses?"
- "DocuSign vs Adobe Sign comparison"
- "Alternatives to DocuSign"
- "Top document signing platforms"

**Expected Results:**
- Visibility scores for DocuSign vs competitors
- Position in AI recommendations
- Sentiment analysis
- Actionable insights

---

## 🔒 IMPORTANT NOTES

1. **API Costs**: Each check makes multiple API calls. Monitor your usage.
2. **Rate Limits**: Respect API provider rate limits
3. **Data Privacy**: All data stored locally in SQLite
4. **Development Only**: This is an MVP - not production-ready
5. **Background Tasks**: Use threading (simple but not scalable)

---

## 🆘 NEED HELP?

1. Check Django admin for ExecutionLog
2. Review terminal output for errors
3. Verify .env file configuration
4. Check README.md for detailed docs

---

## ✨ NEXT STEPS

After getting your first report:

1. **Analyze Gaps**: Where do competitors win?
2. **Review Insights**: Why are you less visible?
3. **Action Plan**: Follow the recommendations
4. **Track Changes**: Re-run after implementing changes
5. **Competitor Mode**: Impersonate competitors to understand their strategy

---

## 🎉 YOU'RE READY!

Start the server and create your first visibility check!

```powershell
C:/Users/swast/anaconda3/python.exe manage.py runserver
```

Then open: http://localhost:8000/
