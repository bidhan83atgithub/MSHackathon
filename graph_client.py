"""Microsoft Graph client for Work IQ integration.

Uses MSAL with Device Code Flow for authentication.
Pulls calendar events, emails, and Teams chats for the past week.
"""

import msal
import httpx
from datetime import datetime, timedelta, timezone
from config import MS_CLIENT_ID, MS_AUTHORITY, MS_SCOPES

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

_token_cache = msal.SerializableTokenCache()
_app = None
_access_token = None


def _get_msal_app():
    global _app
    if _app is None:
        _app = msal.PublicClientApplication(
            MS_CLIENT_ID,
            authority=MS_AUTHORITY,
            token_cache=_token_cache,
        )
    return _app


def get_access_token() -> str:
    """Get access token, using cache if available."""
    global _access_token
    app = _get_msal_app()

    # Try silent token acquisition first
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(MS_SCOPES, account=accounts[0])
        if result and "access_token" in result:
            _access_token = result["access_token"]
            return _access_token

    # Fall back to device code flow
    flow = app.initiate_device_flow(scopes=MS_SCOPES)
    if "user_code" not in flow:
        raise Exception(f"Failed to initiate device flow: {flow}")

    print(f"\n{'='*60}")
    print(f"🔐 To sign in, visit: {flow['verification_uri']}")
    print(f"   Enter code: {flow['user_code']}")
    print(f"{'='*60}\n")

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        _access_token = result["access_token"]
        return _access_token
    else:
        raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")


def _get_headers():
    token = get_access_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


async def get_user_profile() -> dict:
    """Get the signed-in user's profile."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{GRAPH_BASE}/me", headers=_get_headers())
        resp.raise_for_status()
        return resp.json()


async def get_week_calendar_events() -> list:
    """Get calendar events from the past 7 days."""
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    params = {
        "startDateTime": week_ago.isoformat(),
        "endDateTime": now.isoformat(),
        "$orderby": "start/dateTime",
        "$top": "50",
        "$select": "subject,start,end,location,organizer,attendees,isAllDay",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GRAPH_BASE}/me/calendarView",
            headers=_get_headers(),
            params=params,
        )
        resp.raise_for_status()
        return resp.json().get("value", [])


async def get_week_emails() -> list:
    """Get sent and received emails from the past 7 days."""
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    filter_query = f"receivedDateTime ge {week_ago.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    params = {
        "$filter": filter_query,
        "$orderby": "receivedDateTime desc",
        "$top": "30",
        "$select": "subject,from,toRecipients,receivedDateTime,bodyPreview",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GRAPH_BASE}/me/messages",
            headers=_get_headers(),
            params=params,
        )
        resp.raise_for_status()
        return resp.json().get("value", [])


async def get_week_chats() -> list:
    """Get recent Teams chat messages."""
    async with httpx.AsyncClient() as client:
        # Get recent chats
        resp = await client.get(
            f"{GRAPH_BASE}/me/chats",
            headers=_get_headers(),
            params={"$top": "10", "$orderby": "lastMessagePreview/createdDateTime desc"},
        )
        resp.raise_for_status()
        chats = resp.json().get("value", [])

        messages = []
        for chat in chats[:5]:
            chat_id = chat["id"]
            msg_resp = await client.get(
                f"{GRAPH_BASE}/me/chats/{chat_id}/messages",
                headers=_get_headers(),
                params={"$top": "10"},
            )
            if msg_resp.status_code == 200:
                chat_messages = msg_resp.json().get("value", [])
                for msg in chat_messages:
                    if msg.get("body", {}).get("content"):
                        messages.append({
                            "chatId": chat_id,
                            "chatTopic": chat.get("topic", "Direct Message"),
                            "from": msg.get("from", {}).get("user", {}).get("displayName", "Unknown"),
                            "content": msg.get("body", {}).get("content", "")[:200],
                            "createdDateTime": msg.get("createdDateTime", ""),
                        })

        return messages


async def get_weekly_data() -> dict:
    """Fetch all Work IQ data for the past week."""
    profile = await get_user_profile()
    events = await get_week_calendar_events()
    emails = await get_week_emails()
    chats = await get_week_chats()

    return {
        "user": profile,
        "calendar_events": events,
        "emails": emails,
        "teams_chats": chats,
        "period": {
            "start": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            "end": datetime.now(timezone.utc).isoformat(),
        },
    }
