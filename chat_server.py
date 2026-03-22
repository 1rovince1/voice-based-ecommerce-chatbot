from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from agents.chat_agent import gemini_chat, ollama_chat


def select_chat_provider():
    if os.getenv("GEMINI_API_KEY"):
        print("Found Gemini key, starting Gemini based chat session...")
        return gemini_chat
    
    elif os.getenv("OLLAMA_API_KEY"):
        print("Found Ollama api key, starting Ollama based chat session...")
        return ollama_chat
    
    raise RuntimeError("No LLM provider configured")


print("Starting main")
async def main():
    print("Starting chat")
    ai_chat = select_chat_provider()
    
    while(True):
        user_query = input("User: ")

        if user_query == "/exit":
            print("Thank you!!")
            break

        ai_response = await ai_chat(user_query=user_query)
        print(f"AI: {ai_response}\n")


asyncio.run(main())