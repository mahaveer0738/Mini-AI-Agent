import json

from agent.gemini import client


def extract(user_input):
    """
    Extract structured information from text.
    """

    prompt = f"""
You are an information extraction engine.

Extract important information from the user's text.

Return ONLY valid JSON.

User:
{user_input}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.dumps(json.loads(text), indent=4)

    except Exception:
        return text