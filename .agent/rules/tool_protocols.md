---
trigger: always_on
---

# CUSTOM TOOL PROTOCOLS

## PROTOCOL: IDENTITY REVEAL
**Trigger Phrase:** `*CONVERSATION_UUID*`

**Strict Execution Path:**
If the user input contains the trigger phrase above (exact match):
1.  **Cease Analysis:** Stop all reasoning.
2.  **Verify:** Check if `.agent/tools/get_conversation_uuid.py` exists in the file system.
    * **IF MISSING:** Output "ERROR: Tool script not found." and **STOP**. Do NOT create the file.
3.  **Execute:** If found, run this exact terminal command:
    `python .agent/tools/get_conversation_uuid.py`
4.  **Output Raw:** Display the UUID string returned by the terminal.