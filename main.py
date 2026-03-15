import asyncio
from agent import send_async_message


async def main():
    while(True):
        user_query = input("User: ")

        if user_query == "/exit":
            print("Thank you!!")
            break

        ai_response = await send_async_message(user_query=user_query)
        print(f"AI: {ai_response}\n")

asyncio.run(main())