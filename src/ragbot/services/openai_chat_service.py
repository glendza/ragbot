from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ragbot.interfaces import AiChatService


class OpenAIChatService(AiChatService):
    def __init__(
        self,
        openai_client: AsyncOpenAI,
        conversational_schema: str | None = None,
    ) -> None:
        self._openai_client = openai_client
        self._conversational_schema = conversational_schema

    async def process_message(self, message: str) -> str:
        # Prepare the message for the OpenAI API:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "user",
                "content": message,
            },
        ]

        # Prepend the conversational schema to the messages, if provided:
        if self._conversational_schema:
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": self._conversational_schema,
                },
            )

        # Send the message to the OpenAI API:
        response = await self._openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            store=False,
        )

        # Extract the response from the API response:
        if not response.choices or not response.choices[0].message.content:
            return "I'm sorry, I don't understand."  # TODO: parameterize this

        return response.choices[0].message.content
