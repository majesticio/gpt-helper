import asyncio
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant, do not say you are an AI or explain what you are.",
    },
]


async def generate_text(prompt, conversation_history):
    # Add user message to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    completion = await asyncio.to_thread(
        openai.ChatCompletion.create,
        model="gpt-3.5-turbo",
        messages=conversation_history,
    )

    # Extract assistant response and add it to the conversation history
    assistant_response = completion.choices[0]["message"]["content"]
    conversation_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response


def count_words(text):
    return len(text.split())


def truncate_conversation_history(conversation_history, max_words=750):
    words = 0
    truncated_history = []
    system_message = conversation_history[0]

    for message in reversed(conversation_history[1:]):  # Skip the system message
        message_words = count_words(message["content"])
        words += message_words

        if words > max_words:
            break

        truncated_history.insert(0, message)

    # Keep the system message at the beginning
    truncated_history.insert(0, system_message)
    return truncated_history


async def main():
    global conversation_history
    while True:
        try:
            # Truncate the conversation history if it exceeds the word limit
            conversation_history = truncate_conversation_history(conversation_history)

            # Call generate_text with the truncated conversation history
            user_input = input("Ask something (type 'quit' to exit): ").strip()

            if user_input.lower() == "quit":
                break

            response = await generate_text(user_input, conversation_history)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
