import json
import os

MEMORY_FILE = "data/memory.json"

#Load the memory using load function
def load_memory():
    """Load conversation history from memory.json"""

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)
    
#Save the mrmory using dump function
def save_memory(memory):
    """Save conversation history to memory.json"""

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)
        
#Add messages using append function
def add_message(role, content):
    """Add a new message to memory"""

    memory = load_memory()

    memory.append({
        "role": role,
        "content": content
    })

    # Keep only the last 10 messages
    memory = memory[-10:]

    save_memory(memory)