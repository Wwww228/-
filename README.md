# AI Agent: Smilivi Shvorni 🚀

Autonomous AI agent that retrieves secure data using **Llama 3.1** and **Auth0**.

## Features:
- **Fast Reasoning:** Powered by Groq for near-instant responses.
- **Secure Access:** Integrated with Auth0 (OAuth2) to protect sensitive data.
- **Autonomous Logic:** Uses ReAct framework to decide when to call email tools.

## How it works:
1. The agent receives a request (e.g., "Find the secret token in my emails").
2. It authenticates via **Auth0**.
3. It calls the `read_latest_emails` tool.
4. It extracts and provides the final answer: **HACKATHON_OK_2026**.

## Tech Stack:
- LlamaIndex (Agent Framework)
- Groq / Llama 3.1 (LLM)
- Auth0 (Authentication)
- Python
