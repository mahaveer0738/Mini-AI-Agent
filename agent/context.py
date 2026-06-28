from agent.memory import load_memory


def build_context(current_prompt):
    """
    Build conversation context for Gemini.
    """

    memory = load_memory()

    context = ""

    for message in memory:

        role = message["role"].capitalize()

        context += f"{role}: {message['content']}\n"

    context += f"User: {current_prompt}\n"

    context += "Assistant:"

    return context