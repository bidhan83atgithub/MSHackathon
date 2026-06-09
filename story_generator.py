"""Creative story generator using GitHub Models (GPT-4o).

Takes Work IQ data and transforms it into an engaging narrative.
"""

from openai import OpenAI
from config import GITHUB_TOKEN, GITHUB_MODEL, GITHUB_MODELS_ENDPOINT

client = OpenAI(
    base_url=GITHUB_MODELS_ENDPOINT,
    api_key=GITHUB_TOKEN,
)

SYSTEM_PROMPT = """You are a creative storyteller and journalist. Your job is to take 
a person's weekly work data (calendar events, emails, Teams chats) and transform it 
into an engaging, entertaining "Week in Review" narrative.

Your output should be in HTML format with the following structure:
1. A catchy headline/title for the week
2. An opening paragraph that sets the tone (like a magazine article)
3. "Chapter" sections for major themes/projects of the week
4. Fun statistics sidebar (e.g., "meetings attended: 12", "emails conquered: 45")
5. A "Plot Twist" section highlighting something unexpected
6. A closing "Next Week Preview" teaser
7. An overall "mood" or "genre" for the week (e.g., "Action-Adventure", "Mystery", "Comedy")

Style guidelines:
- Write like a witty magazine journalist covering someone's work week
- Use metaphors and storytelling techniques (foreshadowing, callbacks, cliffhangers)
- Keep it professional but entertaining
- Add humor where appropriate
- Use emojis sparingly for emphasis
- Make the person feel like the protagonist of their own story
- Wrap everything in styled HTML (use inline styles, make it visually appealing)
- Use a modern, clean design with a color palette that matches the week's "mood"

IMPORTANT: Return ONLY the HTML content (no markdown code fences). Start with a <div> tag."""


def _prepare_data_summary(weekly_data: dict) -> str:
    """Convert raw Work IQ data into a readable summary for the LLM."""
    user = weekly_data.get("user", {})
    events = weekly_data.get("calendar_events", [])
    emails = weekly_data.get("emails", [])
    chats = weekly_data.get("teams_chats", [])

    summary_parts = []

    # User info
    summary_parts.append(f"Person: {user.get('displayName', 'Unknown')}")
    summary_parts.append(f"Job Title: {user.get('jobTitle', 'Unknown')}")
    summary_parts.append(f"Period: {weekly_data['period']['start'][:10]} to {weekly_data['period']['end'][:10]}")
    summary_parts.append("")

    # Calendar events
    summary_parts.append(f"=== CALENDAR ({len(events)} events) ===")
    for event in events:
        subject = event.get("subject", "No subject")
        start_data = event.get("start", "")
        # Handle both formats: string and datetime object
        if isinstance(start_data, dict):
            start = start_data.get("dateTime", "")[:16]
        else:
            start = str(start_data)[:16]
        attendees = len(event.get("attendees", []))
        summary_parts.append(f"- {start}: {subject} ({attendees} attendees)")
    summary_parts.append("")

    # Emails
    summary_parts.append(f"=== EMAILS ({len(emails)} messages) ===")
    for email in emails:
        subject = email.get("subject", "No subject")
        from_data = email.get("from", {})
        # Handle both formats: dict and string
        if isinstance(from_data, dict):
            sender = from_data.get("emailAddress", {}).get("name", "Unknown")
        else:
            sender = str(from_data) if from_data else "Unknown"
        preview = email.get("preview", email.get("bodyPreview", ""))[:100]
        summary_parts.append(f"- From {sender}: {subject}")
        if preview:
            summary_parts.append(f"  Preview: {preview}")
    summary_parts.append("")

    # Teams chats
    summary_parts.append(f"=== TEAMS CHATS ({len(chats)} messages) ===")
    for chat in chats:
        sender = chat.get("from", "Unknown")
        topic = chat.get("chatTopic", "DM")
        content = chat.get("content", "")[:100]
        summary_parts.append(f"- [{topic}] {sender}: {content}")

    return "\n".join(summary_parts)


async def generate_story(weekly_data: dict) -> str:
    """Generate a creative Week in Review story from Work IQ data."""
    data_summary = _prepare_data_summary(weekly_data)

    user_prompt = f"""Here is my work week data. Please create my "Week in Review" story:

{data_summary}

Remember: Return styled HTML content only. Make it visually stunning and fun to read!"""

    response = client.chat.completions.create(
        model=GITHUB_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.9,
        max_tokens=4000,
    )

    content = response.choices[0].message.content
    # Strip markdown code fences if the model wraps the HTML
    if content.startswith("```"):
        lines = content.split("\n")
        # Remove first line (```html) and last line (```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        content = "\n".join(lines)
    return content


async def generate_story_from_sample(sample_data: dict) -> str:
    """Generate story from sample data (demo mode)."""
    return await generate_story(sample_data)
