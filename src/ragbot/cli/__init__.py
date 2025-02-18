import typer

from .milvus_cli import cli as milvus_cli
from .tinydb_cli import cli as tinydb_cli

app = typer.Typer(
    name="Ragbot CLI",
    help="Ragbot tools.",
    add_completion=True,
    pretty_exceptions_enable=True,
)


app.add_typer(milvus_cli, name="milvus")
app.add_typer(tinydb_cli, name="tinydb")


if __name__ == "__main__":
    app()
