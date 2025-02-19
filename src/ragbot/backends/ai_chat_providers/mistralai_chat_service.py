from logging import Logger

from mistralai import Messages, Mistral, SystemMessage, UserMessage

from ragbot.interfaces import AIChatService
from ragbot.models.dtos import RagSearchResults
from ragbot.models.structured_outputs import ChatResponse


class MistralAIChatService(AIChatService):
    def __init__(
        self,
        logger: Logger,
        mistralai_client: Mistral,
        model: str,
        temperature: float,
        max_tokens: int,
        conversational_schema: str | None = None,
    ) -> None:
        self._logger = logger
        self._mistralai_client = mistralai_client
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._conversational_schema = conversational_schema

    async def process_message(
        self,
        *,
        message: str,
        retrieved_context: RagSearchResults,
        summarized_chat_history: str | None,
    ) -> ChatResponse:
        # Conversational schema:
        conversational_schema: SystemMessage | None = (
            SystemMessage(
                content=self._conversational_schema,
            )
            if self._conversational_schema
            else None
        )

        # Retrieved knowledge:
        retrieved_knowledge_entries = "\n".join(
            f'{i + 1}. "{r.content}" (score: {r.distance:.4f})' for i, r in enumerate(retrieved_context.root)
        )
        retrieved_knowledge: SystemMessage | None = (
            SystemMessage(
                content=f"Retrieved knowledge:\n\n{retrieved_knowledge_entries}",
            )
            if retrieved_context.root
            else None
        )

        # Chat history context:
        history_context: SystemMessage | None = (
            SystemMessage(
                content=f"Here is the summarized chat history for reference:\n\n{summarized_chat_history}",
            )
            if summarized_chat_history
            else None
        )

        # User message:
        user_message: UserMessage = UserMessage(content=message)

        messages: list[Messages] = [
            m
            for m in [
                # NOTE: The order of these messages is important!
                conversational_schema,
                retrieved_knowledge,
                history_context,
                user_message,
            ]
            if m
        ]

        # Send the message to the Mistral AI API:
        response = await self._mistralai_client.chat.parse_async(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=messages,
            response_format=ChatResponse,
        )

        self._logger.info(
            "Spent %d tokens for replying to chat message (%d prompt + %d completion tokens)",
            response.usage.total_tokens,
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
        )

        # Extract the response from the API response:
        if not response.choices or not response.choices[0].message or not response.choices[0].message.parsed:
            return ChatResponse(
                message="I'm sorry, I don't have a response for that.",
                summarized_context=summarized_chat_history,  # Nothing to update
            )

        return response.choices[0].message.parsed
