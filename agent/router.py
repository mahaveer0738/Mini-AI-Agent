import os
import json

from dotenv import load_dotenv
from google import genai

from agent.prompts import ROUTER_PROMPT

# Load API Key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini Client
client = genai.Client(api_key=api_key)


def detect_route(user_input):
    """
    Uses Gemini to decide which tool should handle the user's request.
    """

    # Build router prompt
    router_input = f"""
    {ROUTER_PROMPT}

    User Request:
    {user_input}
    """
    #print("\n========== ROUTER PROMPT ==========\n")
   # print(router_input)
   # print("\n===================================\n")

    # Ask Gemini Router
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=router_input
    )

    router_response = response.text.strip()

    router_response = (
        router_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    #TO check the respose of GEMINI
   # print("\n========== RAW GEMINI RESPONSE ==========")
    #print(router_response)
    #print("=========================================\n")

    # Convert JSON string to Python Dictionary
    try:
        route = json.loads(router_response)

    except json.JSONDecodeError:

        route = {
            "intent": "chat",
            "parallel": False,
            "steps": [
                {
                    "step": 1,
                    "tool": "chat",
                    "input": user_input
                }
            ],
            "confidence": 0.0,
            "reason": "Router failed to generate valid JSON."
        }

    return route