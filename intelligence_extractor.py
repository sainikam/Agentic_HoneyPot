from llm_client import BedrockLLM
from json_utils import extract_json

llm = BedrockLLM(model="llama3")

def extract_intelligence(history):
    convo = "\n".join(history[-10:])  # keep last turns short

    prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

Extract scam intelligence from the conversation.

JSON schema (must match exactly):
{{
  "bank_accounts": [],
  "ifsc_codes": [],
  "upi_ids": [],
  "phishing_links": []
}}

Conversation:
{convo}
"""

    raw = llm.ask(prompt)
    data = extract_json(raw)

    # enforce keys
    for k in ["bank_accounts", "ifsc_codes", "upi_ids", "phishing_links"]:
        data.setdefault(k, [])
        if not isinstance(data[k], list):
            data[k] = [str(data[k])]

    return data

