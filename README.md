# Social-to-Lead Agentic Workflow – AutoStream

## 📌 Project Overview

This project implements a **Conversational AI Agent** for a fictional SaaS product called **AutoStream**, which provides automated video editing tools for content creators.

The agent is designed to convert conversational user interactions into **qualified business leads**, following a structured agentic workflow rather than functioning as a simple chatbot.

The implementation satisfies all mandatory requirements outlined in the assignment, including intent detection, RAG-based knowledge retrieval, multi-turn state management, and controlled tool execution.

---

## 🧠 Agent Capabilities

### 1. Intent Identification (LLM-Based)

User messages are classified into one of three intents:
- `greeting`
- `product_inquiry`
- `high_intent`

Intent detection is performed using an LLM with a constrained prompt to ensure deterministic and controlled outputs.

---

### 2. RAG-Powered Knowledge Retrieval

Product-related questions are answered using a **Retrieval-Augmented Generation (RAG)** pipeline built on a local knowledge base.

**Knowledge Source**
- Stored locally in `knowledge_base.json`
- Contains:
  - Pricing plans
  - Feature descriptions
  - Company policies

**RAG Pipeline**
1. Knowledge base content is embedded using **Gemini embeddings**
2. Embeddings are stored in a **FAISS vector store**
3. Relevant documents are retrieved for each user query
4. Retrieved context is passed to the LLM to generate grounded responses

---

### 3. Lead Qualification & Tool Execution

When a user shows **high intent**, the agent transitions into a lead qualification phase and sequentially collects:
1. Name  
2. Email (validated before acceptance)

After collecting both values, the agent triggers a mock backend tool:

```python
def mock_lead_capture(name, email):
    print(f"Lead captured successfully: {name}, {email}")


## 🧩 Architecture Explanation

The AutoStream conversational agent is built using a modular, agentic architecture that separates **intent reasoning, knowledge retrieval, state management, and action execution**.

User messages are first processed by an **LLM-based intent classification module**, which categorizes each input into one of three predefined intents: greeting, product inquiry, or high intent. The intent classifier uses a constrained prompt to ensure deterministic and controlled outputs while still leveraging the LLM’s natural language understanding.

For product-related questions, the agent employs a **Retrieval-Augmented Generation (RAG)** pipeline. A local knowledge base stored in JSON format is embedded using **Gemini embeddings** and indexed in a **FAISS vector store**. When a query is received, the most relevant documents are retrieved and passed as context to the LLM, ensuring accurate and grounded responses without hallucination.

State management is handled through an **explicit conversation state object** that persists across turns. This state tracks the detected intent, lead qualification status, and collected user details, allowing the agent to retain memory across 5–6 conversation turns. This approach provides deterministic control and is functionally equivalent to LangGraph or memory buffer–based state management.

Once high intent is detected, the agent transitions into a lead qualification phase, sequentially collecting the user’s name and email. A mock lead capture tool is executed **only after** valid details are collected, ensuring safe and realistic agent behavior.


## ⚙️ How to Run the Project Locally

Follow the steps below to run the AutoStream conversational agent on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/lackable/AutoStream-LLM-Agent-ServiceHive-.git
cd AutoStream-LLM-Agent-ServiceHive-

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Setup .env key

GOOGLE_API_KEY = <APIKEY>

### 4. Run The Agent

python main.py


## 📱 WhatsApp Deployment Using Webhooks

To deploy the AutoStream agent on WhatsApp, we would use a webhook-based architecture with the WhatsApp Cloud API.

We would connect the webhooks to an API retrieved from a Whatsapp Buisness account.

A backend service (built using **FastAPI**) would expose this webhook endpoint. When a message is received, the webhook handler would:
1. Extract the user’s WhatsApp number (used as a unique user ID)
2. Extract the message text
3. Forward the message to the AutoStream agent logic

Conversation state would be stored in an external store like a database, keyed by the user’s WhatsApp number. This ensures the agent can maintain context across multiple messages and conversations.

The agent processes the message using intent detection, RAG, and lead qualification logic, and returns a response. The backend then sends this response back to the user via the WhatsApp Cloud API’s send message endpoint.

This architecture allows the same agent logic to support multiple users concurrently, ensures reliable state management, and enables easy scaling without modifying the core agent code.
