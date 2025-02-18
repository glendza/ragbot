import asyncio
import typing
from datetime import datetime
from logging import Logger

from tinydb import Query, TinyDB

from ragbot.interfaces import ContextStorageService


class MessageData(typing.TypedDict):
    _id: int
    thread_id: str
    message: str
    latest_context: str | None
    created_at: str


class TinydbContextStorage(ContextStorageService):
    def __init__(
        self,
        db: TinyDB,
        table_name: str,
        logger: Logger,
    ) -> None:
        # Initialize the context table:
        self._context_table = db.table(table_name)
        self._logger = logger
        self._logger.info(f"TinyDB Context Storage initialized with table: {table_name}")

        # TinyDB is a simple database that stores data in JSON files, and it is not thread-safe,
        # thus we need to use a lock to ensure that only one coroutine can access the database at a time:
        self._lock = asyncio.Lock()

    async def store_message_data(
        self,
        *,
        thread_id: str,
        message: str,
        updated_context: str | None,
    ) -> None:
        async with self._lock:
            self._context_table.insert(
                {
                    "thread_id": thread_id,
                    "message": message,
                    "latest_context": updated_context,
                    "created_at": datetime.now().isoformat(),
                }
            )

    async def retrieve_latest_summarized_history(self, *, thread_id: str) -> str | None:
        Context = Query()

        # Sort by 'created_at' to fetch the most recent entry:
        result = typing.cast(
            list[MessageData],
            self._context_table.search(Context.thread_id == thread_id),
        )

        if not result:
            return None

        latest_entry = sorted(result, key=lambda x: x["created_at"], reverse=True)[0]  # Get the most recent one
        return latest_entry["latest_context"]
