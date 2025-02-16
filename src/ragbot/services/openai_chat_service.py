from openai import AsyncOpenAI

from ragbot.interfaces import AiChatService


class OpenAIChatService(AiChatService):
    def __init__(self, openai_client: AsyncOpenAI) -> None:
        self._openai_client = openai_client

    async def process_message(self, message: str) -> str:
        response = await self._openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                # {
                #     "role": "system",
                #     "content": "TODO: Specialize here",
                # },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            # store=True,
        )
        if not response.choices or not response.choices[0].message.content:
            return "I'm sorry, I don't understand."  # TODO: parameterize this

        return response.choices[0].message.content
