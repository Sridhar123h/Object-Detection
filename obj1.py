import json
import os
from datetime import datetime

# ---------- MEMORY HANDLING ----------
MEMORY_FILE = "jarvis_memory.json"

def initialize_memory():
    if not os.path.exists(MEMORY_FILE):
        memory = {
            "user_preferences": {},
            "interaction_history": [],
            "routines": []
        }
        save_memory(memory)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- INPUT & LEARNING ----------
def log_interaction(command):
    memory = load_memory()
    memory["interaction_history"].append({
        "command": command,
        "timestamp": datetime.now().isoformat()
    })
    save_memory(memory)

def update_preference(key, value):
    memory = load_memory()
    memory["user_preferences"][key] = value
    save_memory(memory)

def show_suggestions():
    memory = load_memory()
    if not memory["interaction_history"]:
        return "No suggestions yet."
    
    commands = [entry["command"] for entry in memory["interaction_history"]]
    suggestion = max(set(commands), key=commands.count)
    return f"Based on your usage, may I suggest: '{suggestion}'?"

# ---------- ROUTINE LEARNING ----------
def log_routine(command):
    now = datetime.now().strftime("%H:%M")
    memory = load_memory()
    memory["routines"].append({"time": now, "command": command})
    save_memory(memory)

def check_routine():
    now = datetime.now().strftime("%H:%M")
    memory = load_memory()
    for r in memory["routines"]:
        if r["time"] == now:
            return f"Routine match found: {r['command']}"
    return None

# ---------- MAIN LOOP ----------
def main():
    initialize_memory()
    print("Hello! I am JARVIS. Let's learn together.")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        if user_input == "exit":
            print("Goodbye!")
            break
        
        elif user_input.startswith("set preference"):
            _, key, value = user_input.split(maxsplit=2)
            update_preference(key, value)
            print(f"Got it. Set {key} to {value}.")
        
        elif user_input == "show suggestion":
            print(show_suggestions())

        elif user_input == "check routine":
            result = check_routine()
            print(result if result else "No routine match now.")
        
        else:
            log_interaction(user_input)
            log_routine(user_input)
            print(f"Understood: '{user_input}'. I'm learning this.")

if __name__ == "__main__":
    main()
