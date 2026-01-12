import re
from intents import detect_intent_llm
from rag import query_rag
from tools import mock_lead_capture

def is_valid_email(email: str) -> bool:
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None

def agent_step(state, user_input):
    state["messages"].append(user_input)

    intent = detect_intent_llm(user_input)
    state["intent"] = intent

    if not state["lead_mode"]:
        if intent == "greeting":
            return "Hi! How can I help you with AutoStream today?"

        if intent == "product_inquiry":
            return query_rag(user_input)

        if intent == "high_intent":
            state["lead_mode"] = True
            return "Great! Before we get you started, may I know your name?"

    if state["lead_mode"]:
        if state["name"] is None:
            state["name"] = user_input
            return "Thanks! Could you share your email address?"

        if state["email"] is None:
            if not is_valid_email(user_input):
                return (
                    "That doesn't look like a valid email address. "
                    "Could you please enter a valid email?"
                )

            state["email"] = user_input
            mock_lead_capture(
                state["name"],
                state["email"]
            )
            return "You're all set! Our team will reach out to you shortly."

    return "How else can I help you?"
