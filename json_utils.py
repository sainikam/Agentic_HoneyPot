import json
import re

def extract_json(text: str):
    text = text.strip()

    # Try direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find the first {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output.")

    return json.loads(match.group(0))
