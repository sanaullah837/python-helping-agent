from ast import Import
import asyncio
from linecache import getline
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# Set up your Gemini API key here
gemini_api_key = "put api key here"


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider,
)

async def main():
    agent = Agent(
        name="Helper Agent",
        instructions="You're a helpful assistant that can answer questions and write essays.",
        model=model,
    )

    # DO NOT await here
    result = Runner.run_streamed(
        agent,
        input="Write an Essay on Programming in 1000 words?",
    )

    # Now stream events
    async for event in result.stream_events():
        # Check if this event has text content
        if hasattr(event, "data") and hasattr(event.data, "delta"):
            print(event.data.delta, end="", flush=True)

    print()  # newline at end

if __name__ == "_main_":
    asyncio.run(main())