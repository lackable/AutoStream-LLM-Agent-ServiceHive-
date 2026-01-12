from llm import get_llm

INTENTS = ["greeting", "product_inquiry", "high_intent"]

def detect_intent_llm(user_message: str) -> str:
    llm = get_llm()

    prompt = f"""
You are an intent classification system for a SaaS product called AutoStream.

Classify the user's message into EXACTLY ONE of the following intents:
- greeting
- product_inquiry
- high_intent

Rules:
- Respond with ONLY the intent name
- No explanation
- No punctuation

User message:
"{user_message}"
"""

    response = llm.invoke(prompt).content.strip().lower()

    if response not in INTENTS:
        return "product_inquiry"  # safe default

    return response
