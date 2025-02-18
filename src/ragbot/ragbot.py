from dependency_injector.wiring import Provide, inject

from ragbot.container import RagbotContainer
from ragbot.interfaces import AiChatService, ChatService, LoggerFactoryService, RagQueryEngine


@inject
async def run(
    *,
    logger_factory: LoggerFactoryService = Provide[RagbotContainer.logger_factory],
    chat_service: ChatService = Provide[RagbotContainer.chat_service],
    ai_chat_service: AiChatService = Provide[RagbotContainer.ai_chat_service],
    rag_query_service: RagQueryEngine = Provide[RagbotContainer.rag_query_engine],
) -> None:
    logger = logger_factory.get_logger("ragbot_runner")
    logger.info("Starting Ragbot...")

    try:
        async for chat_message in chat_service.messages():
            logger.info(f"Received message: {chat_message.message_text}")

            logger.debug(f"Searching Vector Database for related content for message: {chat_message.message_text}")
            search_results = await rag_query_service.process_query(chat_message.message_text)
            logger.debug(
                f"Retrieved {len(search_results.root)} results from Vector Database:\n\n{search_results.model_dump_json(indent=2)}"
            )

            logger.debug(f"Processing message with AI Chat Service: {chat_message.message_text}")
            response = await ai_chat_service.process_message(
                message=chat_message.message_text,
                retrieved_context=search_results,
            )
            await chat_message.reply(response)
    except Exception:
        logger.exception("Ragbot encountered an unexpected error!")
        raise
