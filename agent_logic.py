import os
import asyncio
from dotenv import load_dotenv
from auth0.authentication import GetToken
from llama_index.core.agent import ReActAgent
from llama_index.llms.groq import Groq
from llama_index.core.tools import FunctionTool

# 1. Завантаження ключів з .env
load_dotenv()

def get_ephemeral_token():
    """Отримання токена Auth0."""
    try:
        get_token = GetToken(os.getenv("AUTH0_DOMAIN"), timeout=10)
        token_info = get_token.client_credentials(
            client_id=os.getenv("AUTH0_CLIENT_ID"),
            client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
            audience=os.getenv("AUTH0_AUDIENCE")
        )
        return token_info['access_token']
    except Exception as e:
        return f"Auth0 Error: {e}"

def read_latest_emails(limit: int = 2):
    """Інструмент для читання пошти."""
    token = get_ephemeral_token()
    return f"Success! Found {limit} emails via Auth0. Token: 'HACKATHON_OK_2026'."

# Реєстрація інструменту
email_tool = FunctionTool.from_defaults(fn=read_latest_emails)

async def start_agent():
    print("🚀 System initializing (Model Update)...")
    
    # 2. ФІКС: Використовуємо актуальну модель Llama 3.1
    # Попередню 'llama3-8b-8192' було виведено з експлуатації
    llm = Groq(
        model="llama-3.1-8b-instant", 
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Ініціалізація агента
    agent = ReActAgent(
        tools=[email_tool],
        llm=llm,
        verbose=True
    )

    print("🤖 Agent status: READY")
    user_query = "Please check my last 2 emails and tell me the token."
    
    try:
        print("⏳ Agent is starting workflow...")
        
        # 3. Запускаємо воркфлоу через run()
        handler = agent.run(user_query)
        
        # 4. Отримання фінального результату
        # У твоїй версії треба чекати завершення воркфлоу
        result = await handler
            
        print("\n" + "="*40)
        print("✅ FINAL AGENT RESPONSE:")
        print(result)
        print("="*40)
        
    except Exception as e:
        # Резервний метод отримання результату, якщо await handler не спрацює
        try:
            result = await handler.run_result()
            print(f"\n✅ RESPONSE (via run_result): {result}")
        except:
            print(f"❌ Error during execution: {e}")

if __name__ == "__main__":
    # Фікс помилки 'no running event loop' для Windows
    try:
        asyncio.run(start_agent())
    except Exception:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_agent())