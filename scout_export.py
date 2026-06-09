"""Helper script to export Scout Work IQ data to the app.

Run this from Scout to refresh the app's cached data with fresh Work IQ information.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def export_workiq_data_to_app(
    profile_data: dict,
    calendar_events: list,
    emails: list,
    chats: list,
    output_path: str = "sample_data/week_data_real.json"
) -> bool:
    """Export Scout Work IQ data to the app in the expected format.
    
    Args:
        profile_data: Result from workiq_get_my_profile()
        calendar_events: Result from workiq_list_events()
        emails: Result from workiq_list_emails()
        chats: Result from workiq_list_chats()
        output_path: Where to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Build the combined data structure
        data = {
            "user": {
                "displayName": profile_data.get("displayName", "User"),
                "jobTitle": profile_data.get("jobTitle", ""),
                "mail": profile_data.get("mail", ""),
            },
            "calendar_events": calendar_events if isinstance(calendar_events, list) else [],
            "emails": emails if isinstance(emails, list) else [],
            "teams_chats": chats if isinstance(chats, list) else [],
            "period": {
                "start": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
                "end": datetime.now(timezone.utc).isoformat(),
            },
        }
        
        # Save to JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported to {output_path}")
        print(f"   - {len(calendar_events)} calendar events")
        print(f"   - {len(emails)} emails")
        print(f"   - {len(chats)} Teams chats")
        return True
        
    except Exception as e:
        print(f"❌ Failed to export data: {e}")
        return False
