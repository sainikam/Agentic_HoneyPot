import os
import requests

class BedrockLLM:
    """
    Keep the same class name so your code doesn't break.
    In production (Render), uses Gemini if GEMINI_API_KEY exists.
    Otherwise returns a safe fallback reply (no localhost calls).
    """
    def __init__(self, model="llama3"):
        self.model = model
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    def ask(self, prompt: str) -> str:
        # Use Gemini in production
        if self.gemini_key:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            params = {"key": self.gemini_key}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}

            r = requests.post(url, params=params, json=payload, timeout=20)
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Safe fallback (prevents 500)
        return "I am trying to understand. Can you share the payment details again?"
