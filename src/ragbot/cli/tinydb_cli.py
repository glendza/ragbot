import typer
from rich.console import Console
from tinydb import TinyDB

from ragbot.container import RagbotContainer

console = Console()


cli = typer.Typer(
    name="TinyDB",
    help="Manage TinyDB database and its tables.",
    add_completion=True,
)


@cli.command(
    name="truncate-table",
    help="Truncate a table in the TinyDB database.",
)
def truncate_table() -> None:
    # Bootstrap the container:
    app_container = RagbotContainer.from_default_config()

    db_path = app_container.config.tinydb.db_path()
    if not db_path:
        console.print("TinyDB path not set. Skipping truncation.")
        return

    table_name = app_container.config.tinydb.table_name()
    if not table_name:
        console.print("TinyDB table name not set. Skipping truncation.")
        return

    # Initialize the TinyDB database and the context table:
    db = TinyDB(db_path)
    table = db.table(table_name)

    # Truncate the table:
    table.truncate()

    console.print(f"Table '{table_name}' truncated.")
