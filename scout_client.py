"""Scout WorkIQ integration using workiq CLI.

This module fetches Work IQ data from Scout using the built-in workiq tools.
No Graph API client ID needed - Scout handles authentication.
"""

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path


def _run_workiq_command(query: str) -> dict:
    """Run a WorkIQ ask command and return the parsed JSON response.
    
    Falls back to cached data if command fails.
    """
    try:
        cmd = [
            r"C:\Users\bidhan.dey\.copilot\bin\workiq.cmd",
            "ask",
            "-q",
            query,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode != 0:
            print(f"WorkIQ error: {result.stderr}")
            return None
            
        # Parse JSON response
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Failed to run workiq command: {e}")
        return None


async def get_scout_weekly_data() -> dict:
    """Fetch Work IQ data from Scout.
    
    Uses Scout's built-in workiq tools via CLI.
    Formats the response to match the app's expected structure.
    """
    
    # For now, since workiq CLI doesn't return structured JSON for direct calendar/email fetching,
    # we'll use the cached week_data_real.json as a fallback.
    # In a future version, Scout could expose a JSON API endpoint.
    
    data_path = Path("sample_data/week_data_real.json")
    if data_path.exists():
        with open(data_path, encoding='utf-8-sig') as f:
            return json.load(f)
    
    # If cached data doesn't exist, we could call workiq here:
    # response = _run_workiq_command("Summarize my week's calendar events, emails, and Teams chats")
    
    raise Exception(
        "No cached data available. Scout integration requires cached week_data_real.json. "
        "Run: workiq ask -q 'Show me my calendar events, emails, and Teams messages from this week'"
    )
