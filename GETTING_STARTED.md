# 🚀 GETTING STARTED - AI VISIBILITY TRACKER

Welcome! This guide will get you up and running in **5 minutes**.

---

## 📋 PREREQUISITES

Before you begin, ensure you have:

- ✅ **Python 3.10+** (via Anaconda)
- ✅ **API Keys** from:
  - [OpenAI](https://platform.openai.com/api-keys) - **REQUIRED**
  - [Anthropic](https://console.anthropic.com/) - Optional
  - [Google AI](https://makersuite.google.com/app/apikey) - Optional

---

## ⚡ QUICK START (5 Minutes)

### Step 1: Configure API Keys (2 minutes)

Open the `.env` file in the project root and add your API keys:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxx
DJANGO_SECRET_KEY=change-this-to-something-random
DEBUG=True
```

**Note**: At minimum, you need the **OPENAI_API_KEY** to run the application.

### Step 2: Verify Setup (1 minute)

Run the verification script to check everything is configured:

```powershell
C:/Users/swast/anaconda3/python.exe verify_setup.py
```

This will check:
- Python version
- API keys
- Dependencies
- Database
- Migrations

### Step 3: Start the Server (30 seconds)

**Option A: Using the batch script (Windows)**
```powershell
start_server.bat
```

**Option B: Manual command**
```powershell
C:/Users/swast/anaconda3/python.exe manage.py runserver
```

### Step 4: Open Your Browser (30 seconds)

Navigate to: **http://localhost:8000/**

You should see the AI Visibility Tracker homepage!

---

## 🎯 YOUR FIRST VISIBILITY CHECK (10 Minutes)

### 1. Create an Account
- Click **"Get Started"** or **"Sign Up"**
- Enter username and password
- Click **"Sign Up"**

### 2. Create Your First Project
- Click **"New Check"** or **"Create New Visibility Check"**
- Fill in the form:
  - **Company Name**: e.g., "HubSpot"
  - **Company Description**: What does your company do?
  - **Area of Work**: e.g., "CRM software"
- Click **"Analyze Company"**

### 3. Wait for AI Analysis (1-2 minutes)
The system will:
- ✅ Analyze your company with ChatGPT
- ✅ Discover 5-7 main competitors
- ✅ Generate 8-12 realistic prompts

**Tip**: Watch the terminal/console for progress updates.

### 4. Validate & Customize (2 minutes)
- **Review** the refined company summary
- **Select** which competitors to track
- **Add** custom competitors if needed
- **Choose** which prompts to test
- **Add** custom prompts if needed
- Click **"Continue to Model Selection"**

### 5. Select AI Models (30 seconds)
- ✅ **ChatGPT** (highly recommended)
- ✅ **Claude** (optional but recommended)
- ✅ **Gemini** (optional)
- Click **"Proceed to Execution"**

### 6. Execute Visibility Check (5-15 minutes)
- Review the summary (number of prompts × models)
- Click **"Start Visibility Check"**
- The page will redirect to status monitoring
- **Relax**: The system works in the background

**What's Happening?**
- 🔍 Querying selected AI models
- 📊 Extracting brand mentions
- 💭 Analyzing sentiment
- 🧮 Calculating visibility scores
- 🧠 Generating insights

### 7. View Your Report (when complete)
- Status page will auto-refresh
- When complete, click **"View Report"**
- Explore your comprehensive visibility analysis!

---

## 📊 UNDERSTANDING YOUR REPORT

### Visibility Score (0-100%)
- **80-100%**: Dominant visibility (excellent!)
- **60-80%**: Strong presence (good)
- **40-60%**: Moderate visibility (room for improvement)
- **20-40%**: Weak presence (action needed)
- **0-20%**: Rarely mentioned (significant work needed)

### Report Sections

1. **🏆 Visibility Leaderboard**
   - Your brand vs competitors ranked by score
   - Shows who dominates AI recommendations

2. **📊 Competitor Analysis**
   - Gap analysis: how far behind you are
   - Frequency, prominence, sentiment breakdown

3. **🎯 Prompt-Wise Performance**
   - Which prompts mention your brand
   - Your position in each answer
   - Who wins each prompt

4. **🤖 Model-Wise Performance**
   - How you perform on ChatGPT vs Claude vs Gemini
   - Model-specific insights

5. **⚠️ Negative Sentiment** (if any)
   - Where negative mentions occur
   - Context and reasoning
   - Action items

6. **💡 Strategic Insights**
   - Why competitors win
   - Content gaps
   - Messaging gaps
   - Positioning weaknesses

7. **✅ Action Plan**
   - 5-7 content ideas
   - 5-7 SEO/PR recommendations
   - 5-7 messaging improvements

---

## 🎭 ADVANCED: COMPETITOR IMPERSONATION

Want to see how the world looks from your competitor's perspective?

1. Go to your report
2. Find a competitor in the leaderboard
3. Click **"Impersonate"**
4. The system creates a new project with:
   - Competitor as the main brand
   - Your company as a competitor
   - Same prompts and analysis
5. Run the full workflow again
6. Compare reports!

**Use Case**: Understand why competitors rank higher, what their strengths are.

---

## 🔧 COMMON ISSUES & SOLUTIONS

### Issue: "API key invalid"
**Solution**: 
- Check your .env file
- Ensure no extra spaces in the API key
- Verify key is active on provider's website

### Issue: "Module not found" error
**Solution**:
```powershell
C:/Users/swast/anaconda3/Scripts/activate
pip install -r requirements.txt
```

### Issue: Server won't start
**Solution**:
- Check if port 8000 is in use
- Use different port: `python manage.py runserver 8080`
- Check for Python errors in terminal

### Issue: Background task not running
**Solution**:
- Check ExecutionLog in admin panel: http://localhost:8000/admin/
- Look for error messages
- Verify API quotas/limits

### Issue: Slow execution
**Solution**:
- Select fewer prompts (3-5 for testing)
- Use only ChatGPT initially
- Check your API rate limits

---

## 💡 TIPS FOR BEST RESULTS

### Writing Company Descriptions
✅ **Good**: "HubSpot is an all-in-one CRM platform that helps businesses grow with marketing, sales, and service tools"

❌ **Bad**: "We make software"

### Selecting Prompts
Include variety:
- Best/top lists: "Best CRM for startups"
- Comparisons: "HubSpot vs Salesforce"
- Use cases: "CRM with email marketing"
- Alternatives: "Alternatives to [competitor]"

### Choosing Models
- **ChatGPT**: Always include (most important)
- **Claude**: Add for comparison
- **Gemini**: Add for comprehensive coverage

---

## 📚 NEXT STEPS

### After Your First Report
1. **Analyze**: Study the gaps and insights
2. **Plan**: Review the action items
3. **Implement**: Start with quick wins
4. **Track**: Run again in 2-4 weeks to measure progress

### Learn More
- **README.md**: Comprehensive project documentation
- **ARCHITECTURE.md**: Technical deep dive
- **TESTING_CHECKLIST.md**: Testing guide

---

## 🆘 NEED HELP?

### Check These Resources
1. **ExecutionLog**: Django admin → Execution logs
2. **Terminal Output**: Look for error messages
3. **verify_setup.py**: Run to check configuration
4. **TESTING_CHECKLIST.md**: Complete testing guide

### Common Questions

**Q: How long does a check take?**
A: 5-15 minutes depending on (prompts × models). Example: 5 prompts × 3 models = 15 API calls ≈ 5-10 minutes.

**Q: How much do API calls cost?**
A: Varies by provider. Example: ~$0.50-2.00 for a typical check with 5 prompts × 3 models.

**Q: Can I run multiple checks simultaneously?**
A: Yes, but each runs sequentially in its own thread.

**Q: Can I export the report?**
A: Not yet in MVP. Copy/paste or screenshot for now.

**Q: Can I schedule regular checks?**
A: Not yet in MVP. Run manually for now.

---

## ✨ EXAMPLE: REALISTIC TEST

Let's run a test with a real company:

**Company**: Notion  
**Description**: All-in-one workspace for notes, docs, wikis, and project management  
**Category**: Productivity software

**Expected Competitors**:
- Monday.com
- Asana
- ClickUp
- Airtable
- Coda

**Sample Prompts**:
- "What's the best project management tool for remote teams?"
- "Notion vs Monday.com comparison"
- "Top productivity apps for startups"
- "Alternatives to Notion"
- "Best knowledge management software"

**Expected Results**:
- Notion visibility: 60-80%
- Top competitors: Monday.com, Asana
- Insights: Productivity workflow positioning
- Action items: Content marketing ideas

**Try it yourself!** Use Notion as your test case to see how the system works.

---

## 🎉 YOU'RE READY!

Start the server and create your first visibility check:

```powershell
C:/Users/swast/anaconda3/python.exe manage.py runserver
```

Then open: **http://localhost:8000/**

**Good luck!** 🚀

---

**Questions?** Check the documentation or run `verify_setup.py` to diagnose issues.
