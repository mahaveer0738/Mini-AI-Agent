import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as file:
        try:
            return json.load(file)
        except:
            return []


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def remember(text):

    memory = load_memory()

    memory.append({
        "memory": text
    })

    save_memory(memory)

    return f"🧠 Remembered: {text}"


def recall(query):

    memory = load_memory()

    query = query.lower()

    results = []

    for item in memory:

        if query in item["memory"].lower():
            results.append(item["memory"])

    if results:
        return "\n".join(results)

    return "I don't remember anything about that."


def memory_tool(user_input):

    lower = user_input.lower()

    if lower.startswith("remember"):

        fact = (
            user_input
            .replace("Remember", "")
            .replace("remember", "")
            .strip()
        )

        return remember(fact)

    elif "what do you remember" in lower:

        memory = load_memory()

        if not memory:
            return "Memory is empty."

        return "\n".join([m["memory"] for m in memory])

    else:

        return recall(user_input)