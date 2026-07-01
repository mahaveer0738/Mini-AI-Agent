import json
import os

from agent.gemini import client
from agent.prompts import MEMORY_EXTRACTION_PROMPT

MEMORY_FILE = "data/memory.json"


def load_memory():
    """Load memory from memory.json"""

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_memory(memory):
    """Save memory to memory.json"""

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def add_memory(memory_type, key, value):
    """Add or update memory"""

    memory = load_memory()

    # Update existing memory
    for item in memory:

        if item["key"].lower() == key.lower():

            item["value"] = value
            item["type"] = memory_type

            save_memory(memory)

            return f"🧠 Updated {key}."

    # Add new memory
    new_memory = {
        "id": len(memory) + 1,
        "type": memory_type,
        "key": key,
        "value": value
    }

    memory.append(new_memory)

    save_memory(memory)

    return f"🧠 Remembered {key}."


def search_memory(key):
    """Search memory by key"""

    memory = load_memory()

    key = key.lower()

    for item in memory:

        if item["key"].lower() == key:
            return item["value"]

    return None


def extract_memory(user_input):
    """Use Gemini to extract structured memory"""

    prompt = f"""
{MEMORY_EXTRACTION_PROMPT}

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

    # Debug
    print("\n========== MEMORY EXTRACTION ==========")
    print(text)
    print("=======================================\n")

    try:
        data = json.loads(text)
    except Exception:
        raise ValueError(f"Gemini returned invalid JSON:\n{text}")

    return data


def memory(user_input):
    """
    Main Memory Tool.
    """

    text = user_input.lower()

    # ==================================================
    # SHOW ALL MEMORIES
    # ==================================================

    if "what do you remember" in text:

        memory_list = load_memory()

        if not memory_list:
            return "I don't remember anything yet."

        output = ""

        for item in memory_list:
            output += (
                f"{item['key']} : {item['value']} "
                f"({item['type']})\n"
            )

        return output

    # ==================================================
    # STORE MEMORY
    # ==================================================

    elif "remember" in text:

        try:

            extracted = extract_memory(user_input)

            if not all(
                key in extracted
                for key in ("type", "key", "value")
            ):
                return f"Memory Error: Invalid JSON returned -> {extracted}"

            return add_memory(
                extracted["type"],
                extracted["key"],
                extracted["value"]
            )

        except Exception as e:

            return f"Memory Error: {e}"

    # ==================================================
    # RETRIEVE SINGLE MEMORY
    # ==================================================

    elif (
        "what is my" in text
        or "where do i" in text
        or "who am i" in text
        or "what's my" in text
    ):

        try:

            extracted = extract_memory(user_input)

            if "key" not in extracted:
                return f"Memory Error: Invalid JSON returned -> {extracted}"

            value = search_memory(extracted["key"])

            if value:
                return value

            return "I don't know that yet."

        except Exception as e:

            return f"Memory Error: {e}"

    return "Memory request not understood."