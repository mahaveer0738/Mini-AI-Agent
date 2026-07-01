from agent.gemini import client
from agent.memory import add_message
from agent.context import build_context


def chat_with_gemini(user_prompt):

    context = build_context(user_prompt)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
    )

    assistant_reply = response.text

    add_message("user", user_prompt)
    add_message("assistant", assistant_reply)

    return assistant_reply