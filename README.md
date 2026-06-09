# 📖 Week in Review — Your Work Week, Reimagined as a Story

> Built for the **Agents League Hackathon 2026** | Track: 🎨 Creative Apps

## What is it?

**Week in Review** is a creative AI application that transforms your Microsoft 365 work week into an engaging, magazine-style narrative story. It connects to your calendar, emails, and Teams conversations via **Microsoft Work IQ**, then uses **GitHub Models (GPT-4o)** to craft a personalized, entertaining summary of your week.

Think of it as your personal journalist, turning mundane meetings and emails into a compelling story where YOU are the protagonist.

## 🎯 Microsoft IQ Integration

This project integrates **Work IQ** — the Microsoft 365 intelligence layer:
- 📅 **Calendar Events** — Meetings, their attendees, and time patterns
- 📧 **Emails** — Key conversations and threads
- 💬 **Teams Chats** — Collaboration highlights

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python + FastAPI |
| AI/LLM | GitHub Models (GPT-4o) |
| M365 Auth | MSAL (Device Code Flow) |
| M365 Data | Microsoft Graph API (Work IQ) |
| Frontend | HTML + CSS (Jinja2 templates) |
| Dev Tool | GitHub Copilot (AI-assisted development) |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A GitHub account with Copilot access (for GitHub Models)
- A Microsoft 365 account (for live mode)
- An Azure AD app registration (see Setup below)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/week-in-review.git
cd week-in-review

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
copy .env.example .env
# Edit .env with your values
```

### Azure AD App Registration

1. Go to [Entra ID (Azure AD)](https://entra.microsoft.com) → App registrations → New registration
2. Name: `Week in Review`
3. Supported account types: "Accounts in any organizational directory"
4. Redirect URI: Leave blank (we use Device Code Flow)
5. After creation, note the **Application (client) ID** and **Directory (tenant) ID**
6. Go to API permissions → Add permission → Microsoft Graph → Delegated:
   - `User.Read`
   - `Mail.Read`
   - `Calendars.Read`
   - `Chat.Read`
7. Under Authentication → Advanced settings → Enable "Allow public client flows" = **Yes**

### GitHub Models Token

1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Create a Fine-Grained Personal Access Token
3. Under "Permissions" → enable access to GitHub Models
4. Copy the token to your `.env` file

### Run the App

```bash
python app.py
```

Then open http://localhost:8000

### Demo Mode (No Auth Required)

Click **"Try Demo"** on the homepage to see the app generate a story from sample data — no Microsoft 365 sign-in needed!

## 📸 Screenshots

_Coming soon — demo video will be added before submission._

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│           User Browser               │
│         (localhost:8000)             │
└───────────────┬──────────────────────┘
                │
┌───────────────▼──────────────────────┐
│         FastAPI Backend              │
│                                      │
│  ┌─────────────┐  ┌───────────────┐ │
│  │ Graph Client│  │Story Generator│ │
│  │  (Work IQ)  │  │(GitHub Models)│ │
│  └──────┬──────┘  └───────┬───────┘ │
└─────────┼──────────────────┼─────────┘
          │                  │
┌─────────▼────────┐ ┌──────▼─────────┐
│ Microsoft Graph  │ │ GitHub Models  │
│  (M365 Data)     │ │   (GPT-4o)    │
│  • Calendar      │ │               │
│  • Mail          │ │  AI Narrative │
│  • Teams         │ │  Generation   │
└──────────────────┘ └───────────────┘
```

## 🎨 Features

- **Live Mode**: Authenticates with your M365 account and generates a real story from your actual week
- **Demo Mode**: Generates a story from sample data (perfect for judges without M365 access)
- **Creative Narratives**: Each generation is unique — different tones, themes, and metaphors
- **Magazine Style**: Beautiful HTML output with styled sections, stats, and mood indicators
- **Regenerate**: Not happy with the story? Hit regenerate for a fresh take!

## 📝 License

MIT

## 🙏 Acknowledgments

- Built with AI-assisted development using **GitHub Copilot**
- Microsoft **Work IQ** for the M365 intelligence layer
- **GitHub Models** for creative AI generation
- **Agents League Hackathon 2026** for the inspiration!
