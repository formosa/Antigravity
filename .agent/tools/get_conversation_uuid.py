"""
Tool Name: get_conversation_uuid
Description: Identifies the UUID of the active conversation by finding the most recently modified database file.
Triggers: "*CONVERSATION_UUID*"
"""
import os
import glob

# Auto-detect user home path
USER_BASE = os.path.expanduser('~')
CONVERSATION_PATH = os.path.join(USER_BASE, ".gemini", "antigravity", "conversations")

def execute():
    # 1. Validation
    if not os.path.exists(CONVERSATION_PATH):
        return f"ERROR: Path not found: {CONVERSATION_PATH}"

    # 2. Scan for .pb files
    files = glob.glob(os.path.join(CONVERSATION_PATH, "*.pb"))
    if not files:
        return "ERROR: No conversation history found."

    # 3. Find newest file (The one currently being written to)
    latest_file = max(files, key=os.path.getmtime)
    
    # 4. Extract UUID
    filename = os.path.basename(latest_file)
    uuid = os.path.splitext(filename)[0]
    
    return f"CONVERSATION_UUID: {uuid}"

if __name__ == "__main__":
    print(execute())