# Week in Review - Hackathon Submission Checklist

## ✅ Before uploading to GitHub:

### 1. **REMOVE SENSITIVE DATA** (CRITICAL!)
- [ ] Delete `sample_data/week_data_real.json` (contains your real calendar, emails, Teams data)
- [ ] Keep `sample_data/sample_week.json` (demo data with fictional names)
- [ ] `.env` is already in `.gitignore` so it won't be committed (verified)

### 2. **Verify .gitignore is working**
```bash
# Before git push, check what will be committed:
git status
# Should NOT show: .env, __pycache__/, *.pyc, .venv/
```

### 3. **Verify Secrets**
- [ ] `GITHUB_TOKEN` is safe in `.env` (not committed)
- [ ] `MS_CLIENT_ID` is a placeholder (safe)
- [ ] No API keys in Python files

### 4. **Code is clean**
- [ ] Remove any debug comments
- [ ] Check `README.md` is updated with setup instructions
- [ ] Verify requirements.txt includes all dependencies

### 5. **Optional: Regenerate token**
If you want to be extra safe:
1. Go to https://github.com/settings/tokens
2. Rotate your `github_pat_11ALG72...` token
3. Update `.env` locally (won't be committed)

---

## 🎥 Creating the submission video:

### What to show (5-7 minutes):
1. **Intro (20 sec):**
   - "Week in Review - AI Hackathon Project"
   - Brief description of what it does

2. **Architecture (1 min):**
   - Show the project structure
   - Explain: Scout → Python app → GitHub Models (GPT-4o)

3. **Live Demo (4 min):**
   - Open http://localhost:8000
   - Show the UI
   - Click "Generate Review"
   - Show the AI-generated story (wait for response)
   - Show how beautiful the HTML story is

4. **Code walkthrough (1 min):**
   - Show key files: `story_generator.py`, `app.py`
   - Explain the integration with Scout

5. **Closing (30 sec):**
   - "No Entra ID app registration needed"
   - "Fully integrated with Scout via workiq_* tools"
   - "Automation runs every Monday"

### Tools to use:
- **Windows:** OBS Studio (free) or QuickTime
- **Simple:** ScreenFlow, Camtasia, or even PowerPoint record-screen
- Record at 1080p 30fps
- Keep audio clear

---

## 📝 Git Push Commands:

```bash
cd C:\Users\bidhan.dey\Downloads\MSHackathon

# Remove real data (IMPORTANT!)
rm sample_data/week_data_real.json

# Check what's being committed
git status

# If git repo doesn't exist yet:
git init
git add .
git commit -m "Week in Review - AI Hackathon Project"
git branch -M main
git remote add origin https://github.com/<your-username>/mshackathon.git
git push -u origin main
```

---

## ✨ Final checks before submission:

- [ ] `week_data_real.json` deleted (privacy)
- [ ] `.env` not in repo (checked via `.gitignore`)
- [ ] `README.md` has clear setup instructions
- [ ] Demo video recorded and uploaded
- [ ] Project is public on GitHub
- [ ] Video link in README or submission form
