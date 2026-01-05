"""
TESTING CHECKLIST FOR AI VISIBILITY TRACKER MVP
Complete this checklist to verify all modules work correctly
"""

# ============================================================
# PRE-FLIGHT CHECKS
# ============================================================

## 1. Environment Setup
□ Anaconda environment activated
□ All dependencies installed (pip list shows all packages)
□ .env file exists with valid API keys
□ Database migrated (db.sqlite3 exists)
□ AI models initialized
□ Static directory created

## 2. API Keys Valid
□ OPENAI_API_KEY works (test with simple request)
□ CLAUDE_API_KEY works
□ GEMINI_API_KEY works
□ Keys have sufficient quota/credits

# ============================================================
# MODULE 1: USER INTERFACE PART
# ============================================================

## Test 1: Authentication
□ Server starts without errors
□ Homepage loads at http://localhost:8000/
□ Sign up page works
□ Can create new account
□ Login page works
□ Can login with created account
□ Logout works
□ Redirect to login when accessing protected pages

## Test 2: Project Creation
□ Dashboard loads after login
□ "New Check" button visible
□ Create project page loads
□ Form validation works (empty fields rejected)
□ Can submit company details
□ Background thread starts (Module 1 workflow)
□ Redirects to validation page

## Test 3: AI Analysis (Module 1 Workflow)
□ Company analysis completes (check ExecutionLog)
□ Refined summary generated
□ Competitors discovered (5-7 competitors)
□ Prompts generated (8-12 prompts)
□ No errors in ExecutionLog
□ Page refreshes show updated data

## Test 4: Validation & Customization
□ Refined summary displayed
□ Can edit summary
□ Competitors listed with checkboxes
□ Can select/deselect competitors
□ Can add custom competitors
□ Prompts listed with checkboxes
□ Can select/deselect prompts
□ Can add custom prompts
□ Submit works, redirects to model selection

## Test 5: Model Selection
□ Model selection page loads
□ All 3 models displayed (ChatGPT, Claude, Gemini)
□ Checkboxes work
□ Weights displayed correctly
□ Submit creates ModelSelection records
□ Redirects to execute page

# ============================================================
# MODULE 2: VISIBILITY CHECK ENGINE
# ============================================================

## Test 6: Execution Setup
□ Execute page loads
□ Summary displays correctly:
  - Selected prompts count
  - Selected models count
  - Total queries calculated
□ "Start Check" button works
□ Background thread starts
□ Redirects to status page

## Test 7: Model Querying
□ PromptResponse records created
□ API calls made to selected models
□ Responses stored successfully
□ Retry logic works (simulate failure if possible)
□ Error handling graceful
□ ExecutionLog entries created
□ Status updates to 'checking'

## Test 8: Brand Mention Extraction
□ BrandMention records created
□ Brand names extracted correctly
□ Positions calculated (1st, 2nd, 3rd...)
□ Context captured
□ Main brand vs competitors identified
□ All mentions from all responses extracted

## Test 9: Sentiment Analysis
□ SentimentScore records created for each mention
□ ChatGPT sentiment analysis works
□ Sentiment categories correct (very_positive, positive, neutral, negative)
□ Reasoning captured
□ No mentions left unanalyzed

## Test 10: Score Calculation
□ VisibilityScore records created
□ Frequency calculated correctly
□ Prominence calculated correctly
□ Sentiment weighted correctly
□ Model coverage weighted correctly
□ Raw score computed
□ Normalized score (0-100) calculated
□ Scores for all brands (main + competitors)

# ============================================================
# MODULE 3: ANALYSIS & THINK ENGINE
# ============================================================

## Test 11: Status Monitoring
□ Status page auto-refreshes
□ Status updates from 'checking' to 'analyzing'
□ API endpoint (/api/project/X/status/) works
□ Loading animation displays
□ Completes without hanging

## Test 12: Report Generation
□ Status updates to 'completed'
□ DetailedReport record created
□ Competitor comparison generated
□ Prompt-wise analysis generated
□ Model-wise analysis generated
□ Negative sentiment analysis generated
□ Research sources extracted (if any)

## Test 13: AI-Generated Insights
□ ChatGPT insights generation works
□ "Why competitors win" generated
□ "Content gaps" identified
□ "Messaging gaps" identified
□ "Positioning weaknesses" identified
□ Insights are relevant and actionable

## Test 14: Action Plan
□ Content ideas generated (5-7 items)
□ SEO/PR recommendations generated (5-7 items)
□ Messaging improvements generated (5-7 items)
□ Recommendations are specific and actionable

## Test 15: Report Display
□ "View Report" button appears
□ Report page loads
□ Leaderboard displays correctly
□ Scores sorted by visibility
□ Main brand highlighted
□ All sections visible:
  - Competitor comparison
  - Prompt-wise analysis
  - Model-wise analysis
  - Negative sentiment (if any)
  - Insights
  - Action plan
□ Data accurate and complete

# ============================================================
# ADVANCED FEATURES
# ============================================================

## Test 16: Competitor Impersonation
□ "Impersonate" button visible on report
□ Clicking creates new project
□ Competitor becomes main brand
□ Original company becomes competitor
□ Can run full workflow from competitor perspective
□ Separate report generated

## Test 17: Multiple Projects
□ Dashboard shows all projects
□ Can create multiple projects
□ Each project independent
□ Status badges correct
□ Can access any project report

## Test 18: Admin Panel
□ Admin panel accessible (/admin/)
□ Can view all models
□ ExecutionLog searchable and filterable
□ Can view project details
□ Can manually edit if needed

# ============================================================
# ERROR HANDLING & EDGE CASES
# ============================================================

## Test 19: API Failures
□ Retry logic triggers on failure
□ Exponential backoff works
□ Partial data handled gracefully
□ Status marked as 'partial' when appropriate
□ Workflow continues despite failures
□ Error messages logged

## Test 20: Empty/Invalid Data
□ No competitors found → workflow continues
□ No prompts generated → fallback works
□ No mentions found → zero scores calculated
□ Invalid JSON responses → fallback handling
□ Empty API responses → handled gracefully

## Test 21: Rate Limits
□ Rate limit errors caught
□ Retry with backoff
□ User notified if persistent
□ Doesn't crash application

# ============================================================
# PERFORMANCE & USABILITY
# ============================================================

## Test 22: Response Times
□ Page loads < 2 seconds
□ Module 1 completes in 1-2 minutes
□ Module 2 completes in 5-10 minutes (depends on volume)
□ Module 3 completes in 2-3 minutes
□ Total workflow < 15 minutes

## Test 23: UI/UX
□ Navigation intuitive
□ Messages clear and helpful
□ Loading states visible
□ Errors displayed to user
□ Success confirmations shown
□ Responsive layout
□ Readable fonts and colors

## Test 24: Data Integrity
□ All database relationships correct
□ No orphaned records
□ Cascade deletes work
□ Unique constraints enforced
□ Data consistent across tables

# ============================================================
# REAL-WORLD TEST SCENARIO
# ============================================================

## Test 25: Complete Workflow

SCENARIO: Test with a real company

1. Company: "Notion"
   - Description: "All-in-one workspace for notes, docs, wikis, and project management"
   - Category: "Productivity software"

2. Expected Competitors:
   - Monday.com, Asana, ClickUp, Airtable, Coda

3. Sample Prompts:
   - "What's the best project management tool?"
   - "Notion vs Monday.com"
   - "Top productivity apps for teams"

4. Expected Results:
   - Notion mentioned in 60-80% of prompts
   - Competitors also mentioned
   - Sentiment mostly positive
   - Actionable insights generated

CHECKLIST:
□ Created project with Notion details
□ AI discovered expected competitors
□ AI generated relevant prompts
□ Validated and selected data
□ Selected all 3 models
□ Execution completed successfully
□ Visibility scores calculated
□ Notion's score reasonable (50-80%)
□ Competitors ranked logically
□ Insights relevant to productivity software
□ Action plan specific to Notion's positioning
□ Report comprehensive and useful

# ============================================================
# FINAL VERIFICATION
# ============================================================

## Test 26: End-to-End
□ New user can sign up
□ Complete entire workflow without assistance
□ Understand the results
□ Find value in the insights
□ Can repeat for different companies
□ No crashes or blocking errors

## Test 27: Documentation
□ README.md accurate
□ QUICKSTART.md helpful
□ Code comments clear
□ Error messages informative
□ Admin documentation sufficient

# ============================================================
# PRODUCTION READINESS (MVP)
# ============================================================

## MVP Checklist
□ All critical features work
□ Error handling comprehensive
□ User experience acceptable
□ Data accuracy validated
□ Performance adequate
□ Security basics covered
□ Documentation complete

## Known Limitations (Document These)
□ No Celery (uses threading)
□ SQLite only (not PostgreSQL)
□ No email notifications
□ No historical tracking
□ No export to PDF
□ No API rate limit management
□ No scheduled checks
□ No multi-tenancy
□ No Docker containerization
□ Development server only

# ============================================================
# SIGN-OFF
# ============================================================

Date: _________________
Tester: _______________
Version: MVP v1.0

□ All critical tests passed
□ Known issues documented
□ Ready for demonstration
□ Ready for user acceptance testing

Notes:

Need to add own API keys in .env file to test it. 
_______________________________________
_______________________________________
_______________________________________
