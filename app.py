"""Week in Review - Creative Story Generator powered by Work IQ.

A creative app that transforms your Microsoft 365 work week into 
an engaging narrative story using GitHub Models AI.
"""

import json
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from graph_client import get_weekly_data
from story_generator import generate_story, generate_story_from_sample

app = FastAPI(title="Week in Review", description="Your work week, reimagined as a story")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate_review(request: Request):
    """Generate Week in Review from cached Work IQ data."""
    try:
        # Try to load cached data first (most reliable)
        data_path = Path("sample_data/week_data_real.json")
        if data_path.exists():
            with open(data_path, encoding='utf-8-sig') as f:
                weekly_data = json.load(f)
        else:
            return templates.TemplateResponse(
                "error.html",
                {"request": request, "error": """
                    No cached data found. Please:
                    1. Click "Refresh from Scout" button above to fetch fresh data
                    2. Or use the cached sample data with "Generate Demo"
                """},
            )
        story_html = await generate_story(weekly_data)
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "story": story_html, "mode": "live"},
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
        )


@app.post("/generate-demo", response_class=HTMLResponse)
async def generate_demo(request: Request):
    """Generate Week in Review from sample data (no auth needed)."""
    sample_path = Path("sample_data/sample_week.json")
    if not sample_path.exists():
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Sample data not found. Run with live data instead."},
        )

    with open(sample_path, encoding='utf-8-sig') as f:
        sample_data = json.load(f)

    story_html = await generate_story_from_sample(sample_data)
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "story": story_html, "mode": "demo"},
    )


@app.post("/api/refresh-from-scout")
async def refresh_from_scout():
    """Endpoint that returns instructions for Scout to refresh data.
    
    Workflow:
    1. User clicks "Refresh from Scout" in the app
    2. This endpoint returns instructions
    3. User comes back to Scout (this interface)
    4. Scout fetches fresh data via workiq_* tools
    5. Data is saved to sample_data/week_data_real.json
    6. User clicks "Generate Review" in the app
    """
    from fastapi.responses import JSONResponse
    return JSONResponse({
        "status": "awaiting-scout-data",
        "message": "Scout is ready to fetch your fresh Work IQ data!",
        "instructions": "Go back to Scout and I'll fetch your latest calendar events, emails, and Teams chats",
        "next_step": "After Scout fetches the data, come back and click 'Generate Review' to create your story"
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
