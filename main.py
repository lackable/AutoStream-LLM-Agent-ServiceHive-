from agent import agent_step

state = {
    "messages": [],
    "intent": None,
    "lead_mode": False,
    "name": None,
    "email": None
}

while True:
    user = input("User: ")
    response = agent_step(state, user)
    print("Agent:", response)
