import os
from dotenv import load_dotenv
from google import genai

from agent.memory import add_message
from agent.context import build_context
# Load variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

def chat_with_gemini(user_prompt):

    # Build conversation context
    context = build_context(user_prompt)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
    )

    assistant_reply = response.text

    # Save conversation
    add_message("user", user_prompt)
    add_message("assistant", assistant_reply)

    return assistant_reply