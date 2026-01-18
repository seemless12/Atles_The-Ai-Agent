"""
Simple LangChain Chatbot with OpenRouter Integration
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
import requests

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
FREECRYPTO_API_KEY = os.getenv("FREECRYPTO_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-3.1-8b-instruct")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions" # User provided URL
# Clean URL for LangChain (it needs the base URL, not the full endpoint)
BASE_URL = OPENROUTER_URL.replace("/chat/completions", "").strip()
if BASE_URL.endswith("/"):
    BASE_URL = BASE_URL[:-1]

# Initialize the LLM with OpenRouter
# Note: LangChain's ChatOpenAI uses the base URL, but we'll include the user's suggestion in comments
# Suggested URL: https://openrouter.ai/api/v1/chat/completions
llm = ChatOpenAI(
    model=MODEL_NAME,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base=BASE_URL,
    temperature=0.7,
    max_tokens=1000,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "Crypto Chatbot"
    }
)

# Load System Prompt and Knowledge Base
def load_context():
    try:
        with open("systemprompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
        with open("Crypto_Knowledge_Base.md", "r", encoding="utf-8") as f:
            knowledge_base = f.read()
        
        full_context = f"{system_prompt}\n\n### KNOWLEDGE BASE ###\n{knowledge_base}"
        # Escape curly braces for ChatPromptTemplate
        return full_context.replace("{", "{{").replace("}", "}}")
    except FileNotFoundError as e:
        print(f"⚠️ Warning: Context file not found: {e.filename}")
        return "You are a crypto assistant."

# --- Tools ---

@tool
def get_crypto_conversion(from_coin: str, to_coin: str, amount: float = 1.0):
    """
    Convert between any two cryptocurrencies or from crypto to fiat.
    Example: from_coin="BTC", to_coin="USD", amount=0.5
    """
    url = "https://api.freecryptoapi.com/v1/getConversion"
    headers = {
        "api_key": FREECRYPTO_API_KEY,
        "Authorization": f"Bearer {FREECRYPTO_API_KEY}"
    }
    params = {
        "from": from_coin.upper(),
        "to": to_coin.upper(),
        "amount": amount
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # Based on the API, we expect a 'result' or similar field. 
            # If the API returns a direct numeric value or a dict, we handle it.
            return str(data)
        else:
            return f"Error from Conversion API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception during conversion: {str(e)}"

tools = [get_crypto_conversion]

# --- Agent Setup ---
SYSTEM_CONTEXT = load_context()

# Initialize conversation memory
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

# Create Chat Prompt Template for Agent
# We add a very strict instruction to avoid JSON output
prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_CONTEXT + "\n\nCRITICAL: You are a friendly AI. Never output raw JSON or tool-call syntax directly to the user. Always wait for the tool output and then explain it in natural language. If you are about to output something like '{{\"name\": ...}}', STOP and rewrite it as a natural sentence."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create Agent
try:
    agent = create_openai_tools_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
except Exception as e:
    agent_executor = None
    print(f"⚠️ Warning: Agent initialization failed: {str(e)}")

# --- Initialized Agent ---
def get_agent_executor():
    """Return the initialized agent executor."""
    return agent_executor

def print_header():
    """Print chatbot header"""
    print("\n" + "="*60)
    print("🤖 Atlas Crypto Intelligence Agent")
    print("="*60)
    print("Model:", MODEL_NAME)
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("="*60 + "\n")

def chat():
    """Main chat loop"""
    print_header()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Thanks for chatting!\n")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get response from the chatbot agent
            if agent_executor:
                result = agent_executor.invoke({"input": user_input})
                response = result["output"]
            else:
                # Manual memory fallback (though history key changed)
                messages = [
                    SystemMessage(content=SYSTEM_CONTEXT),
                    HumanMessage(content=user_input)
                ]
                ai_response = llm.invoke(messages)
                response = ai_response.content
                memory.save_context({"input": user_input}, {"output": response})
            
            # Print the response
            print(f"\nBot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            print("Please check your API key and internet connection.\n")
            break

if __name__ == "__main__":
    # Check if API key is set
    if not OPENROUTER_API_KEY:
        print("\n❌ Error: OPENROUTER_API_KEY not found in .env file")
        print("Please create a .env file with your OpenRouter API key\n")
    else:
        chat()
